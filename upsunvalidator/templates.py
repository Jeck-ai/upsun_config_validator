"""Provides access to example Upsun configuration templates."""

import os
import pathlib
from typing import Dict, List, Optional, Tuple


def _get_valid_templates_dir() -> pathlib.Path:
    """Return the path to the valid templates directory."""
    # Find the directory where the tests/valid templates are located
    module_path = pathlib.Path(__file__).parent
    return module_path / "tests" / "valid"


def get_available_template_names() -> List[str]:
    """
    Return a list of available template names.
    
    Returns:
        List[str]: A list of available template names (e.g., 'wordpress-vanilla', 'drupal11', etc.)
    """
    templates_dir = _get_valid_templates_dir()
    if not templates_dir.exists():
        return []
    
    # Get all directories that contain .upsun/config.yaml
    template_names = []
    for item in templates_dir.iterdir():
        if item.is_dir() and (item / ".upsun" / "config.yaml").exists():
            template_names.append(item.name)
    
    return sorted(template_names)


def get_template_config(template_name: str) -> Optional[str]:
    """
    Return the content of a template's config.yaml file.
    
    Args:
        template_name (str): The name of the template (e.g., 'wordpress-vanilla')
    
    Returns:
        Optional[str]: The content of the template's config.yaml file, or None if not found
    """
    templates_dir = _get_valid_templates_dir()
    config_path = templates_dir / template_name / ".upsun" / "config.yaml"
    
    if not config_path.exists():
        return None
    
    with open(config_path, "r") as f:
        return f.read()


def get_template_config_with_info() -> Dict[str, Tuple[str, Optional[str]]]:
    """
    Return a dictionary with template names as keys and tuples of (description, config content) as values.
    
    This function is useful for LLMs that need to select an appropriate template based on a description.
    
    Returns:
        Dict[str, Tuple[str, Optional[str]]]: A dictionary mapping template names to tuples of 
        (description, config content)
    """
    template_names = get_available_template_names()
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
    
    for name in template_names:
        description = descriptions.get(name, f"{name.replace('-', ' ').title()} template")
        content = get_template_config(name)
        result[name] = (description, content)
    
    return result
