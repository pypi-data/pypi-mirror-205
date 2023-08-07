from dataclasses import asdict, dataclass
from http import HTTPStatus

import httpx
from bs4 import BeautifulSoup

from .headers import SimpleResponseHeaders
from .meta import SimpleMeta
from .repo import GithubRepo
from .url import ParsedURL


@dataclass
class InspectedURL:
    url: str
    head: httpx.Headers | None = None
    content: bytes | None = None

    def __post_init__(self):
        r = httpx.get(self.url, follow_redirects=True)
        if not r.status_code == HTTPStatus.OK:
            raise Exception(f"Bad {self.url}: {r.status_code}")
        self.head = r.headers
        self.content = r.content

    def prep(self, dc) -> dict:
        """Must be a dataclass."""
        return {dc.__class__.__name__: asdict(dc)} if dc is not None else {}

    @property
    def site_url(self) -> ParsedURL:
        """Generates the parts of urlparse.ParsedResult as a dictionary."""
        return ParsedURL.from_url(url=self.url)

    @property
    def site_headers(self) -> SimpleResponseHeaders | None:
        """Selected HTML headers, requires content-type to include `text/html`."""
        if self.head:
            return SimpleResponseHeaders.from_raw_headers(data=self.head)

    @property
    def site_meta(self) -> SimpleMeta | None:
        """Simplified summary of meta tags."""
        if self.content:
            html_soup = BeautifulSoup(self.content, "html.parser")
            return SimpleMeta.from_soup(html_soup)

    @property
    def repo_meta(self) -> GithubRepo | None:
        """Usable fields from Github repository, requires Github token."""
        if raw_data := GithubRepo.matches(self.url):
            return GithubRepo(**raw_data)

    @property
    def export(self):
        """Combine url, header, meta, repo key-value pairs."""
        data = self.prep(self.site_url)
        head = self.prep(self.site_headers) or {}
        meta = self.prep(self.site_meta) or {}
        repo = self.prep(self.repo_meta) or {}
        return data | head | meta | repo
