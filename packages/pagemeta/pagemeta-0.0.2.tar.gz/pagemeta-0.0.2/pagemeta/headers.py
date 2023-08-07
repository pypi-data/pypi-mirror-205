import datetime
from dataclasses import dataclass
from typing import Self

import httpx
from dateutil.parser import parse


@dataclass
class SiteHeaders:
    content_type: str
    etag: str
    last_modified: datetime.datetime
    date: datetime.datetime

    @classmethod
    def from_raw_headers(cls, data: httpx.Headers) -> Self:
        return cls(
            content_type=data["content-type"],
            etag=data["etag"],
            last_modified=parse(data["last-modified"]),
            date=parse(data["date"]),
        )
