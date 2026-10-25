# Repository Guide

## Commands

- Install mise, run `mise trust` once in the repository, then `make setup` to install pinned Ruby, the lockfile's Bundler, and local gems. Run `make serve` for `http://localhost:4000`; Make uses `mise exec` without requiring shell activation.
- Use `make serve-future` when a future-dated post must appear locally; normal Jekyll serving hides it.
- Run `make build` as the repository's verification step. There are no test, lint, or typecheck suites.
- Restart Jekyll after editing `_config.yml`; Jekyll does not reload that file while serving.
- Do not use `rake preview`: its task targets a missing `test/` tree. The Makefile's `preview` target is the valid alias for `make serve`.
- Do not treat `.travis.yml` as current CI: it targets a missing `docs/` tree and Ruby 2.4. There are no GitHub Actions workflows.
- `make update` runs Bundler through mise and updates gems and `Gemfile.lock`; it does not remove local theme overrides.
- `package.json` is only for the checked-in theme JavaScript bundle. After editing JavaScript sources, run `npm run build:js` to regenerate `assets/js/main.min.js`.

## Site Structure

- This is one root Jekyll site, not a Node application or monorepo. Site configuration is `_config.yml`; current content lives in `index.md`, `_pages/`, and `_posts/`.
- The site loads Minimal Mistakes through `remote_theme`, but checked-in `_layouts/` and `_includes/` files override matching remote-theme files. Check both the local override and theme behavior before changing layouts.
- `_pages/blog.md` and `_pages/cv.md` define case-sensitive `/Blog/` and `/CV/` permalinks; `_data/navigation.yml` must keep matching URLs.
- Create posts with `make post TITLE="Post Name"`. Cross-post links should use Jekyll's `{% post_url filename-without-extension %}` tag so permalink changes do not break them.

## Generated And Local Files

- `_site/`, `.jekyll-cache/`, `.bundle/`, `vendor/bundle/`, `.env`, and `private/` are gitignored local artifacts. Do not edit `_site/` as source. `mise.toml` pins Ruby and the tracked `Gemfile.lock` pins gems and Bundler.
- Gitignored does not mean excluded from Jekyll: `_config.yml` does not exclude `private/`, so files there become build inputs. Existing remote-theme temp copies under `private/` produce duplicate-page warnings during `make build`.
