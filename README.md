# GitHub Blog

This is my personal website built with Jekyll and the "Minimal Mistakes" theme, hosted on GitHub Pages.
The site is hosted at [https://vikramsg.github.io](https://vikramsg.github.io).

## Setup

### 1. Install mise

[mise](https://mise.jdx.dev/) manages the Ruby version pinned in `mise.toml`. On macOS or Linux, install its official prebuilt executable:

```bash
curl -fsSL https://mise.run | sh
```

The installer writes `~/.local/bin/mise` without changing your shell configuration. That directory must be on `PATH`; if needed, run `export PATH="$HOME/.local/bin:$PATH"` for the current terminal session. See mise's [installation instructions](https://mise.jdx.dev/installing-mise.html) for other methods.

On macOS, Ruby gems with native extensions require Apple's Command Line Tools. If they are not already installed, run `xcode-select --install`. On Linux, install your platform's Ruby build dependencies.

### 2. Install project dependencies

From the repository root, review `mise.toml`, trust it once, and run setup:

```bash
mise trust
make setup
```

Setup installs the pinned Ruby, the Bundler version recorded in `Gemfile.lock`, and the locked project gems into `vendor/bundle`. Commit `Gemfile.lock` when dependencies change so other machines use the same gem and Bundler versions.

Make runs Ruby commands through `mise exec`, so no mise shell activation, Homebrew Ruby installation, or Ruby PATH edits are needed. For direct Ruby commands, use `mise exec -- ruby --version` or `mise exec -- bundle exec jekyll build`. Plain `ruby` or `bundle` can still select macOS's system Ruby if mise is not activated in your shell.

## Running the Blog Locally

To preview the website on your local machine, use the provided Makefile command:

```bash
make serve
```

Once the server is running, you can view your website by navigating to `http://localhost:4000/` in your web browser.

## Makefile Commands

The project includes a `Makefile` to automate common tasks:
*   `make setup`: Installs pinned Ruby, the lockfile's Bundler, and project gems locally.
*   `make update`: Updates gems and `Gemfile.lock`; it does not remove local theme overrides.
*   `make serve`: Runs the Jekyll server with auto-regeneration.
*   `make serve-future`: Includes future-dated posts when serving locally.
*   `make preview`: Alias for `make serve`.
*   `make build`: Builds the static site to the `_site` folder.
*   `make post TITLE="Post Name"`: Scaffolds a new blog post with the correct date and front matter.
*   `make clean`: Removes the generated site files.

## Writing New Blog Posts

1.  **Create a new file**: Use the Makefile to generate a template:
    ```bash
    make post TITLE="Your Post Title"
    ```
    This creates a file in `_posts/` with the naming convention `YYYY-MM-DD-your-post-title.md`.

2.  **Front Matter**: The generated file will include the necessary metadata:
    ```yaml
    ---
    layout: single
    title:  "Your Post Title"
    date:   YYYY-MM-DD
    ---
    ```

3.  **Write your content**: Write your blog post content below the front matter using Markdown.

## What is Where

*   **Home Page**: The content of the home page (the "About Me" section) can be edited in `index.md` in the root directory.
*   **Navigation Tabs**: To add, remove, or edit the navigation tabs (e.g., "Blog"), modify the `_data/navigation.yml` file.
*   **Blog Page**: The page that lists all the blog posts is located at `_pages/blog.md`.
*   **Author Profile**: The author profile information (displayed on the left side) is configured in the `_config.yml` file.
*   **Newsletter Signup**: The newsletter signup form is located in `_data/signup.html`.
*   **Page Layouts**: The general page layouts are defined in the `_layouts` directory.

## How the Theme Works

This site uses the **Minimal Mistakes** theme via the `remote_theme` method.

*   **Remote Source**: The theme's core files are fetched directly from GitHub (`mmistakes/minimal-mistakes`).
*   **Local Overrides**: Any file you place in your local project directory (like `_sass`, `_includes`, or `_layouts`) will **automatically override** the equivalent file in the remote theme. This allows for deep customization without modifying the original theme.
*   **Updating**: Since the site uses `remote_theme`, it automatically pulls the latest version. To update the underlying Jekyll engines and plugins, run `make update` and review the changes to `Gemfile.lock`.
*   **Configuration**: Most theme-specific settings (skins, navigation, author info) are controlled via `_config.yml`.

## Deployment

This blog is hosted on GitHub Pages. To deploy any changes, commit them and push to the `main` branch.

```bash
git add .
git commit -m "Your commit message"
git push
```
