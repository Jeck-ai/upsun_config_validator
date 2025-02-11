import yaml
import re
from jsonschema import validate, ValidationError
from schema import UPSUN_SCHEMA, ALLOWED_VERSIONS

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