"""Test the templates module."""

import pytest
from upsunvalidator.templates import (
    get_available_template_names,
    get_template_config,
    get_template_config_with_info,
)


def test_get_available_template_names():
    """Test that get_available_template_names returns a non-empty list."""
    names = get_available_template_names()
    assert isinstance(names, list)
    assert len(names) > 0
    # Check for some known templates
    assert "wordpress-vanilla" in names
    assert "drupal11" in names


def test_get_template_config():
    """Test that get_template_config returns a non-empty string for a valid template."""
    config = get_template_config("wordpress-vanilla")
    assert isinstance(config, str)
    assert len(config) > 0
    assert "applications:" in config
    
    # Test for a non-existent template
    config = get_template_config("non-existent")
    assert config is None


def test_get_template_config_with_info():
    """Test that get_template_config_with_info returns a dictionary with descriptions and configs."""
    info = get_template_config_with_info()
    assert isinstance(info, dict)
    assert len(info) > 0
    
    # Check wordpress-vanilla entry
    assert "wordpress-vanilla" in info
    description, config = info["wordpress-vanilla"]
    assert isinstance(description, str)
    assert "WordPress" in description
    assert isinstance(config, str)
    assert "applications:" in config
