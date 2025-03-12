import yaml
import pytest

from upsunvalidator.utils.utils import get_yaml_files
from upsunvalidator.utils.utils import load_yaml_file
from upsunvalidator.utils.utils import get_all_projects_in_directory

from upsunvalidator.validate.upsun import validate_upsun_config
from upsunvalidator.validate.platformsh import validate_platformsh_config
from upsunvalidator.validate.errors import ValidationError

from .shared import INVALID_TOP_LEVEL_KEYS_DIR

@pytest.mark.parametrize("current_template", get_all_projects_in_directory(INVALID_TOP_LEVEL_KEYS_DIR, "files"))
def test_invalid_upsun_topleval_keys(current_template):
    yaml_files = get_yaml_files(current_template)

    if "upsun" in yaml_files:
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
            
            with pytest.raises(ValidationError, match=msg):
                validate_upsun_config(yaml_files)

