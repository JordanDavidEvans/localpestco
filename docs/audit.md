# SEO & UX Audit Plan

## Current Issues
- **Headings**: Site title uses `<h1>` in the header and content pages lack an explicit `<h1>`, leading to multiple or missing top-level headings.
- **Metadata**: `description` front matter isn't picked up for meta description because the partial expects `meta_desc`.
- **Last Modified**: `enableGitInfo` disabled; no `<meta property="article:modified_time">`.
- **Accessibility**: No skip link to main content; navigation has no structural indication of current page.
- **Performance**: CSS served from `static/` without minification or fingerprinting.

## Planned Changes
- Update templates to ensure a single `<h1>` per page sourced from front matter.
- Allow `description` front matter to populate meta description and include `article:modified_time`.
- Enable `enableGitInfo` in `hugo.toml` for accurate `.Lastmod`.
- Add a skip-to-content link and main landmark ID for keyboard users; style skip link for focus visibility.

## Requires Approval
- Migrating CSS/JS to Hugo Pipes for minification and fingerprinting.
- Adding LocalBusiness schema if business address/phone details are provided in site params.
- Further navigation or URL structure changes.

## Testing
- `hugo`
- `npx linkinator public` (after build)

## Changes Made
- Enabled Git-based lastmod and added `<meta property="article:modified_time">`.
- Reworked heading structure: site title no longer `<h1>`; templates now output page titles as `<h1>`.
- Added skip-to-content link and focusable styles.
- Meta partial now reads `description` front matter for meta descriptions.

## Test Results
- `hugo --minify` – warns about missing meta description on the 404 page.
- `npx linkinator public` – one broken external link (placeholder image returning 503).

## Core Web Vitals Risks
- [ ] Stylesheet not yet minified or fingerprinted.
- [ ] Placeholder external images returned errors during link check.
