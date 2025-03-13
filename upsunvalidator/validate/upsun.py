import yaml
import ruamel.yaml
from ruamel.yaml.constructor import DuplicateKeyError

# import ruamel.yaml
# from ruamel.yaml.constructor import DuplicateKeyError

# import sys
# sys.tracebacklimit=0

from jsonschema import validate

from upsunvalidator.schemas.upsun import UPSUN_SCHEMA

from upsunvalidator.utils.utils import load_yaml_file, flatten_validation_error
from upsunvalidator.validate.services import validate_service_version, validate_service_schema, validate_service_type, validate_service_version
from upsunvalidator.validate.extensions import validate_php_extensions

from jsonschema import ValidationError

def validate_upsun_config_string(config_yaml_content):
    """Validate a string containing Upsun configuration in YAML format.
    
    Args:
        config_yaml_content (str): String containing the YAML configuration
        
    Returns:
        list: List of validation results or error messages
        
    Raises:
        yaml.YAMLError: If YAML parsing fails
        ValidationError: If validation fails
    """
    # Parse the YAML content
    config = yaml.safe_load(config_yaml_content)
    
    if config is None:
        raise ValidationError("YAML parsing error: Empty configuration")
    
    # Validate the parsed configuration
    return _validate_config(config)

def validate_upsun_config(yaml_files):
    """Validate Upsun configuration files.
    
    Args:
        yaml_files (dict): Dictionary of file paths
        
    Returns:
        list: List of validation results or error messages
    """
    if "upsun" in yaml_files:
        # Combine all files in this directory (Relevant for Upsun only)
        combined = {
            "applications": {},
            "services": {},
            "routes": {}
        }

        for file in yaml_files["upsun"]:
            try:
                data = yaml.safe_load(load_yaml_file(file))
            except yaml.YAMLError as e:
                return [f"YAML parsing error: {e}"]

            # Use ruamel to raise an error iff a duplicate top-level key is included in the same file/string.
            # rYAML = ruamel.yaml.YAML()
            # rYAML.allow_duplicate_keys = False
            # with open(file, "r") as f:
            #     rData = rYAML.load(f)
            # if not rData:
            #     raise DuplicateKeyError

            # Ensure no invalid top-level keys are included in any configuration file.
            invalid_keys = [key for key in data if key not in list(combined.keys())]
            if invalid_keys:
                is_are = "is"
                key_keys = "a valid top-level key"
                if len(invalid_keys) > 1:
                    is_are = "are"
                    key_keys = "valid top-level keys"     
                error_message = f"""
✘ Error found in configuration file {file}.

  '{"', '".join(invalid_keys)}' {is_are} not {key_keys}.

  Supported top-level keys are: {', '.join(list(combined.keys()))}

"""
                raise ValidationError(f"\n{error_message}")

            if "applications" in data:
                combined["applications"] = combined["applications"] | data["applications"]
            if "services" in data:
                combined["services"] = combined["services"] | data["services"]
            if "routes" in data:
                combined["routes"] = combined["routes"] | data["routes"]

        if combined["routes"] == {}:
            del combined["routes"]
        if combined["services"] == {}:
            del combined["services"]

        return _validate_config(combined)
    else:
        return ["✔ No errors found. YAML is valid.\n"]


