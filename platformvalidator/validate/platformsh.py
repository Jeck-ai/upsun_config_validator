import yaml

from jsonschema import validate, ValidationError

from platformvalidator.schemas.platformsh import PLATFORMSH_SCHEMA_APPS, PLATFORMSH_SCHEMA_ROUTES, PLATFORMSH_SCHEMA_SERVICES

from platformvalidator.utils.utils import load_yaml_file, flatten_validation_error
from platformvalidator.validate.services import validate_service_version
from platformvalidator.validate.extensions import validate_php_extensions


def validate_platformsh_config(yaml_files):
    try:
        if "platformsh" in yaml_files:

            configApp = None
            configRoutes = None
            configServices = None

            for file in yaml_files["platformsh"]:
                yaml_content = load_yaml_file(file)
                data = yaml.safe_load(yaml_content)
                if data is not None:
                    if ("name" in data) or ("applications" in data) or ((isinstance(data, list)) and ("name" in data[0])):
                        configApp = data
                    elif ("https://{default}/" in data) or ("https://{default}" in data):
                        configRoutes = data
                    else:
                        configServices = data

        else:
            return ["No Platform.sh configuration found."]

    except yaml.YAMLError as e:
        return [f"YAML parsing error: {e}"]
    
    try:
        if configApp is not None:
            # Custom service version validation
            if 'applications' in configApp:
                for app_name, app_config in configApp['applications'].items():
                    if 'type' in app_config:
                        is_valid, error_message = validate_service_version(app_config['type'])
                        if not is_valid:
                            return [f"Schema validation error for application '{app_name}': {error_message}"]
                        else:
                            validate(instance=app_config, schema=PLATFORMSH_SCHEMA_APPS)
                            return ["No errors found. YAML is valid."]

            elif 'type' in configApp:
                is_valid, error_message = validate_service_version(configApp['type'])
                if not is_valid:
                    return ["Schema validation error for application: {0}".format(error_message)]
                else:
                    validate(instance=configApp, schema=PLATFORMSH_SCHEMA_APPS)
                    return ["No errors found. YAML is valid."]
                
            elif isinstance(configApp, list):
                for app_config in configApp:
                    if 'type' in app_config:
                        is_valid, error_message = validate_service_version(app_config['type'])
                        if not is_valid:
                            return [f"Schema validation error for application: {error_message}"]     
                        else:
                            validate(instance=app_config, schema=PLATFORMSH_SCHEMA_APPS)
                            return ["No errors found. YAML is valid."]

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
