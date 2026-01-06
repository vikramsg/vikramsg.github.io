# GitHub Blog

This is my personal website built with Jekyll and the "Minimal Mistakes" theme, hosted on GitHub Pages.
The site is hosted at [https://vikramsg.github.io](https://vikramsg.github.io).

## Setup

### 1. Prerequisites (Ruby via Homebrew)
macOS comes with a "system Ruby" that is protected and often outdated. To avoid permission errors (`Gem::FilePermissionError`) and ensure compatibility, you should install a separate version of Ruby using Homebrew.

1.  **Install Homebrew** (if not already installed):
    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

2.  **Install Ruby**:
    ```bash
    brew install ruby
    ```

3.  **Update your PATH**: Add the Homebrew Ruby path to your shell configuration (e.g., `~/.zshrc` or `~/.bash_profile`). Homebrew will provide the specific path after installation, but it is typically:
    ```bash
    echo 'export PATH="/usr/local/opt/ruby/bin:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### 2. Install Dependencies
Once you are using the Homebrew-managed Ruby, you can set up the project dependencies.

1.  **Install Bundler**:
    ```bash
    gem install bundler
    ```

2.  **Install Project Gems**:
    ```bash
    make setup
    ```
    *Note: This uses the Makefile to install gems into a local `vendor/bundle` directory to keep your environment isolated.*

## Running the Blog Locally

To preview the website on your local machine, use the provided Makefile command:

```bash
make serve
```

Once the server is running, you can view your website by navigating to `http://localhost:4000/` in your web browser.

## Makefile Commands

The project includes a `Makefile` to automate common tasks:
*   `make setup`: Installs the required Ruby gems.
*   `make serve`: Runs the Jekyll server with auto-regeneration.
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
*   **Updating**: Since the site uses `remote_theme`, it automatically pulls the latest version. To update the underlying Jekyll engines and plugins, run `bundle update`.
*   **Configuration**: Most theme-specific settings (skins, navigation, author info) are controlled via `_config.yml`.

## Deployment

This blog is hosted on GitHub Pages. To deploy any changes, commit them and push to the `master` branch.

```bash
git add .
git commit -m "Your commit message"
git push
```
