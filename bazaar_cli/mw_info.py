import click
from click_default_group import DefaultGroup

from bazaar_cli.bazaarwrapper import Bazaar
from bazaar_cli.common import get_api_key


@click.group(name="info", cls=DefaultGroup, default="hash", default_if_no_args=True)
def main():
    """Sample info."""


def pretty(d, indent=0):
    for key, value in d.items():
        print("\t" * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print("\t" * (indent + 1) + str(value))


@main.command("hash")
@click.argument("sample_hash", type=click.STRING, required=True)
def sample_info(sample_hash: str):
    """Download sample by hash."""
    if len(sample_hash) != 64:
        print("[!] Hash size mismatch")
        return

    api_key = get_api_key()
    bz = Bazaar(api_key)
    print(bz.sample_info(sample_hash))
