#!/usr/bin/env python3
"""
Download a web article to raw/<topic>/articles/ as markdown.

Usage:
    python scripts/ingest_url.py <url> <topic> [--date YYYY-MM-DD] [--slug custom-slug]

Topics: investing, ai-coding, data-engineering

Dependencies:
    pip install requests html2text beautifulsoup4
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urljoin, urlparse

try:
    import requests
    import html2text
    from bs4 import BeautifulSoup
except ImportError:
    print("Missing dependencies. Run: pip install requests html2text beautifulsoup4")
    sys.exit(1)

VALID_TOPICS = {"investing", "ai-coding", "data-engineering"}
REPO_ROOT = Path(__file__).parent.parent


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text[:60].strip("-")


def download_image(url: str, assets_dir: Path, session: requests.Session) -> Path | None:
    try:
        resp = session.get(url, timeout=10)
        resp.raise_for_status()
        ext = Path(urlparse(url).path).suffix or ".jpg"
        filename = slugify(Path(urlparse(url).path).stem) + ext
        dest = assets_dir / filename
        dest.write_bytes(resp.content)
        return dest
    except Exception:
        return None


def fetch_and_convert(url: str, topic: str, slug: str, out_date: str) -> str:
    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (compatible; knowledge-base-ingest/1.0)"

    resp = session.get(url, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    title = soup.title.string.strip() if soup.title else slug

    assets_dir = REPO_ROOT / "raw" / topic / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    # Download images and rewrite src to relative paths
    for img in soup.find_all("img"):
        src = img.get("src")
        if not src:
            continue
        abs_src = urljoin(url, src)
        local = download_image(abs_src, assets_dir, session)
        if local:
            rel = Path("../assets") / local.name
            img["src"] = str(rel)

    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.ignore_images = False
    converter.body_width = 0  # no wrapping
    converter.protect_links = True

    # Try to extract main content; fall back to full body
    main = soup.find("main") or soup.find("article") or soup.find("body")
    markdown = converter.handle(str(main))

    header = f"""---
title: "{title}"
source_url: {url}
date: {out_date}
topic: {topic}
---

# {title}

> Source: {url}

"""
    return header + markdown.strip()


def main():
    parser = argparse.ArgumentParser(description="Ingest a web article as markdown")
    parser.add_argument("url", help="URL to download")
    parser.add_argument("topic", choices=VALID_TOPICS, help="Knowledge base topic")
    parser.add_argument("--date", default=str(date.today()), help="Date (YYYY-MM-DD)")
    parser.add_argument("--slug", default=None, help="Custom filename slug")
    args = parser.parse_args()

    slug = args.slug or slugify(urlparse(args.url).path.split("/")[-1] or args.url)
    filename = f"{args.date}-{slug}.md"
    out_path = REPO_ROOT / "raw" / args.topic / "articles" / filename

    if out_path.exists():
        print(f"Already exists: {out_path}")
        sys.exit(1)

    print(f"Fetching {args.url} ...")
    content = fetch_and_convert(args.url, args.topic, slug, args.date)

    out_path.write_text(content, encoding="utf-8")
    print(f"Saved: {out_path.relative_to(REPO_ROOT)}")
    print()
    print("Next step: tell Claude to process this file into the wiki:")
    print(f'  "Process raw/{args.topic}/articles/{filename} and update the wiki."')


if __name__ == "__main__":
    main()
