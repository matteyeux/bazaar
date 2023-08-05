import click
from click_default_group import DefaultGroup

from bazaar_cli.bazaarwrapper import Bazaar
from bazaar_cli.bazaarwrapper import QueryType
from bazaar_cli.common import get_api_key
from bazaar_cli.common import print_table


@click.group(
    name="list", cls=DefaultGroup, default="latest-samples", default_if_no_args=True
)
def main():
    """List samples."""


@main.command("latest-samples")
def do_list_latest() -> None:
    """List latest malware samples."""
    do_list(QueryType.RECENT, "100")


@main.command(name="tag")
@click.argument("tag", type=click.STRING, required=True)
def list_tag(tag: str) -> None:
    """List samples by tag."""
    do_list(QueryType.TAG, tag)


@main.command(name="sig")
@click.argument("signature", type=click.STRING, required=True)
@click.option("-l", "--limit", help="limit")
def list_signature(signature: str, limit: int = 50) -> None:
    """List samples by signature."""
    do_list(QueryType.SIG, signature, limit)


@main.command(name="type")
@click.argument("file_type", type=click.STRING, required=True)
@click.option("-l", "--limit", help="limit")
def list_type(file_type: str, limit: int = 50) -> None:
    """List samples by file_type."""
    do_list(QueryType.FILE_TYPE, file_type, limit)


def do_list(query_type: QueryType, value: str, limit: int = 50) -> None:
    """List."""
    api_key = get_api_key()
    bz = Bazaar(api_key)
    header = ("Date", "SHA256", "Type", "Signature", "Tags", "Reporter")
    samples = bz.list_samples(query_type, value, limit)
    if not isinstance(samples, dict):
        print(samples)
        return

    sample_list = []
    for sample in samples["data"]:
        if sample["tags"] is not None:
            tags = ", ".join(sample["tags"])
        else:
            tags = None
        sample_list.append(
            [
                sample["first_seen"],
                sample["sha256_hash"],
                sample["file_type"],
                sample["signature"],
                tags,
                sample["reporter"],
            ]
        )
    print_table(sample_list, header)
