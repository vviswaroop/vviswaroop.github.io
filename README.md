# Viswaroop Vadlamudi — A personal atlas

Personal portfolio and writing archive built with Astro and Tailwind CSS. The site connects engineering work, ongoing questions, and reading notes through a spatial homepage and architecture-led project pages.

## Local development

```sh
npm ci
npm run dev -- --host 127.0.0.1
```

The development server prints its local address (normally http://127.0.0.1:4321).

```sh
npm run build
npm run preview
```

## Content

- `src/pages/index.astro`: personal atlas and connected entry points.
- `src/pages/work.astro`: project diagrams, decisions, and the illustrative agent walkthrough.
- `src/content/blog/`: original Markdown essays and reading notes.
- `src/pages/about.astro`, `now.astro`, `services.astro`: biography, ongoing exploration, and consulting.
- `src/styles/global.css`: shared visual system and responsive layouts.
- `src/components/SystemPlate.astro`: accessible architecture diagrams.

Tag URLs normalize case. Reading time is calculated from article content. RSS is the subscription mechanism; no email addresses are collected. The agent walkthrough is a local simulation and creates no real infrastructure or credentials. Navigation uses standard document navigation, keeping the demo lifecycle predictable.

Google Fonts are loaded with `display=swap` and local font fallbacks. No tracking was added.

## Publishing

The existing GitHub Pages workflow is retained. This redesign was built locally; it has not been pushed or published. The canonical domain remains https://viswaroop.dev.
