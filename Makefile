.PHONY: help setup build serve serve-future preview clean update post require-mise

BUNDLER_VERSION := $(shell awk '/^BUNDLED WITH$$/ { getline; print $$1 }' Gemfile.lock)
BUNDLE = mise exec -- bundle _$(BUNDLER_VERSION)_

# Default target
help:
	@echo "Available commands:"
	@echo "  make setup    - Install pinned Ruby, Bundler, and project gems locally"
	@echo "  make update   - Update gems and Gemfile.lock"
	@echo "  make serve    - Serve the site locally at http://localhost:4000"
	@echo "  make serve-future - Serve the site locally including future posts"
	@echo "  make preview  - Alias for 'serve'"
	@echo "  make build    - Build the site to ./_site"
	@echo "  make clean    - Remove the generated ./_site directory"
	@echo "  make post     - Create a new blog post (usage: make post TITLE='My New Post')"

require-mise:
	@command -v mise >/dev/null 2>&1 || { echo "mise is required. Install it: https://mise.jdx.dev/installing-mise.html"; exit 1; }

setup update build serve serve-future: require-mise

setup:
	@echo "Installing dependencies..."
	mise install ruby
	mise exec -- gem install bundler --version $(BUNDLER_VERSION) --no-document
	$(BUNDLE) config set --local path vendor/bundle
	$(BUNDLE) install

update:
	@echo "Updating gems..."
	$(BUNDLE) update

build:
	$(BUNDLE) exec jekyll build

serve:
	$(BUNDLE) exec jekyll serve

# Jekyll hides future-dated posts by default. Use this to preview them.
serve-future:
	$(BUNDLE) exec jekyll serve --future

preview: serve

clean:
	rm -rf _site

# Helper to create a new post
# Usage: make post TITLE="My Post Title"
post:
	@if [ -z "$(TITLE)" ]; then \
		echo "Error: TITLE is undefined. Usage: make post TITLE=\"My Post Title\""; \
		exit 1; \
	fi
	@echo "Creating new post..."
	@DATE=$$(date +%Y-%m-%d); \
	SLUG=$$(echo '$(TITLE)' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-//' | sed 's/-$$//'); \
	FILENAME="_posts/$$DATE-$$SLUG.md"; \
	if [ -f "$$FILENAME" ]; then \
		echo "Error: File $$FILENAME already exists."; \
		exit 1; \
	fi; \
	echo "---" > "$$FILENAME"; \
	echo "layout: single" >> "$$FILENAME"; \
	echo "title: \"$(TITLE)\"" >> "$$FILENAME"; \
	echo "date: $$DATE" >> "$$FILENAME"; \
	echo "---" >> "$$FILENAME"; \
	echo "" >> "$$FILENAME"; \
	echo "New post created at: $$FILENAME"
