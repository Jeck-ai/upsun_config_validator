import yaml
import re
from jsonschema import validate, ValidationError
from schema import UPSUN_SCHEMA, ALLOWED_VERSIONS

def validate_version(type_str):
    try:
        runtime, version = type_str.split('@' if '@' in type_str else ':')
        if runtime not in ALLOWED_VERSIONS:
            return True
        major_version = version.split('.')[0]
        for allowed_version in ALLOWED_VERSIONS[runtime]:
            if major_version == allowed_version.split('.')[0]:
                return True
        return False
    except ValueError:
        return False

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
    
    errors = []
    
    for app_name, app in config.get('applications', {}).items():
        if 'type' in app and not validate_version(app['type']):
            errors.append(f"Schema validation error: Invalid version in application {app_name}: {app['type']}")
    
    try:
        validate(instance=config, schema=UPSUN_SCHEMA)
        if not errors:
            return ["No errors found. YAML is valid."]
        return errors
    except ValidationError as e:
        if e.context:
            for error in sorted(e.context, key=lambda e: e.path):
                detailed_error = flatten_validation_error(error)
                errors.append(f"Schema validation error: {detailed_error['message']} (at {detailed_error['path']})")
        else:
            errors.append(f"Schema validation error: {e.message}")
        return errors