from dataclasses import dataclass
from typing import Iterable

from bs4 import BeautifulSoup

TITLE = (
    'meta[name="twitter:title"]',
    'meta[property="og:title"]',
    "title",
)
DESC = (
    'meta[name="twitter:description"]',
    'meta[property="og:description"]',
    'meta[name="description"]',
)
IMG = (
    'meta[name="twitter:image"]',
    'meta[property="og:image"]',
)
AUTHOR = (
    'meta[name="author"]',
    'meta[name="twitter:creator"]',
)
TYPE = ('meta[property="og:type"]',)


@dataclass
class PageMeta:
    """Extract generic website metadata based on a url fetched on a certain date.

    All of the fields, except the date, default to `None`.

    Field | Type | Description
    :--:|:--:|:--
    title | str | First matching title parsed from `<meta>` CSS selectors (and the `<title>` tag)
    description | str | First matching description Parsed from `<meta>` CSS selectors
    author | str | Either the author or the creator, if the author is absent
    image | str | An [open graph](https://ogp.me/) (OG) image url detected
    category | str | A type detected from OG ("og:type") values
    """  # noqa: E501

    title: str | None = None
    description: str | None = None
    author: str | None = None
    image: str | None = None
    category: str | None = None

    @classmethod
    def from_soup(cls, soup: BeautifulSoup):
        return cls(
            title=cls.select(soup, TITLE),
            description=cls.select(soup, DESC),
            author=cls.select(soup, AUTHOR),
            image=cls.select(soup, IMG),
            category=cls.select(soup, TYPE),
        )

    @classmethod
    def select(
        cls, soup: BeautifulSoup, selectors: Iterable[str]
    ) -> str | None:
        """The order of CSS selectors. The first one
        matched, retrieves the content, if found.

        See present list of selectors used to extract content:

        ```py
        TITLE = (
            'meta[name="twitter:title"]',
            'meta[property="og:title"]',
            "title",
        )
        DESC = (
            'meta[name="twitter:description"]',
            'meta[property="og:description"]',
            'meta[name="description"]',
        )
        IMG = (
            'meta[name="twitter:image"]',
            'meta[property="og:image"]',
        )
        AUTHOR = (
            'meta[name="author"]',
            'meta[name="twitter:creator"]',
        )
        TYPE = ('meta[property="og:type"]',)
        ```

        Note the special rule on `title` as a selector.

        Examples:
            >>> from pathlib import Path
            >>> html = Path(__file__).parent.parent / "tests" / "data" / "test.html"
            >>> soup = BeautifulSoup(html.read_text(), "html.parser")
            >>> PageMeta.select(soup, TITLE)
            'Hello World From Twitter Title!'
            >>> PageMeta.select(soup, DESC)
            'this is a description from twitter:desc'

        Args:
            soup (BeautifulSoup): Converted html content into a soup object
            selectors (Iterable[str]): CSS selectors as a tuple

        Returns:
            str | None: If found, return the text value.
        """
        for selector in selectors:
            if selector.startswith("meta"):
                if desc := soup.select(selector):
                    if content := desc[0].get("content"):
                        if content and isinstance(content, str):
                            return content
            elif selector == "title":
                if titles := soup("title"):
                    return titles[0].get_text()
        return None
