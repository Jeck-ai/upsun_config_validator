"""Provides access to example Upsun configuration examples."""

import os
import pathlib
from typing import Dict, List, Optional, Tuple


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
    
    descriptions = {
        "wordpress-vanilla": "WordPress standard installation",
        "wordpress-bedrock": "WordPress using Bedrock project structure",
        "wordpress-composer": "WordPress with Composer-based management",
        "drupal11": "Drupal 11 CMS",
        "laravel": "Laravel PHP framework",
        "django4": "Django 4 Python web framework",
        "flask": "Flask Python microframework",
        "express": "Express.js Node.js web application framework",
        "nextjs": "Next.js React framework",
        "nuxtjs": "Nuxt.js Vue.js framework",
        "rails": "Ruby on Rails web application framework",
        "gatsby": "Gatsby static site generator",
        "gatsby-wordpress": "Gatsby with WordPress as a headless CMS",
        "fastapi": "FastAPI Python web framework",
        "shopware": "Shopware e-commerce platform",
        "strapi4": "Strapi v4 headless CMS",
        "akeneo": "Akeneo PIM (Product Information Management)",
        "directus": "Directus headless CMS",
        "magentoce": "Magento Community Edition e-commerce platform",
        "pimcore": "Pimcore digital experience platform",
        "pyramid": "Pyramid Python web framework",
        "sylius": "Sylius e-commerce platform",
        "typo3-v11": "TYPO3 v11 CMS",
        "wagtail": "Wagtail CMS built on Django",
    }
    
    for name in example_names:
        description = descriptions.get(name, f"{name.replace('-', ' ').title()} example")
        content = get_example_config(name)
        result[name] = (description, content)
    
    return result
