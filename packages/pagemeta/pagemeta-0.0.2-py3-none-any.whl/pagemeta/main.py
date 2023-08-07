from dataclasses import asdict, dataclass
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

from .headers import SiteHeaders
from .meta import PageMeta


@dataclass
class InspectedURL:
    url: str
    headers: SiteHeaders | None = None
    meta: PageMeta | None = None

    def __post_init__(self):
        r = httpx.get(self.url, follow_redirects=True)
        self.headers = SiteHeaders.from_raw_headers(data=r.headers)
        self.meta = PageMeta.from_soup(BeautifulSoup(r.content, "html.parser"))

    def prep(self, obj) -> dict:
        return asdict(obj) if obj is not None else {}

    @property
    def url_data(self) -> dict:
        parsed = urlparse(self.url)
        return {k: getattr(parsed, k) for k in parsed._fields}

    @property
    def export(self):
        return self.url_data | self.prep(self.headers) | self.prep(self.meta)
