.PHONY: help setup build serve serve-future preview clean test post snack require-mise

HUGO = mise exec -- hugo

# Default target
help:
	@echo "Available commands:"
	@echo "  make setup    - Install pinned Hugo, the PaperMod theme submodule, and test dependencies"
	@echo "  make serve    - Serve the site locally at http://localhost:1313"
	@echo "  make serve-future - Serve the site locally including future-dated posts"
	@echo "  make preview  - Alias for 'serve'"
	@echo "  make build    - Build the site to ./public"
	@echo "  make test     - Check every page in a browser with Playwright"
	@echo "  make clean    - Remove generated files"
	@echo "  make post     - Create a new blog post (usage: make post TITLE='My New Post')"
	@echo "  make snack    - Create a new short note (usage: make snack TITLE='My Note')"

require-mise:
	@command -v mise >/dev/null 2>&1 || { echo "mise is required. Install it: https://mise.jdx.dev/installing-mise.html"; exit 1; }

setup build serve serve-future test post snack: require-mise

setup:
	mise install
	git submodule update --init
	npm install
	npx playwright install chromium

build:
	$(HUGO) --gc --minify

serve:
	$(HUGO) server

# Hugo hides future-dated posts by default. Use this to preview them.
serve-future:
	$(HUGO) server --buildFuture

preview: serve

test:
	npx playwright test

clean:
	rm -rf public resources .hugo_build.lock test-results playwright-report

# Usage: make post TITLE="My Post Title"   -> content/posts/YYYY-MM-DD-my-post-title.md, served at /my-post-title/
# Usage: make snack TITLE="My Note"        -> content/snacks/YYYY-MM-DD-my-note.md, served at /snacks/my-note/
# TITLE reaches the shell through the environment, so quotes and apostrophes in it are safe.
post snack: export TITLE := $(TITLE)
post snack:
	@if [ -z "$$TITLE" ]; then \
		echo "Error: TITLE is undefined. Usage: make $@ TITLE=\"My Title\""; \
		exit 1; \
	fi
	@SLUG=$$(printf '%s' "$$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | tr -s '-' | sed 's/^-//; s/-$$//'); \
	FILE="content/$@s/$$(date +%Y-%m-%d)-$$SLUG.md"; \
	if [ -e "$$FILE" ]; then echo "Error: $$FILE already exists."; exit 1; fi; \
	ESCAPED=$$(printf '%s' "$$TITLE" | sed 's/\\/\\\\/g; s/"/\\"/g'); \
	printf -- '---\ntitle: "%s"\ndate: %s\n---\n\n' "$$ESCAPED" "$$(date +%Y-%m-%d)" > "$$FILE"; \
	echo "Created $$FILE"
