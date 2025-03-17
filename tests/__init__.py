import os 
import pathlib

# Get the current directory (tests folder)
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))

# Invalid tests directory
FAILING_DIR = os.path.join(TESTS_DIR, 'invalid')

# Valid tests directory
PASSING_DIR = pathlib.Path(__file__).parent.parent / "upsunvalidator" / "examples"
