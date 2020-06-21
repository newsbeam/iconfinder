from typing import List, Optional

from base64 import b64encode
from urllib.parse import urljoin
from io import BytesIO

from bs4 import BeautifulSoup
from PIL import Image, UnidentifiedImageError
import requests

TIMEOUT = 3  # seconds


class Icon:
    """
    All icons are assumed to be square.
    """

    def __init__(self, url: str, size: int, mimetype: str, data: bytes):
        self.url = url
        self.size = size
        self.mimetype = mimetype
        self.data = data
        self.data_uri = "data:%s;base64,%s" % (mimetype, b64encode(data).decode("ascii"))

    def __repr__(self):
        if "icon" in self.mimetype:
            format = "ico"
        else:
            format = self.mimetype.split("/", 1)[1]

        return "Icon {0} {1}x{1}".format(format, self.size)

    @classmethod
    def from_url(cls, url: str) -> Optional["Icon"]:
        try:
            res = requests.get(url, timeout=TIMEOUT)
            res.raise_for_status()
        except requests.exceptions.RequestException:
            return None

        with BytesIO(res.content) as bio:
            try:
                img = Image.open(bio)
            except (UnidentifiedImageError, ValueError):
                return None
        width, height = img.size
        # Ignore non-square Icons
        if width != height:
            return None

        mimetype = res.headers["Content-Type"].split(";", 1)[0].strip()
        return cls(url, width, mimetype, res.content)


def icons(url: str) -> List[Icon]:
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return []

    soup = BeautifulSoup(response.text, features="lxml")
    links = soup.find_all("link", attrs={"rel": "shortcut icon", "href": True}) \
            + soup.find_all("link", attrs={"rel": "icon", "href": True}) \
            + soup.find_all("link", attrs={"rel": "apple-touch-icon-precomposed", "href": True}) \
            + soup.find_all("link", attrs={"rel": "apple-touch-icon", "href": True}) \
            + [{"href": "/favicon.ico"}]
    hrefs = set(urljoin(url, link["href"]) for link in links)

    icons_ = [Icon.from_url(urljoin(url, href)) for href in hrefs]  # type: List[Optional[Icon]]
    return sorted(filter(lambda i: i is not None, icons_), key=lambda i: i.size, reverse=True)
