import re
from dataclasses import dataclass, field, fields
from http import HTTPStatus
from urllib.parse import urlparse

from start_sdk import Github

gh = Github()


REPO_PATTERN = re.compile(r"^\/(?P<author>.*)\/(?P<repo>.*)$")
REPO_FIELDS = [
    "created_at",
    "updated_at",
    "pushed_at",
    "stargazers_count",
    "description",
]


@dataclass
class Topic:
    name: str


@dataclass
class Owner:
    login: str
    avatar_url: str
    gravatar_id: str

    @classmethod
    def from_github_data(cls, data: dict):
        if (own := data.get("owner")) and isinstance(own, dict):
            keys = [k.name for k in fields(cls)]
            return cls(**{k: v for k, v in own.items() if k in keys})
        return None


@dataclass
class GithubRepo:
    """Requires a private access token (PAT) from Github Developer Settings."""

    author: str
    repo: str
    key: str | None = None
    owner: Owner | None = None
    topics: list[Topic] = field(default_factory=list)
    columns: dict = field(default_factory=dict)

    def __post_init__(self):
        data = self.get_data(author=self.author, repo=self.repo)
        self.key = data.get("license") and data["license"].get("key")
        self.owner = Owner.from_github_data(data)
        self.topics = [Topic(name=name) for name in data.get("topics")]
        self.columns = {k: v for k, v in data.items() if k in REPO_FIELDS}

    @classmethod
    def get_data(cls, author: str, repo: str):
        res = gh.get_repo(author=author, repo=repo)
        if res.status_code != HTTPStatus.OK:
            raise Exception(f"Fail github: {author=} {repo=}")
        return res.json()

    @classmethod
    def matches(cls, url: str) -> dict | None:
        p = urlparse(url)
        if p.netloc == "github.com" and p.path and p.path != "/":
            if match := REPO_PATTERN.search(p.path):
                return match.groupdict()
        return None

    @classmethod
    def from_url(cls, url: str):
        return cls(**d) if (d := cls.matches(url)) else None
