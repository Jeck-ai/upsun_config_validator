import pytest
import os

from upsunvalidator import validate_string
from upsunvalidator.utils.utils import load_yaml_file

# Get the current directory (tests folder)
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))

# Valid tests directory
PASSING_DIR = os.path.join(TESTS_DIR, 'valid')

def get_all_upsun_config_paths(directory):
    """Get all .upsun/config.yaml file paths."""
    result = []
    for root, dirs, files in os.walk(directory):
        if '.upsun' in dirs:
            config_path = os.path.join(root, '.upsun', 'config.yaml')
            if os.path.exists(config_path):
                result.append(config_path)
    return result

@pytest.mark.parametrize("config_path", get_all_upsun_config_paths(PASSING_DIR))
def test_valid_upsun_templates(config_path):
    """Test that all .upsun/config.yaml files are valid when validated as strings."""
    yaml_content = load_yaml_file(config_path)
    is_valid, message = validate_string(yaml_content)
    assert is_valid, f"Expected valid but got error: {message} for file {config_path}"
    assert "✔ No errors found. YAML is valid" in message
