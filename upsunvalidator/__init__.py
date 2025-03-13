"""Validation library for Upsun Configuration."""

try:
    from upsunvalidator._version import version as __version__
except ImportError:
    __version__ = "0.0.0.dev0"  # Fallback version if not installed from git

from upsunvalidator.__main__ import validate, validate_string
from upsunvalidator.templates import (
    get_available_template_names,
    get_template_config,
    get_template_config_with_info,
)
