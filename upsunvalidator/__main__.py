import click

from upsunvalidator.utils.utils import get_yaml_files

from upsunvalidator.validate.validate import validate_all 
from upsunvalidator.validate.platformsh import validate_platformsh_config
from upsunvalidator.validate.upsun import validate_upsun_config

from upsunvalidator.utils.utils import make_bold_text


class Config:
    """The config in this example only holds aliases."""

    def __init__(self):
        self.path = os.getcwd()
        self.aliases = {}

    def add_alias(self, alias, cmd):
        self.aliases.update({alias: cmd})

    def read_config(self, filename):
        parser = configparser.RawConfigParser()
        parser.read([filename])
        try:
            self.aliases.update(parser.items("aliases"))
        except configparser.NoSectionError:
            pass

    def write_config(self, filename):
        parser = configparser.RawConfigParser()
        parser.add_section("aliases")
        for key, value in self.aliases.items():
            parser.set("aliases", key, value)
        with open(filename, "wb") as file:
            parser.write(file)


pass_config = click.make_pass_decorator(Config, ensure=True)


class AliasedGroup(click.Group):
    """This subclass of a group supports looking up aliases in a config
    file and with a bit of magic.
    """

    def get_command(self, ctx, cmd_name):
        # Step one: bulitin commands as normal
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv

        # Step two: find the config object and ensure it's there.  This
        # will create the config object is missing.
        cfg = ctx.ensure_object(Config)

        # Step three: look up an explicit command alias in the config
        if cmd_name in cfg.aliases:
            actual_cmd = cfg.aliases[cmd_name]
            return click.Group.get_command(self, ctx, actual_cmd)

        # Alternative option: if we did not find an explicit alias we
        # allow automatic abbreviation of the command.  "status" for
        # instance will match "st".  We only allow that however if
        # there is only one command.
        matches = [
            x for x in self.list_commands(ctx) if x.lower().startswith(cmd_name.lower())
        ]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail(f"Too many matches: {', '.join(sorted(matches))}")

    def resolve_command(self, ctx, args):
        # always return the command's name, not the alias
        _, cmd, args = super().resolve_command(ctx, args)
        return cmd.name, cmd, args


def read_config(ctx, param, value):
    """Callback that is used whenever --config is passed.  We use this to
    always load the correct config.  This means that the config is loaded
    even if the group itself never executes so our aliases stay always
    available.
    """
    cfg = ctx.ensure_object(Config)
    if value is None:
        value = os.path.join(os.path.dirname(__file__), "aliases.ini")
    cfg.read_config(value)
    return value

@click.command(cls=AliasedGroup)
# @click.option(
#     "--config",
#     type=click.Path(exists=True, dir_okay=False),
#     callback=read_config,
#     expose_value=False,
#     help="The config file to use instead of the default.",
# )
def cli():
    """Helper library for producing and ensuring valid Upsun & Platform.sh PaaS configuration against their schemas.
    
    Tip: you can use this CLI directly (`upsunvalidator`) or through the alias (`uv`).
    """


@cli.command()
@click.option("--src", help="Repository location you'd like to validate.", type=str)
@click.option("--provider", help="PaaS provider you'd like to validate against.", type=str)
def validate(src, provider):
    """Validate a project's configuration files against PaaS schemas.
    
    Example:

    upsunvalidator validate --src $(pwd) --provider upsun
    
    or 

    uv validate --src $(pwd) --provider upsun
    """
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
    """Generate configuration files for a given PaaS.
    
    This command is currently being developed.
    """
    print("Coming soon...") 

cli.add_command(validate)
cli.add_command(generate)

if __name__ == '__main__':
    cli()



# While developing, add the `pipenv run python -m` prefix to all of the below commands:

# # Valid
# upsunvalidator validate --src tests/valid/shopware/files --provider upsun

# # Invalid
# upsunvalidator validate --src tests/invalid_runtime_versions/nodejs/files --provider upsun
# upsunvalidator validate --src tests/invalid_service_versions/mariadb/files --provider upsun
# upsunvalidator validate --src tests/invalid_enable_php_extensions/php/files --provider upsun
