import yaml

from jsonschema import validate, ValidationError

from platformvalidator.schemas.upsun import UPSUN_SCHEMA

from platformvalidator.utils.utils import load_yaml_file, flatten_validation_error
from platformvalidator.validate.services import validate_service_version
from platformvalidator.validate.extensions import validate_php_extensions


def validate_upsun_config(yaml_files):
    try:
        if "upsun" in yaml_files:
            config = yaml.safe_load(load_yaml_file(yaml_files["upsun"][0]))
        else:
            return ["No Upsun configuration found."]
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

                    if "php" in app_config["type"]:
                        php_version = app_config["type"].split(":")[1]
                        if "runtime" in app_config:
                            if ( "extensions" in app_config["runtime"] ) or ( "disabled_extensions" in app_config["runtime"] ):
                                is_valid, error_message = validate_php_extensions(app_config["runtime"], php_version)
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
