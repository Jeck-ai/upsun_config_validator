import yaml
import jsonschema
from jsonschema import validate
from schema import UPSUN_SCHEMA

def validate_upsun_config(yaml_string):
    """
    Validates the provided YAML string against the JSON schema for .upsun/config.yaml.
    Returns a list of errors if found.
    """
    try:
        config = yaml.safe_load(yaml_string)
    except yaml.YAMLError as e:
        return [f"YAML parsing error: {e}"]
    
    try:
        validate(instance=config, schema=UPSUN_SCHEMA)
        return ["No errors found. YAML is valid."]
    except jsonschema.exceptions.ValidationError as e:
        return [f"Schema validation error: {e.message}"]

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
