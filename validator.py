import yaml
import re
from jsonschema import validate, ValidationError
from schema import UPSUN_SCHEMA, validate_runtime_version

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
        # Custom runtime version validation
        if 'applications' in config:
            for app_name, app_config in config['applications'].items():
                if 'type' in app_config:
                    is_valid, error_message = validate_runtime_version(app_config['type'])
                    if not is_valid:
                        return [f"Schema validation error for application '{app_name}': {error_message}"]
        
        validate(instance=config, schema=UPSUN_SCHEMA)
        return ["No errors found. YAML is valid."]
    except ValidationError as e:
        errors = []
        if e.context:
            for error in sorted(e.context, key=lambda e: e.path):
                detailed_error = flatten_validation_error(error)
                errors.append(f"Schema validation error: {detailed_error['message']} (at {detailed_error['path']})")
        else:
            errors.append(f"Schema validation error: {e.message}")
        return errors