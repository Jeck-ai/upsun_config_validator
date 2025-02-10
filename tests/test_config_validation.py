import os
import pytest
from validator import validate_upsun_config

# Get the current directory (tests folder)
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
PASSING_DIR = os.path.join(TESTS_DIR, 'passing_configs')
FAILING_DIR = os.path.join(TESTS_DIR, 'failing_configs')

def load_yaml_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def get_yaml_files(directory):
    yaml_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.yaml'):
                yaml_files.append(os.path.join(root, file))
    return yaml_files

def check_push_output(output):
    error_indicators = [
        "invalid configuration files",
        "failed to push",
        "configuration error",
        "validation failed"
    ]
    return not any(indicator in output.lower() for indicator in error_indicators)

@pytest.mark.parametrize("filepath", get_yaml_files(PASSING_DIR))
def test_valid_configs(filepath):
    yaml_content = load_yaml_file(filepath)
    errors = validate_upsun_config(yaml_content)
    
    assert errors == ["No errors found. YAML is valid."], \
        f"Expected valid but got errors in {filepath}: {errors}"

    try:
        with open("/Users/robert/jeck/upsun_config_validator/logs/upsun.log", "r") as log_file:
            log_content = log_file.read()
            assert check_push_output(log_content), \
                f"Upsun push failed for {filepath}"
    except FileNotFoundError:
        pytest.skip("Upsun log file not found - skipping push validation")

@pytest.mark.parametrize("filepath", get_yaml_files(FAILING_DIR))
def test_invalid_configs(filepath):
    yaml_content = load_yaml_file(filepath)
    errors = validate_upsun_config(yaml_content)
    
    assert errors and any(
        err.startswith(("Schema validation error:", "YAML parsing error:")) 
        for err in errors
    ), f"Expected errors in {filepath} but got: {errors}"

def test_empty_config():
    errors = validate_upsun_config("")
    assert "YAML parsing error: Empty configuration" in errors

def test_invalid_yaml_syntax():
    invalid_yaml = """
    applications:
      myapp:
        type: 'nodejs@14'
        web:
          - this is invalid yaml
          syntax: [
    """
    errors = validate_upsun_config(invalid_yaml)
    assert any("YAML parsing error:" in err for err in errors)

def test_missing_required_fields():
    yaml_content = """
    services:
      database:
        type: 'mariadb:10.4'
    """
    errors = validate_upsun_config(yaml_content)
    assert any("'applications' is a required property" in err for err in errors)

def test_invalid_version_format():
    yaml_content = """
    applications:
      myapp:
        type: 'nodejs@invalid'
    """
    errors = validate_upsun_config(yaml_content)
    assert any("does not match pattern" in err for err in errors)