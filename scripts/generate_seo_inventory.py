#!/usr/bin/env python3
"""Generate an SEO inventory report from built Hugo output.

Parses the rendered HTML in the public/ directory to collect
headings, metadata, canonical URLs, structured data types, and
robots directives, then writes both CSV and JSON summaries.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass, asdict
from html import unescape
from pathlib import Path
from typing import Iterable, List, Set

from bs4 import BeautifulSoup


@dataclass
class PageInventoryRow:
    url: str
    h1: str
    heading_outline: str
    title: str
    meta_description: str
    canonical: str
    structured_data_types: str
    notes: str
    manual_review: str


def iter_html_files(public_dir: Path) -> Iterable[Path]:
    for path in sorted(public_dir.rglob("*.html")):
        rel_parts = path.relative_to(public_dir).parts
        if len(rel_parts) >= 3 and rel_parts[0] == "404" and rel_parts[1] == "page" and path.name != "index.html":
            # Skip Netlify-style redirect helpers inside /404/page/.
            continue
        yield path


def build_url(base_url: str, html_path: Path, public_dir: Path) -> str:
    rel = html_path.relative_to(public_dir)
    if rel.name == "index.html":
        parent = rel.parent.as_posix()
        if parent in ("", "."):
            return base_url
        if not parent.endswith("/"):
            parent += "/"
        return f"{base_url.rstrip('/')}/{parent}"
    return f"{base_url.rstrip('/')}/{rel.as_posix()}"


def extract_headings(soup: BeautifulSoup) -> tuple[str, str, str]:
    headings: List[str] = []
    h1_text = ""
    manual_notes: List[str] = []
    for tag in soup.find_all(["h1", "h2", "h3"]):
        text = tag.get_text(separator=" ", strip=True)
        if not text:
            continue
        text = unescape(text)
        level = tag.name[1]
        headings.append(f"H{level}: {text}")
        if tag.name == "h1":
            if not h1_text:
                h1_text = text
            else:
                manual_notes.append("Multiple H1 elements detected")
    outline = " > ".join(headings)
    return h1_text, outline, "; ".join(dict.fromkeys(manual_notes))


def extract_meta(soup: BeautifulSoup) -> tuple[str, str, str]:
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else ""

    desc_tag = soup.find("meta", attrs={"name": "description"})
    description = desc_tag["content"].strip() if desc_tag and desc_tag.has_attr("content") else ""

    canon_tag = soup.find("link", attrs={"rel": "canonical"})
    canonical = canon_tag["href"].strip() if canon_tag and canon_tag.has_attr("href") else ""

    return title, description, canonical


def extract_structured_data(soup: BeautifulSoup) -> tuple[str, str]:
    types: Set[str] = set()
    notes: List[str] = []
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw = script.string
        if not raw:
            continue
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            notes.append("Structured data JSON parse error")
            continue
        nodes: List[dict] = []
        if isinstance(data, dict) and "@graph" in data and isinstance(data["@graph"], list):
            nodes = [n for n in data["@graph"] if isinstance(n, dict)]
        elif isinstance(data, list):
            nodes = [n for n in data if isinstance(n, dict)]
        elif isinstance(data, dict):
            nodes = [data]
        for node in nodes:
            node_type = node.get("@type")
            if not node_type:
                continue
            if isinstance(node_type, list):
                for t in node_type:
                    if isinstance(t, str):
                        types.add(t)
            elif isinstance(node_type, str):
                types.add(node_type)
    return ", ".join(sorted(types)), "; ".join(notes)


def extract_robots(soup: BeautifulSoup) -> str:
    robots_tag = soup.find("meta", attrs={"name": "robots"})
    if robots_tag and robots_tag.has_attr("content"):
        return robots_tag["content"].strip()
    return ""


def process_file(base_url: str, html_path: Path, public_dir: Path) -> PageInventoryRow:
    html = html_path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")

    url = build_url(base_url, html_path, public_dir)
    title, description, canonical = extract_meta(soup)
    h1_text, outline, heading_notes = extract_headings(soup)
    sd_types, sd_notes = extract_structured_data(soup)
    robots = extract_robots(soup)

    notes_parts: List[str] = []
    if robots:
        robots_lower = robots.lower()
        if "noindex" in robots_lower or "nofollow" in robots_lower:
            notes_parts.append(f"robots={robots}")
    if heading_notes:
        notes_parts.append(heading_notes)
    if sd_notes:
        notes_parts.append(sd_notes)
    if not description:
        notes_parts.append("Missing meta description")
    if not h1_text:
        notes_parts.append("Missing H1")

    notes = "; ".join(notes_parts)

    manual_review = ""
    if "Multiple H1" in notes or "Missing meta description" in notes or "Structured data JSON parse error" in notes:
        manual_review = "Check headings or metadata"

    return PageInventoryRow(
        url=url,
        h1=h1_text,
        heading_outline=outline,
        title=title,
        meta_description=description,
        canonical=canonical,
        structured_data_types=sd_types,
        notes=notes,
        manual_review=manual_review,
    )


def write_reports(rows: List[PageInventoryRow], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "seo-inventory.csv"
    json_path = output_dir / "seo-inventory.json"

    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(PageInventoryRow.__annotations__.keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))

    with json_path.open("w", encoding="utf-8") as fh:
        json.dump([asdict(row) for row in rows], fh, ensure_ascii=False, indent=2)

    print(f"Wrote {csv_path}")
    print(f"Wrote {json_path}")


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate SEO inventory from built site output.")
    parser.add_argument("--public-dir", default="public", type=Path, help="Path to the built public directory")
    parser.add_argument("--output-dir", default=Path("reports"), type=Path, help="Directory for generated reports")
    parser.add_argument("--base-url", default="https://localpest.co/", help="Base URL for constructing canonical page URLs")
    args = parser.parse_args(argv)

    public_dir: Path = args.public_dir
    if not public_dir.exists():
        parser.error(f"Public directory {public_dir} does not exist. Run 'hugo --gc --minify' first.")

    rows = [process_file(args.base_url, path, public_dir) for path in iter_html_files(public_dir)]
    rows.sort(key=lambda row: row.url)
    write_reports(rows, Path(args.output_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
