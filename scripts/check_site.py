from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "index.html"
CSS_PATH = ROOT / "styles.css"

REQUIRED_IDS = {
    "resume",
    "focus-heading",
    "stack-heading",
    "education-heading",
    "impact-heading",
    "experience-heading",
    "projects-heading",
    "contact-heading",
}

REQUIRED_META = {
    ("name", "description"),
    ("property", "og:title"),
    ("property", "og:description"),
    ("property", "og:url"),
    ("property", "og:image"),
    ("name", "twitter:card"),
}


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.local_refs: list[tuple[str, str]] = []
        self.fragment_refs: list[str] = []
        self.images_without_alt: list[str] = []
        self.unsafe_blank_links: list[str] = []
        self.meta_keys: set[tuple[str, str]] = set()
        self.main_count = 0
        self.h1_count = 0
        self.form_count = 0
        self.has_lang = False
        self.has_viewport = False
        self.has_canonical = False
        self.has_script = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)

        if tag == "html":
            self.has_lang = bool(data.get("lang"))
        elif tag == "main":
            self.main_count += 1
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "form":
            self.form_count += 1
        elif tag == "script":
            self.has_script = True
        elif tag == "meta":
            if data.get("name") == "viewport":
                self.has_viewport = True
            for key in ("name", "property"):
                value = data.get(key)
                if value and data.get("content"):
                    self.meta_keys.add((key, value))
        elif tag == "link":
            if data.get("rel") == "canonical" and data.get("href"):
                self.has_canonical = True

        element_id = data.get("id")
        if element_id:
            self.ids.append(element_id)

        if tag == "img" and "alt" not in data:
            self.images_without_alt.append(data.get("src") or "<unknown>")

        if tag == "a":
            href = data.get("href") or ""
            if href.startswith("#") and len(href) > 1:
                self.fragment_refs.append(href[1:])

            if data.get("target") == "_blank":
                rel = set((data.get("rel") or "").split())
                if not {"noopener", "noreferrer"}.issubset(rel):
                    self.unsafe_blank_links.append(href)

        for attribute in ("href", "src"):
            value = data.get(attribute)
            if not value or value.startswith(("#", "mailto:", "tel:", "data:")):
                continue

            parsed = urlparse(value)
            if parsed.scheme or parsed.netloc:
                continue

            self.local_refs.append((tag, value))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    css = CSS_PATH.read_text(encoding="utf-8")

    parser = SiteParser()
    parser.feed(html)

    require(parser.has_lang, "HTML document must declare a language.")
    require(parser.has_viewport, "Viewport metadata is required.")
    require(parser.has_canonical, "Canonical URL is required.")
    require(REQUIRED_META <= parser.meta_keys, f"Missing metadata: {sorted(REQUIRED_META - parser.meta_keys)}")
    require(parser.main_count == 1, "Expected exactly one <main> element.")
    require(parser.h1_count == 1, "Expected exactly one <h1> element.")
    require(parser.form_count == 0, "The resume should not contain a non-functional form.")
    require(not parser.has_script, "The production page intentionally has no JavaScript runtime.")
    require("javascript:" not in html.lower(), "Inline JavaScript URLs are not allowed.")
    require(not parser.images_without_alt, f"Images missing alt text: {parser.images_without_alt}")
    require(not parser.unsafe_blank_links, f"Unsafe target=_blank links: {parser.unsafe_blank_links}")

    duplicate_ids = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
    require(not duplicate_ids, f"Duplicate HTML IDs: {duplicate_ids}")

    id_set = set(parser.ids)
    require(REQUIRED_IDS <= id_set, f"Missing recruiter-facing sections: {sorted(REQUIRED_IDS - id_set)}")

    missing_fragments = sorted(set(parser.fragment_refs) - id_set)
    require(not missing_fragments, f"Broken fragment links: {missing_fragments}")

    missing_files: list[str] = []
    for _tag, value in parser.local_refs:
        local_path = value.split("#", 1)[0].split("?", 1)[0]
        if local_path and not (ROOT / local_path).exists():
            missing_files.append(value)

    require(not missing_files, f"Missing local files: {sorted(set(missing_files))}")

    require("@media print" in css, "Print stylesheet is required.")
    require(":focus-visible" in css, "Visible keyboard focus styling is required.")
    require("prefers-reduced-motion" in css, "Reduced-motion handling is required.")
    require("forced-colors" in css, "Forced-colors handling is required.")

    print("Site checks passed.")


if __name__ == "__main__":
    main()
