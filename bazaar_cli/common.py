import os

from tabulate import tabulate


def print_table(sample_list: list, header: tuple, fmt: str = "simple"):
    print(tabulate(sample_list, headers=header, tablefmt=fmt))


def get_api_key() -> str:
    """Get MB API key."""

    api_key = os.environ.get("MB_API_KEY", None)

    if api_key is None:
        raise Exception("MB_API_KEY not set as an envionment variable")

    return api_key
