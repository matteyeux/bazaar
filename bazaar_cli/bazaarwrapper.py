import os
from enum import Enum
from typing import Union
import requests

MB_API = "https://mb-api.abuse.ch/api/v1/"


class QueryType(Enum):
    TAG = "get_taginfo"
    SIG = "get_siginfo"
    FILE_TYPE = "get_file_type"
    RECENT = "get_recent"
    FILE_INFO = "get_info"


class Bazaar:
    """MalwareBazaar wrapper class."""

    def __init__(self, api_key: str = ""):
        if not api_key:
            raise Exception("No API key specified")

        self.api_key = api_key
        self.headers = {"Auth-Key": self.api_key}

    def __repr__(self):
        return "<bazaar.bazaarwrapper.Bazaar(api_key='{}')>".format(self.api_key)

    def _query(
        self,
        url: str,
        method="GET",
        raw: bool = False,
        data=None,
        params=None,
    ) -> Union[dict, requests.Response]:
        """Perform a request using the `self._req` HTTP client.
        Upon requesting a non-standard URL (not returning JSON),
        the `raw` flag allow to return a `requests.Response` object
        instead of a dictionnary.
        """
        response = requests.request(
            method,
            url,
            data=data,
            headers=self.headers,
            timeout=50,
        )
        if raw:
            return response
        return response.json()

    def list_samples(self, query_type: QueryType, key: str, limit: int = 50) -> dict:
        """Currently only lists by tags."""

        match query_type:
            case QueryType.TAG:
                key_type = "tag"
            case QueryType.SIG:
                key_type = "signature"
            case QueryType.FILE_TYPE:
                key_type = "file_type"
            case QueryType.RECENT:
                key_type = "selector"
            case _:
                key_type = "tag"

        samples = self._query(
            MB_API,
            "POST",
            data={"query": query_type.value, key_type: key, "limit": limit},
        )

        if samples.get("data", {}) == {}:  # type: ignore
            return samples.get("query_status")

        return samples

    def download_sample(self, sample_hash: str, outdir: str = "") -> None:
        """Download a sample by its hash."""
        if len(sample_hash) != 64:
            raise Exception("Hash is not recognized")

        if outdir != "" and not outdir.endswith("/"):
            outdir += "/"

        sample = self._query(
            MB_API,
            "POST",
            data={"query": "get_file", "sha256_hash": sample_hash},
            raw=True,
        ).content

        if sample == b'{\n    "query_status": "file_not_found"\n}':
            raise Exception("File not found")

        if outdir != "":
            if os.path.isdir(outdir) is False:
                os.mkdir(outdir)

        open(f"{outdir}{sample_hash}.zip", "wb").write(sample)

    def sample_info(self, sample_hash) -> dict:
        """Get sample hash info."""
        sample = self._query(
            MB_API,
            "POST",
            data={"query": QueryType.FILE_INFO.value, "hash": sample_hash},
        )

        return sample
