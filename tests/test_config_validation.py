import os
import yaml
import itertools

import pytest
import unittest
from upsunvalidator.validate.errors import ValidationError, InvalidServiceVersionError, InvalidPHPExtensionError

# import sys
# sys.tracebacklimit=0

from upsunvalidator.schemas.services import SERVICE_VERSIONS
from upsunvalidator.schemas.extensions import PHP_EXTENSIONS

from upsunvalidator.utils.utils import get_yaml_files, load_yaml_file, get_all_projects_in_directory
from upsunvalidator.validate.validate import validate_all
from upsunvalidator.validate.upsun import validate_upsun_config
from upsunvalidator.validate.platformsh import validate_platformsh_config

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

    skip_exceptions = ["shopware", "gatsby-wordpress"]
    template = current_template.split("/")[-2]
    yaml_files = get_yaml_files(current_template)

    if template not in skip_exceptions:
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

        assert yaml_files.keys() == expected_files.keys(), f"Expected keys {expected_files.keys()} but got {yaml_files.keys()}"
        assert len(yaml_files["upsun"]) == len(expected_files["upsun"]), f"Expected {len(expected_files["upsun"])} configuration yaml files but got {len(yaml_files["upsun"])}."
        assert len(yaml_files["platformsh"]) == len(expected_files["platformsh"]), f"Expected {len(expected_files["platformsh"])} configuration yaml files but got {len(yaml_files["platformsh"])}."
        assert sorted(yaml_files["upsun"]) == sorted(expected_files["upsun"]), f"Expected yaml files {expected_files["upsun"]} but got {yaml_files["upsun"]}"
        assert sorted(yaml_files["platformsh"]) == sorted(expected_files["platformsh"]), f"Expected yaml files {expected_files["platformsh"]} but got {yaml_files["platformsh"]}"

    elif template == "shopware":
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

        assert yaml_files.keys() == expected_files.keys(), f"Expected keys {expected_files.keys()} but got {yaml_files.keys()}"
        assert len(yaml_files["upsun"]) == len(expected_files["upsun"]), f"Expected {len(expected_files["upsun"])} configuration yaml files but got {len(yaml_files["upsun"])}."
        assert len(yaml_files["platformsh"]) == len(expected_files["platformsh"]), f"Expected {len(expected_files["platformsh"])} configuration yaml files but got {len(yaml_files["platformsh"])}."
        assert sorted(yaml_files["upsun"]) == sorted(expected_files["upsun"]), f"Expected yaml files {expected_files["upsun"]} but got {yaml_files["upsun"]}"
        assert sorted(yaml_files["platformsh"]) == sorted(expected_files["platformsh"]), f"Expected yaml files {expected_files["platformsh"]} but got {yaml_files["platformsh"]}"

    elif template == "gatsby-wordpress":
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

        assert yaml_files.keys() == expected_files.keys(), f"Expected keys {expected_files.keys()} but got {yaml_files.keys()}"
        assert len(yaml_files["upsun"]) == len(expected_files["upsun"]), f"Expected {len(expected_files["upsun"])} configuration yaml files but got {len(yaml_files["upsun"])}."
        assert len(yaml_files["platformsh"]) == len(expected_files["platformsh"]), f"Expected {len(expected_files["platformsh"])} configuration yaml files but got {len(yaml_files["platformsh"])}."
        assert sorted(yaml_files["upsun"]) == sorted(expected_files["upsun"]), f"Expected yaml files {expected_files["upsun"]} but got {yaml_files["upsun"]}"
        assert sorted(yaml_files["platformsh"]) == sorted(expected_files["platformsh"]), f"Expected yaml files {expected_files["platformsh"]} but got {yaml_files["platformsh"]}"

@pytest.mark.parametrize("current_template", get_all_projects_in_directory(PASSING_DIR, "files"))
def test_valid_upsun_templates(current_template):
    yaml_files = get_yaml_files(current_template)
    if "upsun" in yaml_files:
        errors = validate_upsun_config(yaml_files)
        assert errors == ["✔ No errors found. YAML is valid."], \
            f"Expected valid but got errors in {yaml_files['upsun'][0]}"

