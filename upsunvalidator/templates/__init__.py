from typing import Dict, List, Optional, Tuple

from upsunvalidator.examples import (

    get_available_example_names,
    get_example_config,
    get_example_config_with_info,

)

def get_available_template_names() -> List[str]:
    """
    DEPRECATED: 

    Use `get_available_example_names` instead.

    Return a list of available example names.
    
    Returns:
        List[str]: A list of available example names (e.g., 'wordpress-vanilla', 'drupal11', etc.)
    """
    
    return get_available_example_names() 

def get_template_config(example_name: str) -> Optional[str]:
    """
    DEPRECATED: 

    Use `get_example_config` instead.

    Return the content of a example's config.yaml file.
    
    Args:
        example_name (str): The name of the example (e.g., 'wordpress-vanilla')
    
    Returns:
        Optional[str]: The content of the example's config.yaml file, or None if not found
    """
    return get_example_config(example_name)

def get_template_config_with_info() -> Dict[str, Tuple[str, Optional[str]]]:
    """
    DEPRECATED: 

    Use `get_example_config_with_info` instead.

    Return a dictionary with example names as keys and tuples of (description, config content) as values.
    
    This function is useful for LLMs that need to select an appropriate example based on a description.
    
    Returns:
        Dict[str, Tuple[str, Optional[str]]]: A dictionary mapping example names to tuples of 
        (description, config content)
    """
    return get_example_config_with_info()
