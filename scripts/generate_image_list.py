#!/usr/bin/env python3
"""Scan content files for placeholder images and produce a list of required images.

The script searches Markdown files for image references and location placeholders,
then writes a consolidated list of desired image filenames with improved descriptions.
"""
import os
import re
from pathlib import Path

CONTENT_DIR = Path('content')
OUTPUT_DIR = Path('static/image-requests')
OUTPUT_FILE = OUTPUT_DIR / 'images-needed.txt'

IMAGE_PATTERN = re.compile(r'!\[(.*?)\]\((.*?)\)')
HERO_PATTERN = re.compile(r'<div class="hero">(.*?) hero placeholder</div>')
SHORTCODE_PATTERN = re.compile(r'{{<\s*requestedimg\s+file="([^"]+)"\s+alt="([^"]+)"\s*>}}')


def slug_from_path(path: Path) -> str:
    rel = path.relative_to(CONTENT_DIR).with_suffix('')
    parts = rel.parts
    if parts and parts[-1] == '_index':
        parts = parts[:-1] + ('home',)
    return '-'.join(parts)


def improve_description(text: str) -> str:
    return f"{text}. High-resolution, well-lit photo capturing the subject clearly to convey professionalism and trust."


def main() -> None:
    entries = {}
    for md_file in CONTENT_DIR.rglob('*.md'):
        slug = slug_from_path(md_file)
        content = md_file.read_text(encoding='utf-8')

        index = 1
        for alt, src in IMAGE_PATTERN.findall(content):
            if 'placehold' in src:
                filename = f"{slug}-{index}.jpg"
                description = improve_description(alt)
                entries[filename] = description
                index += 1

        for _ in HERO_PATTERN.findall(content):
            filename = f"{slug}-hero.jpg"
            description = improve_description(f"Hero image for {slug.replace('-', ' ')} page")
            entries[filename] = description

        if '<div class="placeholder-box"></div>' in content:
            filename = f"{slug}-detail.jpg"
            description = improve_description(f"Detail image for {slug.replace('-', ' ')} page")
            entries[filename] = description

        for file_name, alt in SHORTCODE_PATTERN.findall(content):
            description = improve_description(alt)
            entries[file_name] = description

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open('w', encoding='utf-8') as f:
        for filename in sorted(entries):
            f.write(f"{filename} | {entries[filename]}\n")


if __name__ == '__main__':
    main()
