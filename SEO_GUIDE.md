# SEO Guide

## Front Matter Fields

| Key | Description | Default |
| --- | --- | --- |
| `title` | Page title | required |
| `meta_desc` | Meta description | from summary or site param |
| `slug` | URL slug | generated from title |
| `aliases` | Legacy paths for 301 redirects | [] |
| `draft` | If true, page excluded | `false` |
| `date` | Publish date | file mtime |
| `lastmod` | Last modified date | file mtime |
| `tags`/`categories` | Taxonomy terms | [] |
| `canonical` | Override canonical URL | computed |
| `robots` | Custom robots directive | `index,follow` |
| `images` | Array of image paths | [] |
| `social_image` | Image used for social cards | first item in `images` |
| `schema` | Additional schema properties | {} |
| `noindex` | Boolean shortcut for `noindex,follow` | `false` |

## Redirects

- Per-page: set `aliases` in front matter.
- Global `_redirects` file: create `static/_redirects` with one rule per line.

## Testing

Run locally before deploying:

```bash
hugo --gc --minify
htmltest || true
html-validate public/**/*.html || true
```
