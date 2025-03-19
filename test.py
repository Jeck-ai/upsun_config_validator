import pathlib

from upsunvalidator import validate_string
from upsunvalidator.utils.utils import load_yaml_file

from upsunvalidator.examples import (
    get_available_example_names,
    get_example_config,
    get_example_config_with_info,
)

from upsunvalidator.validate.errors import ValidationError

import upsunvalidator.examples as uve


TEST_EXAMPLE = "directus"

testconfig = get_example_config(TEST_EXAMPLE)

print(validate_string(testconfig))

print(dir(uve))