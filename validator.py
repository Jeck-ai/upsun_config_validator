import yaml
import jsonschema
from jsonschema import validate, ValidationError
from schema import UPSUN_SCHEMA

def flatten_validation_error(error):
    """
    Convert a complex validation error into a more readable format.
    """
    error_path = " -> ".join(str(path) for path in error.path)
    return {
        'message': error.message,
        'path': error_path,
        'validator': error.validator,
        'validator_value': error.validator_value
    }

def validate_upsun_config(yaml_string):
    """
    Validates the provided YAML string against the JSON schema for .upsun/config.yaml.
    Returns a list of detailed errors if found.
    """
    try:
        config = yaml.safe_load(yaml_string)
    except yaml.YAMLError as e:
        return [f"YAML parsing error: {e}"]
    
    # Handle None or empty config
    if config is None:
        return ["YAML parsing error: Empty configuration"]
    
    try:
        # Strict validation with all keyword checks
        validate(instance=config, schema=UPSUN_SCHEMA)
        return ["No errors found. YAML is valid."]
    except ValidationError as e:
        # More granular error handling
        all_errors = []
        for error in sorted(e.context, key=lambda e: e.path):
            detailed_error = flatten_validation_error(error)
            error_msg = f"Schema validation error: {detailed_error['message']} (at {detailed_error['path']})"
            if detailed_error['validator'] == 'pattern':
                error_msg += f" (expected format: {detailed_error['validator_value']})"
            all_errors.append(error_msg)
        
        return all_errors if all_errors else [f"Schema validation error: {e.message}"]

# Example usage:
if __name__ == "__main__":
    example_yaml = """
    applications:
      myapp:
        type: 'nodejs@22'
        web:
          commands:
            start: npm start
          locations:
            '/':
              root: 'public'
              passthru: true
              index: ["index.html"]
              allow: true
    services:
      database:
        type: 'mariadb:11.4'
        configuration:
          storage: 10GB
        relationships:
          app:
            service: 'myapp'
            endpoint: 'db-url'
    routes:
      "https://{default}/":
        type: upstream
        upstream: "myapp:http"
      "https://www.{default}/":
        type: redirect
        to: "https://{default}/"
    """
    
    errors = validate_upsun_config(example_yaml)
    for error in errors:
        print(error)
