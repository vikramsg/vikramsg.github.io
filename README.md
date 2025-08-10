# GitHub Blog

This is my personal website built with Jekyll and the "Minimal Mistakes" theme, hosted on GitHub Pages.
The site is hosted at [https://vikramsg.github.io](https://vikramsg.github.io). 

## Setup

1.  **Prerequisites**: Ensure you have Ruby installed. It is recommended to install it via Homebrew on macOS if you encounter issues with the system's default version.

2.  **Install Dependencies**: Navigate to the project's root directory and run the following commands to install the necessary gems:

    ```bash
    gem install bundler jekyll
    bundle update
    ```

## Running the Blog Locally

To preview the website on your local machine, run the following command from the project's root directory:

```bash
bundle exec jekyll serve
```

Once the server is running, you can view your website by navigating to `http://localhost:4000/` in your web browser.

## Writing New Blog Posts

1.  **Create a new file**: All blog posts are located in the `_posts` directory.

2.  **File Naming Convention**: The filename must follow the format `YYYY-MM-DD-your-post-title.md`.

3.  **Front Matter**: At the beginning of your Markdown file, you must include the following front matter:

    ```yaml
    ---
    layout: single
    title:  "Your Post Title"
    date:   YYYY-MM-DD
    ---
    ```

4.  **Write your content**: Write your blog post content below the front matter using Markdown.

## Deployment

This blog is hosted on GitHub Pages. To deploy any changes, commit them and push to the `master` branch of your `username.github.io` repository.

```bash
git add .
git commit -m "Your commit message"
git push origin master
```
