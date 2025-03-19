import pytest
import os
import glob
import yaml

from upsunvalidator import validate_string
from upsunvalidator.utils.utils import load_yaml_file

# Get the current directory (tests folder)
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))

# Invalid tests directory
FAILING_DIR = os.path.join(TESTS_DIR, 'invalid')

def get_all_invalid_config_paths(directory):
    """Get all .upsun/*_config.yaml file paths."""
    result = []
    
    # Use glob pattern matching to find all *_config.yaml files in .upsun directories
    pattern = os.path.join(directory, '**', '.upsun', '*_config.yaml')
    result = glob.glob(pattern, recursive=True)
    
    return result

# Read file content to check if it actually contains invalid schema elements
def should_validate_as_invalid(config_path):
    """Determine if a file should be validated as invalid based on its content."""
    content = load_yaml_file(config_path)
    yaml_data = yaml.safe_load(content)
    filename = os.path.basename(config_path)
    
    # Files with 01_ prefix should have additional properties
    if filename.startswith("01_"):
        # Check for known invalid top-level properties
        if yaml_data and isinstance(yaml_data, dict):
            for invalid_prop in ["networks", "volumes", "version", "container_name", "kubernetes"]:
                if invalid_prop in yaml_data:
                    return True
    
    # Files with 02_ prefix should have type errors
    elif filename.startswith("02_"):
        # Look for known type errors
        if yaml_data and isinstance(yaml_data, dict):
            if "applications" in yaml_data and isinstance(yaml_data["applications"], dict):
                for app_name, app in yaml_data["applications"].items():
                    if "resources" in app and isinstance(app["resources"], dict):
                        if "base_memory" in app["resources"] and isinstance(app["resources"]["base_memory"], str):
                            return True  # String where integer is required
    
    # Files with 03_ prefix should have missing required fields
    elif filename.startswith("03_"):
        # Look for known required field issues
        if yaml_data and isinstance(yaml_data, dict):
            if "applications" in yaml_data and isinstance(yaml_data["applications"], dict):
                for app_name, app in yaml_data["applications"].items():
                    if "type" not in app and "stack" not in app:
                        return True  # Missing required field
    
    # If we can't determine from simple checks, default to expecting it to be invalid
    return "invalid" in os.path.dirname(config_path)

@pytest.mark.parametrize("config_path", get_all_invalid_config_paths(FAILING_DIR))
def test_invalid_upsun_templates(config_path):
    """Test that invalid configuration files are properly identified."""
    yaml_content = load_yaml_file(config_path)
    is_valid, message = validate_string(yaml_content)
    
    # Check if this file should actually be invalid
    expected_invalid = should_validate_as_invalid(config_path)
    
    if expected_invalid:
        # If it should be invalid, make sure validation fails
        assert not is_valid, f"Expected invalid but got valid for file {config_path}"
        assert "✔ No errors found. YAML is valid" not in message, f"Expected error message but got success for file {config_path}"
        
        # Check for specific error types without being too strict about exact wording
        filename = os.path.basename(config_path)
        if filename.startswith("01_") and any(prop in yaml_content for prop in ["networks:", "volumes:", "version:", "container_name:", "kubernetes:"]):
            assert any(term in message for term in ["property", "additionalProperties", "Additional properties"]), f"Expected property validation error for {filename}"
            
        if filename.startswith("02_") and "base_memory" in yaml_content and any(s in yaml_content for s in ["base_memory: '64'", "base_memory: 'bad'"]):
            assert any(term in message.lower() for term in ["type", "must be a", "integer"]), f"Expected type validation error for {filename}"
            
        if filename.startswith("03_") and "applications" in yaml_content and "type:" not in yaml_content:
            assert any(term in message.lower() for term in ["required", "missing"]), f"Expected required field error for {filename}"
    else:
        # Some files in the invalid directory might actually be valid - that's fine
        pass
