import os
import pytest

from platformvalidator.utils.utils import get_yaml_files, load_yaml_file, get_all_projects_in_directory
from platformvalidator.validate.validate import validate_all
from platformvalidator.validate.upsun import validate_upsun_config
from platformvalidator.validate.platformsh import validate_platformsh_config

# Get the current directory (tests folder)
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
PASSING_DIR = os.path.join(TESTS_DIR, 'templates')

@pytest.mark.parametrize("current_template", get_all_projects_in_directory(PASSING_DIR, "files"))
def test_valid_provider_configfile_count(current_template):

    skip_exceptions = ["shopware"]
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

@pytest.mark.parametrize("current_template", get_all_projects_in_directory(PASSING_DIR, "files"))
def test_valid_upsun_templates(current_template):
    yaml_files = get_yaml_files(current_template)
    errors = validate_upsun_config(yaml_files)
    assert errors == ["No errors found. YAML is valid."], \
        f"Expected valid but got errors in {yaml_files['upsun'][0]}"

@pytest.mark.parametrize("current_template", get_all_projects_in_directory(PASSING_DIR, "files"))
def test_valid_platformsh_templates(current_template):
    print(current_template)
    yaml_files = get_yaml_files(current_template)
    errors = validate_platformsh_config(yaml_files)
    assert errors == ["No errors found. YAML is valid."], \
        f"Expected valid but got errors in {current_template}"

@pytest.mark.parametrize("current_template", get_all_projects_in_directory(PASSING_DIR, "files"))
def test_crossprovider_validation(current_template):
    errors = validate_all(current_template)
    assert errors == ["No errors found. YAML is valid."], \
        f"Expected valid but got errors in {current_template}"
