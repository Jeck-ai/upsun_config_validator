"""Provides access to example Upsun configuration examples."""

import os
import yaml
import pathlib
from typing import Dict, List, Optional, Tuple

from upsunvalidator.utils.utils import load_yaml_file

def _get_valid_examples_dir() -> pathlib.Path:
    """Return the path to the valid examples directory."""
    # Find the directory where the tests/valid examples are located
    module_path = pathlib.Path(__file__).parent
    return module_path


def get_available_example_names() -> List[str]:
    """
    Return a list of available example names.
    
    Returns:
        List[str]: A list of available example names (e.g., 'wordpress-vanilla', 'drupal11', etc.)
    """
    examples_dir = _get_valid_examples_dir()
    if not examples_dir.exists():
        return []
    
    # Get all directories that contain .upsun/config.yaml
    example_names = []
    for item in examples_dir.iterdir():
        if item.is_dir() and (item / ".upsun" / "config.yaml").exists():
            example_names.append(item.name)
    
    return sorted(example_names)


def get_example_config(example_name: str) -> Optional[str]:
    """
    Return the content of a example's config.yaml file.
    
    Args:
        example_name (str): The name of the example (e.g., 'wordpress-vanilla')
    
    Returns:
        Optional[str]: The content of the example's config.yaml file, or None if not found
    """
    examples_dir = _get_valid_examples_dir()
    config_path = examples_dir / example_name / ".upsun" / "config.yaml"
    
    if not config_path.exists():
        return None
    
    with open(config_path, "r") as f:
        return f.read()


def get_example_config_with_info() -> Dict[str, Tuple[str, Optional[str]]]:
    """
    Return a dictionary with example names as keys and tuples of (description, config content) as values.
    
    This function is useful for LLMs that need to select an appropriate example based on a description.
    
    Returns:
        Dict[str, Tuple[str, Optional[str]]]: A dictionary mapping example names to tuples of 
        (description, config content)
    """
    example_names = get_available_example_names()
    result = {}
    
    # Grab list of examples with decriptions from `meta.yaml` file
    desc_file = _get_valid_examples_dir() / "meta.yaml"
    try:
        descriptions = yaml.safe_load(load_yaml_file(desc_file))
    except yaml.YAMLError as e:
        return [f"YAML parsing error: {e}"]
    
    for name in example_names:
        description = descriptions.get(name, f"{name.replace('-', ' ').title()} example")
        content = get_example_config(name)
        result[name] = (description, content)
    
    return result


def get_example_info() -> Dict[str, Tuple[str, Optional[str]]]:
    """
    Return a dictionary with example names as keys and tuples of (description, config content) as values.
    
    This function is useful for LLMs that need to select an appropriate example based on a description.
    
    Returns:
        Dict[str, Tuple[str, Optional[str]]]: A dictionary mapping example names to tuples of 
        (description, config content)
    """
    example_names = get_available_example_names()
    result = {}

    # Grab list of examples with decriptions from `meta.yaml` file
    desc_file = _get_valid_examples_dir() / "meta.yaml"
    try:
        descriptions = yaml.safe_load(load_yaml_file(desc_file))
    except yaml.YAMLError as e:
        return [f"YAML parsing error: {e}"]
    
    for name in example_names:
        description = descriptions.get(name, f"{name.replace('-', ' ').title()} example")
        result[name] = description
    
    return result
