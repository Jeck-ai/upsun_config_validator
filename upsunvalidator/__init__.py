"""Validation library for Upsun Configuration."""

__version__ = '0.2.3'

from upsunvalidator.__main__ import validate, validate_string
from upsunvalidator.templates import (
    get_available_template_names,
    get_template_config,
    get_template_config_with_info,
)
