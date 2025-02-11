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
    
    assert errors, f"Expected errors in {filepath} but got no errors"
    assert any(
        "validation error" in err.lower() or 
        "invalid" in err.lower() or 
        "error" in err.lower()
        for err in errors
    ), f"Expected meaningful validation errors in {filepath}, but got: {errors}"

def test_invalid_runtime_format():
    # Test invalid runtime formats
    test_cases = [
        {
            "name": "Wrong separator",
            "yaml": """
            applications:
              myapp:
                type: 'nodejs@14'
            """,
            "expected_message": "invalid runtime"
        },
        {
            "name": "Unsupported runtime",
            "yaml": """
            applications:
              myapp:
                type: 'unknown:1.0'
            """,
            "expected_message": "unsupported runtime"
        },
        {
            "name": "Invalid version format",
            "yaml": """
            applications:
              myapp:
                type: 'nodejs:abc'
            """,
            "expected_message": "invalid version"
        }
    ]

    for case in test_cases:
        errors = validate_upsun_config(case["yaml"])
        assert errors, f"Case '{case['name']}' should have errors"
        assert any(
            case["expected_message"].lower() in err.lower() 
            for err in errors
        ), f"Case '{case['name']}' did not produce expected error message. Got: {errors}"

def test_empty_config():
    errors = validate_upsun_config("")
    assert "YAML parsing error" in errors[0].lower()

def test_invalid_yaml_syntax():
    invalid_yaml = """
    applications:
      myapp:
        type: 'nodejs:14'
        web:
          - this is invalid yaml
          syntax: [
    """
    errors = validate_upsun_config(invalid_yaml)
    assert "YAML parsing error" in errors[0].lower()