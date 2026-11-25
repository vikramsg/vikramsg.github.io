# Repository Guide

## Commands

- Install mise, run `mise trust` once in the repository, then `make setup` to install pinned Hugo and Node, the PaperMod submodule, and Playwright. Run `make serve` for `http://localhost:1313`; Make uses `mise exec` without requiring shell activation.
- Use `make serve-future` when a future-dated post must appear locally; Hugo hides it otherwise.
- Run `make build` and `make test` as the verification steps. `make build` should produce no warnings. `make test` runs the Playwright suite in `tests/` against `hugo server`; it checks every page in the sitemap plus legacy Jekyll URLs, so add an assertion there when adding a feature.
- Do not use a bare `hugo` if mise is not activated; use `mise exec -- hugo` so the version pinned in `mise.toml` is used.
- `package.json` exists only for Playwright. The site has no Node build.

## Site Structure

- This is one Hugo site. Configuration is `hugo.yaml`; content lives in `content/`.
- The theme is PaperMod, a git submodule at `themes/PaperMod` pinned to a commit. Never edit it. Files in `layouts/` override the theme's files at the same path; check both before changing templates.
- `/Blog/` and `/CV/` are case-sensitive URLs set with `url:` in `content/blog.md` and `content/cv.md`. Menu entries in `hugo.yaml` use `pageRef`, because Hugo lowercases menu `url` values.
- Posts migrated from Jekyll set `url:` to their old addresses; `tests/site.spec.ts` lists those URLs. Don't change them. New posts get `/<slug>/` from the filename.
- Create posts with `make post TITLE="Post Name"` and snacks (short notes) with `make snack TITLE="Note"`. Link between posts with `{{< ref "filename-without-extension" >}}`.
- Snacks live in `content/snacks/`. They are excluded from the home page, `/Blog/` and `/feed.xml` (`mainSections: [posts]` and `layouts/home.rss.xml`), and have their own feed at `/snacks/feed.xml`.
- Math: inline `\(...\)`, display `$$` on their own lines; rendered at build time by `layouts/_markup/render-passthrough.html`. Mermaid: fenced `mermaid` code blocks. The KaTeX stylesheet and Mermaid script are only loaded on pages that use them (`layouts/_partials/extend_head.html`).

## Generated And Local Files

- `public/`, `resources/`, `.hugo_build.lock`, `node_modules/`, `test-results/`, `playwright-report/`, and `.env` are gitignored. Do not edit `public/` as source.
- `.agents/` is local except for the shared Pax skill at `.agents/skills/branch/SKILL.md`. Use `/branch commit` in Pax to commit and push a finished snack, then `/branch merge` when you're ready to merge it and watch the deploy. If `/branch` isn't listed in an existing session, run `/reload` first.
- Hugo builds only from `content/`, `layouts/`, `static/`, `assets/`, `data/`, `i18n/` and the theme, so repo tooling files at the root are never published.
