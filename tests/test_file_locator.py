import os
import yaml
import pytest

from upsunvalidator.utils.utils import get_yaml_files
from upsunvalidator.utils.utils import get_all_projects_in_directory

# Get the current directory (tests folder)
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))

# Valid tests.
PASSING_DIR = os.path.join(TESTS_DIR, 'valid')

# Failing tests.
INVALID_RUNTIME_VERSION_DIR = os.path.join(TESTS_DIR, 'invalid_runtime_versions')
INVALID_SERVICE_VERSION_DIR = os.path.join(TESTS_DIR, 'invalid_service_versions')
INVALID_ENABLE_PHP_EXTENSIONS_DIR = os.path.join(TESTS_DIR, 'invalid_enable_php_extensions')

@pytest.mark.parametrize("current_template", get_all_projects_in_directory(PASSING_DIR, "files"))
def test_valid_provider_configfile_count(current_template):
    """
    Confirms that the tool is finding the expected number of configuration files across the various possible combinations of Upsun, Platform.sh, and combined configuration.
    """

    # skip_exceptions are valid templates that have different expected numbers of config files. 
    skip_exceptions = ["shopware", "gatsby-wordpress"]
    template = current_template.split("/")[-2]
    yaml_files = get_yaml_files(current_template)

    # Most cases.
    if template not in skip_exceptions:
        # The files we expect to find.
        expected_files = {
            "upsun": [
                os.path.join(PASSING_DIR, f"{template}/files/.upsun/config.yaml")
            ],
            "platformsh": [
                os.path.join(PASSING_DIR, f"{template}/files/.platform.app.yaml"),
                os.path.join(PASSING_DIR, f"{template}/files/.platform/services.yaml"),
                os.path.join(PASSING_DIR, f"{template}/files/.platform/routes.yaml")
            ]
        }
        # We expect certain providers to be found (upsun/platformsh).
        assert yaml_files.keys() == expected_files.keys(), f"Expected keys {expected_files.keys()} but got {yaml_files.keys()}"
        # We expect certain numbers of files for each provider.
        assert len(yaml_files["upsun"]) == len(expected_files["upsun"]), f"Expected {len(expected_files["upsun"])} configuration yaml files but got {len(yaml_files["upsun"])}."
        assert len(yaml_files["platformsh"]) == len(expected_files["platformsh"]), f"Expected {len(expected_files["platformsh"])} configuration yaml files but got {len(yaml_files["platformsh"])}."
        # We expect specific file names for these providers.
        assert sorted(yaml_files["upsun"]) == sorted(expected_files["upsun"]), f"Expected yaml files {expected_files["upsun"]} but got {yaml_files["upsun"]}"
        assert sorted(yaml_files["platformsh"]) == sorted(expected_files["platformsh"]), f"Expected yaml files {expected_files["platformsh"]} but got {yaml_files["platformsh"]}"
    
    # Special case: Shopware.
    elif template == "shopware":
        # The files we expect to find.
        expected_files = {
            "upsun": [
                os.path.join(PASSING_DIR, f"{template}/files/.upsun/config.yaml")
            ],
            "platformsh": [
                os.path.join(PASSING_DIR, f"{template}/files/.platform/applications.yaml"),
                os.path.join(PASSING_DIR, f"{template}/files/.platform/services.yaml"),
                os.path.join(PASSING_DIR, f"{template}/files/.platform/routes.yaml")
            ]
        }
        # We expect certain providers to be found (upsun/platformsh).
        assert yaml_files.keys() == expected_files.keys(), f"Expected keys {expected_files.keys()} but got {yaml_files.keys()}"
        # We expect certain numbers of files for each provider.
        assert len(yaml_files["upsun"]) == len(expected_files["upsun"]), f"Expected {len(expected_files["upsun"])} configuration yaml files but got {len(yaml_files["upsun"])}."
        assert len(yaml_files["platformsh"]) == len(expected_files["platformsh"]), f"Expected {len(expected_files["platformsh"])} configuration yaml files but got {len(yaml_files["platformsh"])}."
        # We expect specific file names for these providers.
        assert sorted(yaml_files["upsun"]) == sorted(expected_files["upsun"]), f"Expected yaml files {expected_files["upsun"]} but got {yaml_files["upsun"]}"
        assert sorted(yaml_files["platformsh"]) == sorted(expected_files["platformsh"]), f"Expected yaml files {expected_files["platformsh"]} but got {yaml_files["platformsh"]}"
    # Special case: Gastby + WordPress multi-app.
    elif template == "gatsby-wordpress":
        # The files we expect to find.
        expected_files = {
            "upsun": [
                os.path.join(PASSING_DIR, f"{template}/files/.upsun/config.yaml")
            ],
            "platformsh": [
                os.path.join(PASSING_DIR, f"{template}/files/.platform/services.yaml"),
                os.path.join(PASSING_DIR, f"{template}/files/.platform/routes.yaml"),
                os.path.join(PASSING_DIR, f"{template}/files/gatsby/.platform.app.yaml"),
                os.path.join(PASSING_DIR, f"{template}/files/wordpress/.platform.app.yaml")
            ]
        }
        # We expect certain providers to be found (upsun/platformsh).
        assert yaml_files.keys() == expected_files.keys(), f"Expected keys {expected_files.keys()} but got {yaml_files.keys()}"
        # We expect certain numbers of files for each provider.
        assert len(yaml_files["upsun"]) == len(expected_files["upsun"]), f"Expected {len(expected_files["upsun"])} configuration yaml files but got {len(yaml_files["upsun"])}."
        assert len(yaml_files["platformsh"]) == len(expected_files["platformsh"]), f"Expected {len(expected_files["platformsh"])} configuration yaml files but got {len(yaml_files["platformsh"])}."
        # We expect specific file names for these providers.
        assert sorted(yaml_files["upsun"]) == sorted(expected_files["upsun"]), f"Expected yaml files {expected_files["upsun"]} but got {yaml_files["upsun"]}"
        assert sorted(yaml_files["platformsh"]) == sorted(expected_files["platformsh"]), f"Expected yaml files {expected_files["platformsh"]} but got {yaml_files["platformsh"]}"
