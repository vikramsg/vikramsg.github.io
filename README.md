# GitHub Blog

This is my personal website built with [Hugo](https://gohugo.io/) and the [PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme, hosted on GitHub Pages.
The site is hosted at [https://vikramsg.github.io](https://vikramsg.github.io).

## Setup

### 1. Install mise

[mise](https://mise.jdx.dev/) manages the Hugo and Node versions pinned in `mise.toml`. On macOS or Linux, install its official prebuilt executable:

```bash
curl -fsSL https://mise.run | sh
```

The installer writes `~/.local/bin/mise` without changing your shell configuration. That directory must be on `PATH`; if needed, run `export PATH="$HOME/.local/bin:$PATH"` for the current terminal session. See mise's [installation instructions](https://mise.jdx.dev/installing-mise.html) for other methods.

### 2. Install project dependencies

From the repository root, review `mise.toml`, trust it once, and run setup:

```bash
mise trust
make setup
```

Setup installs the pinned Hugo and Node, checks out the PaperMod theme submodule, and installs Playwright and Chromium for `make test`.
If you cloned without `--recurse-submodules`, setup fetches the theme for you.

## Running the Blog Locally

```bash
make serve
```

Then open `http://localhost:1313/`. Hugo reloads the page as you edit, including `hugo.yaml`.

## Makefile Commands

*   `make setup`: Installs pinned tools, the theme submodule, and test dependencies.
*   `make serve`: Runs the Hugo server with live reload.
*   `make serve-future`: Includes future-dated posts when serving locally.
*   `make preview`: Alias for `make serve`.
*   `make build`: Builds the static site to `public/`.
*   `make test`: Opens every page in Chromium with Playwright and checks links, math, diagrams, feeds and search.
*   `make post TITLE="Post Name"`: Creates a new blog post.
*   `make snack TITLE="Note Name"`: Creates a new snack (short note).
*   `make clean`: Removes generated files.

## Writing

### Posts

```bash
make post TITLE="Your Post Title"
```

This creates `content/posts/YYYY-MM-DD-your-post-title.md`, published at `/your-post-title/`:

```yaml
---
title: "Your Post Title"
date: YYYY-MM-DD
---
```

Posts migrated from Jekyll set `url:` in their front matter to keep their original addresses. Don't change those.

### Snacks

Snacks are short notes: a link, a tip, something learned. They have their own page at `/snacks/`, which shows every snack in full, and their own feed at `/snacks/feed.xml`. They don't appear on the home page, in `/Blog/`, or in the main feed.

```bash
make snack TITLE="Your Note"
```

This creates `content/snacks/YYYY-MM-DD-your-note.md`, published at `/snacks/your-note/`.

### Math and diagrams

*   Inline math: `\(E = mc^2\)`. Display math: `$$` on its own line before and after the equation. Math is rendered to HTML at build time with KaTeX.
*   Diagrams: a fenced code block with the `mermaid` language.

## What is Where

*   **Site configuration**: `hugo.yaml` (title, menu, home page intro, social links, theme options).
*   **Home page**: the intro text is `params.homeInfoParams` in `hugo.yaml`; the post list below it is automatic.
*   **About page**: `content/about.md`.
*   **CV**: `content/cv.md` (served at `/CV/`).
*   **Blog archive**: `content/blog.md` (served at `/Blog/`).
*   **Theme**: `themes/PaperMod` is a git submodule pinned to a commit. Don't edit it; override files in `layouts/` instead.
*   **Local overrides** in `layouts/`:
    *   `_partials/extend_head.html`: KaTeX stylesheet, Mermaid, and Umami analytics (production only).
    *   `_markup/render-passthrough.html`: renders math with KaTeX.
    *   `_markup/render-codeblock-mermaid.html`: renders `mermaid` code blocks.
    *   `snacks/list.html`: the snacks page.
    *   `home.rss.xml`: keeps snacks out of the main feed.
    *   `_shortcodes/social_icons.html`: social links on the About page.
*   **Browser tests**: `tests/site.spec.ts`.

## Updating the Theme

```bash
git -C themes/PaperMod fetch
git -C themes/PaperMod checkout <commit-or-tag>
make build && make test
git add themes/PaperMod
```

Check PaperMod's `theme.toml` for the minimum Hugo version and bump `mise.toml` if needed. `layouts/home.rss.xml` is a copy of PaperMod's `rss.xml` with one change; re-copy it if the theme's feed template changes.

## Deployment

`.github/workflows/hugo.yml` builds the site and deploys it to GitHub Pages on every push to `main`. The repository's **Settings → Pages → Source** must be set to **GitHub Actions**.
