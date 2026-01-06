.PHONY: help setup build serve preview clean post

# Default target
help:
	@echo "Available commands:"
	@echo "  make setup    - Install dependencies (bundler, jekyll, gems)"
	@echo "  make serve    - Serve the site locally at http://localhost:4000"
	@echo "  make preview  - Alias for 'serve'"
	@echo "  make build    - Build the site to ./_site"
	@echo "  make clean    - Remove the generated ./_site directory"
	@echo "  make post     - Create a new blog post (usage: make post TITLE='My New Post')"

setup:
	gem install bundler jekyll
	bundle install

build:
	bundle exec jekyll build

serve:
	bundle exec jekyll serve

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
