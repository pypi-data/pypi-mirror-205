from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass
class ParsedURL:
    scheme: str
    netloc: str
    path: str | None = None
    params: str | None = None
    query: str | None = None
    fragment: str | None = None

    @classmethod
    def from_url(cls, url: str):
        p = urlparse(url)
        return cls(
            scheme=p.scheme,
            netloc=p.netloc,
            path=p.path.removeprefix("/").removesuffix("/") or None,
            params=p.params or None,
            query=p.query or None,
            fragment=p.fragment or None,
        )