def _check_data_types(config):
    """
    Verify data types match expected schema types before validation
    
    Args:
        config (dict): Parsed YAML configuration
        
    Raises:
        ValidationError: If data types don't match expected schema types
    """
    if not isinstance(config, dict):
        raise ValidationError("Configuration must be a dictionary/object")
    
    # Check root level properties
    if 'applications' in config:
        if not isinstance(config['applications'], dict):
            raise ValidationError("'applications' must be an object/dictionary")
            
    if 'services' in config:
        if not isinstance(config['services'], dict):
            raise ValidationError("'services' must be an object/dictionary")
            
    if 'routes' in config:
        if not isinstance(config['routes'], dict):
            raise ValidationError("'routes' must be an object/dictionary")
    
    # Check applications section more deeply
    if 'applications' in config and isinstance(config['applications'], dict):
        for app_name, app_config in config['applications'].items():
            if not isinstance(app_config, dict):
                raise ValidationError(f"Application '{app_name}' must be an object/dictionary")
            
            # Check critical application properties
            if 'type' in app_config and not isinstance(app_config['type'], str):
                raise ValidationError(f"Application '{app_name}' type must be a string")
                
            if 'resources' in app_config and app_config['resources'] is not None:
                if not isinstance(app_config['resources'], dict):
                    raise ValidationError(f"Application '{app_name}' resources must be an object/dictionary")
                
                if 'base_memory' in app_config['resources'] and not isinstance(app_config['resources']['base_memory'], int):
                    raise ValidationError(f"Application '{app_name}' base_memory must be an integer")
    
    # Check services section more deeply
    if 'services' in config and isinstance(config['services'], dict):
        for service_name, service_config in config['services'].items():
            if not isinstance(service_config, dict):
                raise ValidationError(f"Service '{service_name}' must be an object/dictionary")
            
            # Check critical service properties
            if 'type' in service_config and not isinstance(service_config['type'], str):
                raise ValidationError(f"Service '{service_name}' type must be a string")

def _check_for_local_mounts(config):
    """
    Check for 'local' mount sources that are deprecated but still supported for backward compatibility
    
    Args:
        config (dict): Parsed YAML configuration
        
    Raises:
        ValidationError: If 'local' mount source is found
    """
    if 'applications' in config and isinstance(config['applications'], dict):
        for app_name, app_config in config['applications'].items():
            if isinstance(app_config, dict) and 'mounts' in app_config and isinstance(app_config['mounts'], dict):
                for mount_path, mount_config in app_config['mounts'].items():
                    if isinstance(mount_config, dict) and 'source' in mount_config and mount_config['source'] == 'local':
                        error_message = f"""
✘ Backward compatibility issue found in application '{app_name}' mount '{mount_path}':

  'local' is a deprecated mount source type from Platform.sh. While Upsun still accepts it 
  for backward compatibility, it is not recommended for new configurations.
  
  Please replace 'source: local' with 'source: storage' in your mount configuration:
  
  applications:
    {app_name}:
      mounts:
        '{mount_path}':
          source: storage  # <-- Change from 'local' to 'storage'
          source_path: "{mount_config.get('source_path', 'data')}"
          
  This will ensure your configuration is compatible with current Upsun standards.
"""
                        raise ValidationError(error_message)

