import click
import os
import pyzipper
from click_default_group import DefaultGroup

from bazaar_cli.bazaarwrapper import Bazaar, QueryType
from bazaar_cli.common import get_api_key


@click.group(name="download", cls=DefaultGroup, default="hash", default_if_no_args=True)
def main():
    """Download samples."""


@main.command("hash")
@click.argument("sample_hash", type=click.STRING, required=True)
@click.option("-u", "--unzip", is_flag=True, help="unzip malware sample")
@click.option("-k", "--keep-zip", is_flag=True, help="keep zip archive after unzip")
@click.option("-o", "--outdir", default="", help="output directory")
def download_hash(
    sample_hash: str, unzip: bool, keep_zip: bool = False, outdir: str = ""
):
    """Download sample by hash."""
    if len(sample_hash) != 64:
        print("[!] Hash size mismatch")
        return

    if outdir != "" and not outdir.endswith("/"):
        outdir += "/"

    api_key = get_api_key()
    bz = Bazaar(api_key)
    bz.download_sample(sample_hash, outdir)

    if unzip:
        do_unzip(f"{sample_hash}.zip", outdir)
        if not keep_zip:
            os.remove(f"{outdir}{sample_hash}.zip")


def do_unzip(zipfile: str, outdir: str = "") -> None:
    """Unzip with password."""
    with pyzipper.AESZipFile(f"{outdir}{zipfile}") as f:
        f.pwd = b"infected"
        filename = f.infolist()[0].filename
        content = f.read(f.infolist()[0].filename)
        open(f"{outdir}{filename}", "wb").write(content)


@main.command("sig")
@click.argument("signature", type=click.STRING, required=True)
@click.option("-u", "--unzip", is_flag=True, help="unzip malware sample")
@click.option("-k", "--keep-zip", is_flag=True, help="keep zip archive after unzip")
@click.option("-o", "--outdir", default="", help="output directory")
def download_sig(signature: str, unzip: bool, keep_zip: bool, outdir: str = ""):
    """Download sample by hash."""
    if outdir != "" and not outdir.endswith("/"):
        outdir += "/"
    print(outdir)
    api_key = get_api_key()
    bz = Bazaar(api_key)

    samples = bz.list_samples(QueryType.SIG, signature)

    for sample in samples["data"]:
        filename = sample["sha256_hash"]

        print(filename)

        bz.download_sample(filename, outdir)
        if unzip:
            do_unzip(f"{filename}.zip", outdir)
            if not keep_zip:
                os.remove(f"{outdir}{filename}.zip")
