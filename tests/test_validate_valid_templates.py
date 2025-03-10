import pytest

from upsunvalidator.utils.utils import get_yaml_files
from upsunvalidator.utils.utils import get_all_projects_in_directory

from upsunvalidator.validate.upsun import validate_upsun_config
from upsunvalidator.validate.platformsh import validate_platformsh_config

from .shared import PASSING_DIR

@pytest.mark.parametrize("current_template", get_all_projects_in_directory(PASSING_DIR, "files"))
def test_valid_upsun_templates(current_template):
    yaml_files = get_yaml_files(current_template)
    if "upsun" in yaml_files:
        errors = validate_upsun_config(yaml_files)
        assert errors == ["✔ No errors found. YAML is valid.\n"], \
            f"Expected valid but got errors in {yaml_files['upsun'][0]}"

# @pytest.mark.parametrize("current_template", get_all_projects_in_directory(PASSING_DIR, "files"))
# def test_valid_platformsh_templates(current_template):
#     yaml_files = get_yaml_files(current_template)
#     if "platformsh" in yaml_files:
#         errors = validate_platformsh_config(yaml_files)
#         assert errors == ["✔ No errors found. YAML is valid.\n"], \
#             f"Expected valid but got errors in {yaml_files['upsun'][0]}"