@pytest.mark.parametrize("current_template", get_all_projects_in_directory(INVALID_RUNTIME_VERSION_DIR, "files"))
def test_invalid_runtime_versions(current_template):
    yaml_files = get_yaml_files(current_template)

    if "upsun" in yaml_files:
        service = current_template.split("/")[-2]
        data = yaml.safe_load(load_yaml_file(yaml_files["upsun"][0]))
        app_name = list(data["applications"].keys())[0]
        invalid_version = data["applications"][app_name]["type"].split(":")[1]
        msg = f"\nUpsun schema validation error for application '{app_name}'\n✘ Unsupported version '{invalid_version}' for runtime '{service}'. Allowed versions are: {', '.join(SERVICE_VERSIONS[service]["versions"])}\n"

        with pytest.raises(InvalidServiceVersionError, match=msg):
            validate_upsun_config(yaml_files)

@pytest.mark.parametrize("current_template", get_all_projects_in_directory(INVALID_SERVICE_VERSION_DIR, "files"))
def test_invalid_service_versions(current_template):
    yaml_files = get_yaml_files(current_template)

    if "upsun" in yaml_files:
        service = current_template.split("/")[-2]
        data = yaml.safe_load(load_yaml_file(yaml_files["upsun"][0]))
        service_name = list(data["services"].keys())[0]
        invalid_version = data["services"][service_name]["type"].split(":")[1]
        msg = f"\nUpsun schema validation error for service '{service_name}'\n✘ Unsupported version '{invalid_version}' for service '{service}'. Allowed versions are: {', '.join(SERVICE_VERSIONS[service]["versions"])}\n"

        with pytest.raises(InvalidServiceVersionError, match=msg):
            validate_upsun_config(yaml_files)

@pytest.mark.parametrize("current_template", get_all_projects_in_directory(INVALID_ENABLE_PHP_EXTENSIONS_DIR, "files"))
def test_invalid_enable_php_extensions(current_template):
    yaml_files = get_yaml_files(current_template)

    valid_extensions_key = "extensions"
    schema_valid_extensions_key = PHP_EXTENSIONS["valid"][valid_extensions_key]
    valid_disable_extensions_key = "disabled_extensions"
    schema_valid_disable_extensions_key = PHP_EXTENSIONS["valid"][valid_disable_extensions_key]
    invalid_disable_extensions_key = "built-in"
    schema_invalid_disable_extensions_key = PHP_EXTENSIONS["valid"][invalid_disable_extensions_key]
    with_webp_extensions_key = "with-webp"
    schema_with_webp_extensions_key = PHP_EXTENSIONS["valid"][with_webp_extensions_key]

    if "upsun" in yaml_files:
        data = yaml.safe_load(load_yaml_file(yaml_files["upsun"][0]))
        app_name = list(data["applications"].keys())[0]
        php_version = data["applications"][app_name]["type"].split(":")[1]

        # if schema_with_webp_extensions_key not in PHP_EXTENSIONS["extensions_by_version"][php_version]:
        #     PHP_EXTENSIONS["extensions_by_version"][php_version][schema_with_webp_extensions_key] = []

        invalid_extension = data["applications"][app_name]["runtime"]["extensions"][0]

        all_supported_extensions = list(itertools.chain(PHP_EXTENSIONS["extensions_by_version"][php_version][schema_valid_extensions_key],
            PHP_EXTENSIONS["extensions_by_version"][php_version][schema_invalid_disable_extensions_key],
            PHP_EXTENSIONS["extensions_by_version"][php_version][schema_valid_disable_extensions_key],
            PHP_EXTENSIONS["extensions_by_version"][php_version][schema_with_webp_extensions_key]) )
        msg = f"\nUpsun schema validation error for runtime '{app_name}'\n✘ Extension {invalid_extension} is not supported in PHP {php_version}. Supported extensions are: {', '.join(all_supported_extensions)}\n"

        with pytest.raises(InvalidPHPExtensionError, match=msg):
            validate_upsun_config(yaml_files)


# @pytest.mark.parametrize("current_template", get_all_projects_in_directory(PASSING_DIR, "files"))
# def test_valid_platformsh_templates(current_template):
#     yaml_files = get_yaml_files(current_template)
#     if "platformsh" in yaml_files:
#         errors = validate_platformsh_config(yaml_files)
#         assert errors == ["No errors found. YAML is valid."], \
#             f"Expected valid but got errors in {current_template}"

# @pytest.mark.parametrize("current_template", get_all_projects_in_directory(PASSING_DIR, "files"))
# def test_crossprovider_validation(current_template):
#     errors = validate_all(current_template)
#     for error in errors:
#         assert error == ["No errors found. YAML is valid."], \
#             f"Expected valid but got errors in {current_template}"