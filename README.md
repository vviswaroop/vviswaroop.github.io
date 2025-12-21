# vviswaroop.github.io

This repository is the source for a personal website built with **Jekyll** and intended to be hosted on **GitHub Pages**.

## Local development

Prerequisites: Ruby and Bundler installed.

Install dependencies and run a local dev server:

```bash
bundle install
bundle exec jekyll serve
```

Open http://127.0.0.1:4000 locally.

## Deployment

You can use GitHub Pages to serve the site. This repo includes an Actions workflow that automatically builds the site on push to `main` and deploys the generated static site to the `gh-pages` branch.

To enable the site after the first deploy:

1. Go to the repository Settings → Pages. Select the **gh-pages** branch as the source and save. The site should become available at the URL in `_config.yml` once the workflow completes.

The repository also includes an additional workflow (`.github/workflows/jekyll-build.yml`) that runs a build check on push and PRs.

Blog development:

- Posts live under `_posts/` using standard Jekyll filenames (YYYY-MM-DD-title.md).
- The blog index is at `/blog/` and uses pagination (`paginate: 5`).
- Plugins included: `jekyll-feed`, `jekyll-sitemap`, `jekyll-seo-tag`, `jekyll-paginate`.

Testing tips (CI):

- The `jekyll-build` workflow runs a non-blocking HTML link check using `html-proofer`.
