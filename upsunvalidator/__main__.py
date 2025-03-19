
# from upsunvalidator.validate.validate import validate

# if __name__ == '__main__':
#     # Simple example usage
#     success, message = validate()
#     print(message)

import os
import click

import upsunvalidator

from upsunvalidator.utils.utils import get_yaml_files
from upsunvalidator.utils.utils import load_yaml_file

from upsunvalidator.validate.validate import validate_all 
from upsunvalidator.validate.upsun import validate_upsun_config
from upsunvalidator.validate.upsun import validate_upsun_config_string

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
@click.option("--file", help="Location of a particular file you'd like to validate", type=str)
@click.option("--string", help="File contents (string) to validate.", type=str)
def validate(src, file, string):
    """Validate a project's configuration files against PaaS schemas.
    
    Example:

        # Validate a directory

        upsunvalidator validate --src $(pwd)

        # Validate a file

        upsunvalidator validate --file $(pwd)/.upsun/config.yaml

        # Validate string contents
        
        FILE_CONTENTS=$(cat .upsun/config.yaml)

        upsunvalidator validate --string $FILE_CONTENTS
    """

    if not string and not file and not src:
        # If no arguments are passed, assume we are validating the current directory, where `.upsun` is in root.
        src = os.getcwd()
        yaml_files = get_yaml_files(src, recursive=False)
        if "upsun" in yaml_files:
            results = validate_upsun_config(yaml_files)
            print(results[0])
        else:
            print(f"\n✘ No Upsun configuration files found in {src}.\n\n  Exiting.\n")

    # only `src` is provided.
    elif src and not string and not file:
        yaml_files = get_yaml_files(src, recursive=False)
        if "upsun" in yaml_files:
            results = validate_upsun_config(yaml_files)
            print(results[0])
        else:
            print(f"\n✘ No Upsun configuration files found in {src}.\n\n  Exiting.\n")

    # only `file` is provided.
    elif file and not string and not src:
        yaml_contents = load_yaml_file(file)
        results = validate_upsun_config_string(yaml_contents)
        print(results[0])

    # only `string` is provided.
    elif string and not file and not src:
        results = validate_upsun_config_string(string)
        print(results[0])

cli.add_command(validate)

if __name__ == '__main__':
    cli()
