# CSS Resume — Mykola Dotsenko

A recruiter-facing, print-ready software engineering resume built with **semantic HTML and modern CSS only**.

The repository started as an early CSS learning exercise. The current version keeps that original constraint but upgrades the project into a deliberately small engineering case study: clear content hierarchy, responsive layout, accessibility, print output, automated structural checks, and no unnecessary runtime code.

## What the page does

- presents a concise software-engineering profile
- highlights production impact and current experience
- links to selected portfolio projects
- adapts cleanly across desktop, tablet, and mobile
- prints to an A4-friendly resume/PDF from the browser
- works without JavaScript, a framework, a bundler, or runtime dependencies

## Why no framework?

A resume is static content. React, Next.js, a design system, or a JavaScript animation layer would increase the maintenance surface without solving a product requirement.

The implementation therefore uses the smallest appropriate stack:

- semantic HTML5
- modern CSS
- CSS Grid and Flexbox
- fluid typography with `clamp()`
- CSS custom properties as design tokens
- responsive breakpoints
- `:focus-visible` keyboard states
- `prefers-reduced-motion`
- dedicated `@media print` rules
- GitHub Actions for automated checks

## Design principles

### 1. Content first

The visual hierarchy is built around what a recruiter needs to scan quickly: role, focus, production impact, experience, technical strengths, and selected projects.

### 2. One source, two outputs

The same HTML serves both the responsive website and the print/PDF resume. Print CSS removes screen-only chrome, flattens decorative surfaces, and switches to an A4-oriented grid.

### 3. Proportional architecture

There is no component framework, runtime state, client-side routing, form submission layer, or animation dependency because the page does not need them.

### 4. Accessibility by default

The page includes:

- a skip link
- semantic landmarks and heading structure
- descriptive image alternative text
- visible keyboard focus states
- safe external-link behavior
- reduced-motion handling
- readable contrast and scalable typography

## Quality checks

Run:

```bash
python scripts/check_site.py
```

The zero-dependency checker verifies important invariants, including:

- one `<main>` and one `<h1>`
- a document language
- viewport and description metadata
- unique HTML IDs
- valid local file references
- valid internal fragment links
- image alternative text
- safe `target="_blank"` links
- no inline JavaScript
- no `<script>` runtime
- presence of print and focus-visible CSS

GitHub Actions runs the same checks on pushes and pull requests.

## Project structure

```text
.
├── .github/
│   └── workflows/
│       └── quality.yml
├── scripts/
│   └── check_site.py
├── avatar.jpg
├── favicon.svg
├── index.html
├── styles.css
└── README.md
```

## Run locally

No installation is required.

Open `index.html` directly, or serve the directory with any static HTTP server:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

## Print / PDF

Use the browser's print command and choose **Save as PDF**. The page has dedicated A4 print rules and automatically removes screen-only labels and footer text.

## Engineering goal

The project is intentionally small. Its value is not feature count; it is showing that a static page can still demonstrate professional judgment:

**use the simplest architecture that fully satisfies the product, then make that implementation exceptionally clear, resilient, accessible, and maintainable.**
