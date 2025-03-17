import pytest
import os
import pathlib

from upsunvalidator import validate_string
from upsunvalidator.utils.utils import load_yaml_file

from upsunvalidator.examples import (
    get_available_example_names,
    get_example_config,
    get_example_config_with_info,
)

# Valid tests directory (examples)
from . import PASSING_DIR

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
def test_valid_upsun_examples(config_path):
    """Test that all .upsun/config.yaml files are valid when validated as strings."""
    yaml_content = load_yaml_file(config_path)
    is_valid, message = validate_string(yaml_content)
    assert is_valid, f"Expected valid but got error: {message} for file {config_path}"
    assert "✔ No errors found. YAML is valid" in message

def test_get_available_example_names():
    """Test that get_available_example_names returns a non-empty list."""
    names = get_available_example_names()
    assert isinstance(names, list)
    assert len(names) > 0
    # Check for some known examples
    assert "wordpress-vanilla" in names
    assert "drupal11" in names


def test_get_example_config():
    """Test that get_example_config returns a non-empty string for a valid example."""
    config = get_example_config("wordpress-vanilla")
    assert isinstance(config, str)
    assert len(config) > 0
    assert "applications:" in config
    
    # Test for a non-existent example
    config = get_example_config("non-existent")
    assert config is None


def test_get_example_config_with_info():
    """Test that get_example_config_with_info returns a dictionary with descriptions and configs."""
    info = get_example_config_with_info()
    assert isinstance(info, dict)
    assert len(info) > 0
    
    # Check wordpress-vanilla entry
    assert "wordpress-vanilla" in info
    description, config = info["wordpress-vanilla"]
    assert isinstance(description, str)
    assert "WordPress" in description
    assert isinstance(config, str)
    assert "applications:" in config
