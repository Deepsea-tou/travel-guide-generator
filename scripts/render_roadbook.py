#!/usr/bin/env python3
"""Render a self-contained TravelOS roadbook HTML document."""

from pathlib import Path

try:
    from .guide_utils import json_for_script, text
    from .roadbook_components import render_body
except ImportError:
    from guide_utils import json_for_script, text
    from roadbook_components import render_body


ROOT = Path(__file__).resolve().parents[1]


def _language(meta):
    language = str(meta.get("language", "zh-CN"))
    root = language.lower().split("-", 1)[0]
    direction = ' dir="rtl"' if root in {"ar", "fa", "he", "ur"} else ""
    return f'lang="{text(language)}"{direction}'


def render_roadbook(data):
    meta = data.get("meta", {})
    shell = (ROOT / "assets" / "roadbook-shell.html").read_text(encoding="utf-8")
    replacements = {
        "__LANG__": _language(meta),
        "__THEME__": text(meta.get("theme", "forest")),
        "__TITLE__": text(meta.get("title", "Travel Roadbook")),
        "__STYLE__": (ROOT / "assets" / "roadbook.css").read_text(encoding="utf-8"),
        "__BODY__": render_body(data),
        "__DATA__": json_for_script(data),
        "__SCRIPT__": (ROOT / "assets" / "roadbook.js").read_text(encoding="utf-8"),
    }
    for marker, value in replacements.items():
        shell = shell.replace(marker, value)
    return shell


def render_file(data, output):
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_roadbook(data), encoding="utf-8")
    return str(path)
