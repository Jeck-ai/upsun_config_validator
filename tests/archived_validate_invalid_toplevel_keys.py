import yaml
import pytest

from upsunvalidator.utils.utils import get_yaml_files
from upsunvalidator.utils.utils import load_yaml_file
from upsunvalidator.utils.utils import get_all_projects_in_directory

from upsunvalidator.validate.upsun import validate_upsun_config
# from upsunvalidator.validate.platformsh import validate_platformsh_config
from upsunvalidator.validate.errors import ValidationError

# from ruamel.yaml.constructor import DuplicateKeyError

from .shared import INVALID_TOP_LEVEL_KEYS_DIR

@pytest.mark.parametrize("current_template", get_all_projects_in_directory(INVALID_TOP_LEVEL_KEYS_DIR, "files"))
def test_invalid_upsun_topleval_keys(current_template):
    yaml_files = get_yaml_files(current_template)

    if "upsun" in yaml_files:

        # Ensure no top-level keys are included except those in `valid_keys` below.
        if "invalid_key" in yaml_files["upsun"][0]:
            service = current_template.split("/")[-2]
            data = yaml.safe_load(load_yaml_file(yaml_files["upsun"][0]))
            invalid_keys = ["another_random_key", "another_another_random_key"]
            valid_keys = ["applications", "services", "routes"]

            msg = f"""
✘ Error found in configuration file {yaml_files["upsun"][0]}.

  '{"', '".join(invalid_keys)}' are not valid top-level keys.

  Supported top-level keys are: {', '.join(valid_keys)}

"""
            # with pytest.raises(ValidationError, match=msg):
            with pytest.raises(ValidationError):
                validate_upsun_config(yaml_files)

#         # Ensure no valid keys are duplicated within the same file.
#         if "duplicate_key" in yaml_files["upsun"][0]:
# #             config_snippet_a = "{\'db\': {\'type\': \'redis:6.2\'}}"
# #             config_snippet_b = "{\'db\': {\'type\': \'mariadb:10.4\'}}"
# #             msg = f"""while constructing a mapping
# #   in "{yaml_files["upsun"][0]}", line 1, column 1
# # found duplicate key "services" with value "{config_snippet_a}" (original value: "{config_snippet_b}"))
# #   in "{yaml_files["upsun"][0]}", line 18, column 1

# # To suppress this check see:
# #    http://yaml.readthedocs.io/en/latest/api.html#duplicate-keys
# # """
            
#             with pytest.raises(DuplicateKeyError):
#             # with pytest.raises(DuplicateKeyError, match=msg):
#                 validate_upsun_config(yaml_files)

