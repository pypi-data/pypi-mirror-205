from dataclasses import asdict, dataclass
from http import HTTPStatus
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

from .headers import HTMLHeaders
from .meta import SimplifiedMeta


@dataclass
class InspectedURL:
    url: str
    head: httpx.Headers
    content: bytes

    def __post_init__(self):
        r = httpx.get(self.url, follow_redirects=True)
        if not r.status_code == HTTPStatus.OK:
            raise Exception(f"Bad {self.url}: {r.status_code}")
        self.head = r.headers
        self.content = r.content

    def prep(self, obj) -> dict:
        return asdict(obj) if obj is not None else {}

    @property
    def url_data(self) -> dict:
        """Generates the parts of urlparse.ParsedResult as a dictionary."""
        parsed = urlparse(self.url)
        return {k: getattr(parsed, k) for k in parsed._fields}

    @property
    def site_headers(self) -> HTMLHeaders | None:
        """Selected HTML headers, requires content-type to include `text/html`."""
        return HTMLHeaders.from_raw_headers(data=self.head)

    @property
    def site_meta(self) -> SimplifiedMeta | None:
        """Simplified summary of meta tags."""
        html_soup = BeautifulSoup(self.content, "html.parser")
        return SimplifiedMeta.from_soup(html_soup)

    @property
    def export(self):
        """Combines url, header, meta info into a single dictionary."""
        url = self.url_data
        head = self.prep(self.site_headers) or {}
        meta = self.prep(self.site_meta) or {}
        return url | head | meta
