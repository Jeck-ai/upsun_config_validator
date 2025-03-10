import click

from upsunvalidator.utils.utils import get_yaml_files

from upsunvalidator.validate.validate import validate_all 
from upsunvalidator.validate.platformsh import validate_platformsh_config
from upsunvalidator.validate.upsun import validate_upsun_config

from upsunvalidator.utils.utils import make_bold_text

@click.group()
def cli():
    pass

@cli.command()
@click.option("--src", default="root", help="Repository location you'd like to validate.")
@click.option("--provider", default="all", help="PaaS provider you'd like to validate against.")
def validate(src, provider):

    yaml_files = get_yaml_files(src)

    if provider == "all":
        validate_all(src)
    
    valid_providers = [
        "upsun", 
        "platformsh"
    ]

    if provider in valid_providers:
        if provider == "upsun":
            print(make_bold_text("Validating for Upsun..."))
            results = validate_upsun_config(yaml_files)
        elif provider == "platformsh":
            print("\nValidating for Platform.sh...\n")
            results = validate_platformsh_config(yaml_files)
    else:
        results = ["Choose a valid provider: upsun, platformsh"]

    print(results[0])

@cli.command 
def generate(**args):
    print("Coming soon...") 

cli.add_command(validate)
cli.add_command(generate)

if __name__ == '__main__':
    cli()





# Valid
# @todo: there's no output right now.
# pipenv run python -m upsunvalidator validate --src tests/valid/shopware/files --provider upsun

# Invalid
# pipenv run python -m upsunvalidator validate --src tests/invalid_runtime_versions/nodejs/files --provider upsun
# pipenv run python -m upsunvalidator validate --src tests/invalid_service_versions/mariadb/files --provider upsun
# pipenv run python -m upsunvalidator validate --src tests/invalid_enable_php_extensions/invalid_enable/files --provider upsun

# # pyinstaller --onefile --paths /Users/chadwcarlson/.local/share/virtualenvs/upsun_config_validator-xybjvp6i/lib/python3.13 upsunvalidator/__main__.py -n upsunvalidator
# % ./dist/upsunvalidator --src tests/invalid_service_versions/mariadb/files --provider upsun                                      
# ModuleNotFoundError: No module named 'jsonschema'
# [PYI-16617:ERROR] Failed to execute script '__main__' due to unhandled exception!