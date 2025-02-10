# tests/test_config_validation.py
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

# Collect all YAML files from a directory.
def get_yaml_files(directory):
    return [
        os.path.join(directory, fname)
        for fname in os.listdir(directory)
        if fname.endswith('.yaml')
    ]

@pytest.mark.parametrize("filepath", get_yaml_files(PASSING_DIR))
def test_valid_configs(filepath):
    yaml_content = load_yaml_file(filepath)
    errors = validate_upsun_config(yaml_content)
    # Expect no errors if valid
    assert errors == ["No errors found. YAML is valid."], f"Expected valid but got errors in {filepath}: {errors}"

@pytest.mark.parametrize("filepath", get_yaml_files(FAILING_DIR))
def test_invalid_configs(filepath):
    yaml_content = load_yaml_file(filepath)
    errors = validate_upsun_config(yaml_content)
    # In our tests, we expect at least one error message that indicates a validation or YAML parsing error.
    assert any(err.startswith("Schema validation error:") or err.startswith("YAML parsing error:") for err in errors), \
        f"Expected errors in {filepath} but got none."