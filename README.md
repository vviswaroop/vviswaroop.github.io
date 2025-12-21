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

New features:

- Topic pages: `/developer/`, `/product/`, `/infrastructure/` — lists posts filtered by tag.
- Top tags pipeline: a small script `scripts/generate_top_tags.rb` generates `_data/top_tags.yml` (run in CI) so the homepage can display popular tags safely.
- Homepage: redesigned to a minimal, content-first layout (compact recent-post list and CTA).

Testing tips (CI):

- The `jekyll-build` workflow runs a non-blocking HTML link check using `html-proofer`.

If deploy fails with a 403 (permission denied)

- Cause: GitHub Actions' `GITHUB_TOKEN` may be restricted from creating or pushing the `gh-pages` branch depending on repository-level Actions permissions. The deploy job will report a 403 like: `Permission to ... denied to github-actions[bot]`.
- Quick fixes:
	1. Easiest: In the repo **Settings → Actions → General**, set **Workflow permissions** to **Read and write** and save. Then re-run the "Deploy to GitHub Pages" workflow.
	2. More controlled (recommended for locked-down repos): Create a personal access token (PAT) with **repo** scope, then add it as a repository secret named `GH_PAGES_DEPLOY_TOKEN` (Settings → Secrets and variables → Actions → New repository secret). The deploy workflow is already configured to use this secret if present.

If you want, I can (A) make the workflow use a PAT secret (already done), and commit instructions to the README (done), or (B) guide you through enabling the repo-level Actions write permission so you can re-run the deploy — tell me which you prefer and I'll proceed.