def _validate_config(config):
    """
    Internal function to validate the Upsun config structure
    
    Args:
        config (dict): Parsed YAML configuration
        
    Returns:
        list: List of validation results or error messages
    """
    # First check for required fields
    if 'applications' not in config:
        raise ValidationError("Missing required property: 'applications'")
    
    # Check for invalid top-level properties
    invalid_props = []
    for prop in config:
        if prop not in ["applications", "services", "routes"]:
            invalid_props.append(prop)
    
    if invalid_props:
        props_list = ", ".join(f"'{prop}'" for prop in invalid_props)
        raise ValidationError(f"Additional properties are not allowed: {props_list}")
    
    # Validate data types before schema validation
    _check_data_types(config)
    
    # Check for 'local' mount sources (deprecated but supported for backward compatibility)
    _check_for_local_mounts(config)
    
    # Validate against schema to catch structural issues early
    try:
        validate(instance=config, schema=UPSUN_SCHEMA)
    except ValidationError as e:
        # Enhance the error message to make it more clear
        error_message = str(e)
        
        # Special handling for 'local' mount source validation errors
        if "local" in error_message and "source" in error_message and "'local' is not one of" in error_message and "enum" in error_message:
            # Extract details from error message
            mount_path = "unknown"
            app_name = "unknown"
            
            # Try to extract mount path and app name from error message
            import re
            match = re.search(r"On instance\['applications'\]\['([^']+)'\]\['mounts'\]\['([^']+)'\]", error_message)
            if match:
                app_name = match.group(1)
                mount_path = match.group(2)
            
            custom_message = f"""
✘ Backward compatibility issue detected in application '{app_name}' mount '{mount_path}':

  'local' is a deprecated mount source type from Platform.sh. While Upsun still accepts it 
  for backward compatibility, it is not recommended for new configurations.
  
  Please replace 'source: local' with 'source: storage' in your mount configuration:
  
  applications:
    {app_name}:
      mounts:
        '{mount_path}':
          source: storage  # <-- Change from 'local' to 'storage'
          source_path: "data"  # <-- Use your actual source_path here
          
  This will ensure your configuration is compatible with current Upsun standards.
"""
            raise ValidationError(custom_message)
        
        # Make additionalProperties errors more explicit
        if "additionalProperties" in error_message:
            raise ValidationError(f"Schema validation error: Additional properties not allowed - {error_message}")
            
        # Enhance type errors to make them more obvious
        if "is not of type" in error_message:
            raise ValidationError(f"Schema validation error: Type mismatch - {error_message}")
            
        # Enhance required field errors
        if "required property" in error_message:
            raise ValidationError(f"Schema validation error: Missing required field - {error_message}")
            
        # Pass through other validation errors
        raise e
    
    # Now perform detailed validations for specific components
    if 'applications' in config:
        for app_name, app_config in config['applications'].items():
            # Check required fields for applications
            if not isinstance(app_config, dict):
                raise ValidationError(f"Application '{app_name}' must be an object/dictionary")
                
            # Each application must have either type or stack
            if 'type' not in app_config and 'stack' not in app_config:
                raise ValidationError(f"Application '{app_name}' is missing required property: either 'type' or 'stack'")
            
            if 'type' in app_config:
                if not isinstance(app_config['type'], str):
                    raise ValidationError(f"Application '{app_name}' type must be a string")
                    
                # Validate the 'type' schema.
                is_valid, error_message = validate_service_schema(app_config['type'], app_name, "runtime")
                if not is_valid:
                    raise ValidationError(f"\n\n✘ Error found in application '{app_name}'{error_message}")
                # Validate the type.
                is_valid, error_message = validate_service_type(app_config['type'], app_name, "runtime")
                if not is_valid:
                    raise ValidationError(f"\n\n✘ Error found in application '{app_name}':{error_message}")
                # Validate the runtime versions.
                is_valid, error_message = validate_service_version(app_config['type'], app_name, "runtime")
                if not is_valid:
                    raise ValidationError(f"\n\n✘ Error found in application '{app_name}':{error_message}")
                # Validate PHP extensions if defined.
                if "php" in app_config["type"]:
                    php_version = app_config["type"].split(":")[1]
                    if "runtime" in app_config:
                        if ( "extensions" in app_config["runtime"] ) or ( "disabled_extensions" in app_config["runtime"] ):
                            is_valid, error_message = validate_php_extensions(app_config["runtime"], php_version, app_name)
                            if not is_valid:
                                raise ValidationError(f"\n\n✘ Error found in application '{app_name}':{error_message}")

    if 'services' in config:
        for service_name, service_config in config['services'].items():
            # Check required fields for services
            if not isinstance(service_config, dict):
                raise ValidationError(f"Service '{service_name}' must be an object/dictionary")
                
            if 'type' not in service_config:
                raise ValidationError(f"Service '{service_name}' is missing required property: 'type'")
                
            if 'type' in service_config:
                if not isinstance(service_config['type'], str):
                    raise ValidationError(f"Service '{service_name}' type must be a string")
                    
                # Validate the schema.
                is_valid, error_message = validate_service_schema(service_config['type'], service_name, "service")
                if not is_valid:
                    raise ValidationError(f"\n\n✘ Error found in service '{service_name}':{error_message}")
                # Validate the type.
                is_valid, error_message = validate_service_type(service_config['type'], service_name, "service")
                if not is_valid:
                    raise ValidationError(f"\n\n✘ Error found in service '{service_name}':{error_message}")
                # Validate the service versions.
                is_valid, error_message = validate_service_version(service_config['type'], service_name, "service")
                if not is_valid:
                    raise ValidationError(f"\n\n✘ Error found in service '{service_name}':{error_message}")

    return ["✔ No errors found. YAML is valid.\n"]
