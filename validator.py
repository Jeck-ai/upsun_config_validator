import yaml
import re
from jsonschema import validate, ValidationError
from schema import validate_service_version
from schema import UPSUN_SCHEMA
from schema import PLATFORMSH_SCHEMA_APPS, PLATFORMSH_SCHEMA_ROUTES, PLATFORMSH_SCHEMA_SERVICES

def flatten_validation_error(error):
    error_path = " -> ".join(str(path) for path in error.path)
    return {
        'message': error.message,
        'path': error_path,
        'validator': error.validator,
        'validator_value': error.validator_value
    }

def validate_upsun_config(yaml_string):
    try:
        config = yaml.safe_load(yaml_string)
    except yaml.YAMLError as e:
        return [f"YAML parsing error: {e}"]
    
    if config is None:
        return ["YAML parsing error: Empty configuration"]
    
    try:
        # Custom service version validation
        if 'applications' in config:
            for app_name, app_config in config['applications'].items():
                if 'type' in app_config:
                    is_valid, error_message = validate_service_version(app_config['type'])
                    if not is_valid:
                        return [f"Schema validation error for application '{app_name}': {error_message}"]
        
        if 'services' in config:
            for service_name, service_config in config['services'].items():
                if 'type' in service_config:
                    is_valid, error_message = validate_service_version(service_config['type'])
                    if not is_valid:
                        return [f"Schema validation error for service '{service_name}': {error_message}"]

        validate(instance=config, schema=UPSUN_SCHEMA)
        return ["No errors found. YAML is valid."]
    except ValidationError as e:
        errors = []

        if e.context:
            for error in sorted(e.context, key=lambda e: e.path):
                detailed_error = flatten_validation_error(error)
                errors.append(f"Schema validation error: {detailed_error['message']} (at {detailed_error['path']})")
        else:
            errors.append(f"Schema validation error: [{".".join(e.absolute_path)}] {e.message}")
        return errors

def validate_platformsh_config(yaml_app_string, yaml_routes_string, yaml_services_string):
    try:
        configApp = yaml.safe_load(yaml_app_string)
        configRoutes = yaml.safe_load(yaml_routes_string)
        configServices = yaml.safe_load(yaml_services_string)
    except yaml.YAMLError as e:
        return [f"YAML parsing error: {e}"]
    
    if configApp is None:
        return ["YAML parsing error: No applications defined in configuration"]
    
    # @todo: there are many ways to define applications. 
    # 1) a single applications.yaml file in root (with an array of apps, or multiple app keys under an applications top-level key), 
    # 2) a .platform.app.yaml file in root. 
    # 3) multiple .platform.app.yaml files in many subdirs.

    try:
        # Custom service version validation
        if 'applications' in configApp:
            for app_name, app_config in config['applications'].items():
                if 'type' in app_config:
                    is_valid, error_message = validate_service_version(app_config['type'])
                    if not is_valid:
                        return [f"Schema validation error for application '{app_name}': {error_message}"]
        else:
            if 'type' in configApp:
                is_valid, error_message = validate_service_version(configApp['type'])
                if not is_valid:
                    return [f"Schema validation error for application: {error_message}"]

        validate(instance=configApp, schema=PLATFORMSH_SCHEMA_APPS)

        if configRoutes is not None:
            validate(instance=configRoutes, schema=PLATFORMSH_SCHEMA_ROUTES)

        if configServices is not None:

            for service_name, service_config in configServices.items():
                if 'type' in service_config:
                    is_valid, error_message = validate_service_version(service_config['type'])
                    if not is_valid:
                        return [f"Schema validation error for service '{service_name}': {error_message}"]

            validate(instance=configServices, schema=PLATFORMSH_SCHEMA_SERVICES)

        return ["No errors found. YAML is valid."]
    except ValidationError as e:
        errors = []
        if e.context:
            for error in sorted(e.context, key=lambda e: e.path):
                detailed_error = flatten_validation_error(error)
                errors.append(f"Schema validation error: {detailed_error['message']} (at {detailed_error['path']})")
        else:
            errors.append(f"Schema validation error: [{".".join(e.absolute_path)}] {e.message}")
        return errors
