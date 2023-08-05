#!/usr/bin/env python3
import click

__version__ = "0.1.0"


from bazaar_cli import mw_list
from bazaar_cli import mw_dl
from bazaar_cli import mw_info


@click.group(invoke_without_command=True)
@click.pass_context
@click.option("-v", "--version", is_flag=True, help="print version")
@click.option("-d", "--docs", is_flag=True, help="access documentation")
def main(ctx, version, docs) -> int:
    if version:
        print(f"Bazaar CLI version {__version__}")
        print("~matteyeux")
    elif docs:
        click.launch("https://google.com")
    elif ctx.invoked_subcommand is None:
        click.echo(main.get_help(ctx))
    return 0


main.add_command(mw_list.main)
main.add_command(mw_dl.main)
main.add_command(mw_info.main)


if __name__ == "__main__":
    main()
