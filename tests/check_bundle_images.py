"""Check real bundle images in built posts and every list that includes them."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
import sys


class Images(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            self.sources.append(dict(attrs).get("src", ""))


public = Path(sys.argv[1] if len(sys.argv) > 1 else "rnp/public")
expected = {
    "containers.png": "/2023/08/webstack/containers.png",
    "cloudy.png": "/2023/08/webstack/cloudy.png",
    "matrix-internet.png": "/2023/08/webstack/matrix-internet.png",
    "internet-cables.png": "/2023/07/the-internet/internet-cables.png",
    "internet-computer.png": "/2023/07/the-internet/internet-computer.png",
}
seen = {name: set() for name in expected}
errors = []
for page in public.rglob("index.html"):
    parser = Images()
    parser.feed(page.read_text())
    page_url = "/" + page.relative_to(public).as_posix().removesuffix("index.html")
    for source in parser.sources:
        name = Path(urlsplit(source).path).name
        if name not in expected:
            continue
        resolved = urlsplit(urljoin(page_url, source)).path
        if resolved != expected[name] or not (public / resolved.lstrip("/")).is_file():
            errors.append(f"{page_url}: {source!r} does not resolve to {expected[name]}")
        seen[name].add(page_url)

for name, locations in seen.items():
    single = expected[name].rsplit("/", 1)[0] + "/"
    if single not in locations:
        errors.append(f"{name}: missing from its individual post")
    if not any(url.startswith("/page/") for url in locations):
        errors.append(f"{name}: missing from homepage pagination")
    if not any(url.startswith("/posts/page/") for url in locations):
        errors.append(f"{name}: missing from posts pagination")

if errors:
    raise SystemExit("\n".join(errors))
print("Bundle images resolve to existing post resources in single and list views.")
