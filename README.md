# CSS Resume — Mykola Dotsenko

A recruiter-facing, print-ready software engineering resume built with **semantic HTML and modern CSS only**.

**Live site:** https://mykoladotsenko.github.io/My-CSS-CV/

The repository started as an early CSS learning exercise. The current version keeps that constraint while turning the project into a focused engineering case study: high-signal content, responsive layout, accessibility, print output, browser verification, and no runtime JavaScript.

## Product goal

The live page is intentionally optimized for a recruiter or hiring manager scanning quickly:

1. identity and engineering focus
2. measurable production impact
3. software-engineering trajectory
4. selected projects
5. technical strengths and education
6. a direct path to GitHub or LinkedIn

Implementation commentary stays here in the README instead of competing with hiring information on the live page.

## Why no framework?

A resume is static content. React, Next.js, a design system, a state library, or a runtime animation layer would increase the maintenance surface without solving a product requirement.

The production page therefore has:

- semantic HTML5
- modern CSS
- CSS Grid and Flexbox
- fluid typography with `clamp()`
- CSS custom properties as design tokens
- responsive breakpoints
- `:focus-visible`
- `prefers-reduced-motion`
- forced-colors support
- dedicated A4-oriented print rules
- **zero runtime JavaScript**
- **zero runtime dependencies**

Browser tooling exists only in development/CI.

## Quality strategy

### Static invariants

```bash
python scripts/check_site.py
```

The zero-dependency checker validates:

- one `<main>` and one `<h1>`
- document language
- viewport and description metadata
- canonical URL and core social metadata
- unique HTML IDs
- local files and fragment links
- image alternative text
- safe external links
- no forms or JavaScript runtime
- print, focus-visible, reduced-motion, and forced-colors CSS
- expected recruiter-facing sections

### Browser, accessibility, and print checks

```bash
npm install
npx playwright install chromium
npm run test:e2e
```

Playwright checks the page in desktop and mobile Chromium for:

- successful render
- no page errors or console errors
- no horizontal overflow
- critical recruiter-facing content
- expected external project/profile links
- WCAG A/AA serious/critical violations via axe
- print media behavior
- successful A4 PDF generation

These are development-only dependencies. They do not change the runtime architecture of the site.

## CI

GitHub Actions runs static validation and browser/a11y/print checks on pull requests and pushes to `main`.

The repository also contains a GitHub Pages deployment workflow for the static production assets.

## Project structure

```text
.
├── .github/
│   └── workflows/
│       ├── pages.yml
│       └── quality.yml
├── scripts/
│   └── check_site.py
├── tests/
│   └── resume.spec.js
├── avatar.jpg
├── favicon.svg
├── index.html
├── package.json
├── playwright.config.js
├── styles.css
└── README.md
```

## Run locally

No application installation is required:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`.

Install npm packages only when running the browser verification suite.

## Print / PDF

Use the browser's print command and choose **Save as PDF**. Screen-only actions are removed in print media and the layout switches to an A4-oriented presentation.

## Engineering rationale

The useful signal in this repository is not feature count. It is proportionality:

> Use the simplest architecture that fully satisfies the product, then make that implementation clear, accessible, verifiable, and maintainable.

The live surface serves recruiters. The README and tests provide the engineering evidence.
