import os
import click

import upsunvalidator

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
def cli():
    """Helper library for producing and ensuring valid Upsun & Platform.sh PaaS configuration against their schemas.
    
    Tip: 
    
    You can use this CLI directly or through the alias (`upv`).
    """


@cli.command 
def version(**args):
    """Retrieve the current version of this tool."""
    print(upsunvalidator.__version__) 


@cli.command()
@click.option("--src", help="Repository location you'd like to validate.", type=str)
@click.option("--provider", default="all", help="PaaS provider you'd like to validate against. (all, upsun, platformsh)", type=str)
def validate(src, provider):
    """Validate a project's configuration files against PaaS schemas.
    
    Example:

        upsunvalidator validate --src $(pwd) --provider upsun

        upsunvalidator validate --src $(pwd) --provider platformsh
    
    or 

        upv validate --src $(pwd) --provider upsun

        upv validate --src $(pwd) --provider platformsh

    You can run against all providers if `--provider` is not passed

        upv validate --src $(pwd)

        upsunvalidator validate --src $(pwd)

    Alias: val
    """

    if not src:
        src = os.getcwd()

    yaml_files = get_yaml_files(src)

    valid_providers = [
        "upsun", 
        "platformsh"
    ]
    
    if provider == "all":
        print(make_bold_text("Validating for all providers..."))
        if yaml_files:
            print(make_bold_text("1. Validating for Upsun..."))
            results = validate_upsun_config(yaml_files)
            print(results[0])
            print(make_bold_text("2. Validating for Platform.sh..."))
            results = validate_platformsh_config(yaml_files)
            print(results[0])
        else:
            print("✘ No YAML files found. Exiting.\n")
    elif provider in valid_providers:
        if provider == "upsun" and "upsun" in yaml_files:
            print(make_bold_text("Validating for Upsun..."))
            results = validate_upsun_config(yaml_files)
            print(results[0])
        elif provider == "platformsh" and "platformsh" in yaml_files:
            print(make_bold_text("Validating for Platform.sh..."))
            results = validate_platformsh_config(yaml_files)
            print(results[0])
        elif not yaml_files:
            print("✘ No YAML files found. Exiting.\n")
    elif provider != "all":
        results = ["✘ Choose a valid provider: upsun, platformsh"]

        print(results[0])

cli.add_command(validate)

if __name__ == '__main__':
    cli()
