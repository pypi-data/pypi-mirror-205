import datetime
from dataclasses import dataclass
from typing import Self

import httpx
from dateutil.parser import parse


@dataclass
class SimpleResponseHeaders:
    content_type: str
    etag: str | None
    last_modified: datetime.datetime | None
    last_checked: datetime.datetime | None

    @classmethod
    def from_raw_headers(cls, data: httpx.Headers) -> Self | None:
        if (pagetype := data.get("content-type")) and "text/html" in pagetype:
            checked = data.get("date")
            modified = data.get("last-modified")
            return cls(
                content_type=data["content-type"],
                etag=data.get("etag", None),
                last_modified=parse(modified) if modified else None,
                last_checked=parse(checked) if checked else None,
            )
        return None
