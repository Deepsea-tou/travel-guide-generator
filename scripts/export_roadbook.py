#!/usr/bin/env python3
"""Export Travel Roadbook v2 bundles using the proven legacy formats."""

from pathlib import Path
from uuid import uuid4

try:
    from .export_guide import geojson_data, ics_text, markdown_text
    from .guide_utils import write_json
    from .render_roadbook import render_roadbook
    from .sanitize_share_version import sanitize_for_share
    from .validate_roadbook import validate_roadbook
except ImportError:
    from export_guide import geojson_data, ics_text, markdown_text
    from guide_utils import write_json
    from render_roadbook import render_roadbook
    from sanitize_share_version import sanitize_for_share
    from validate_roadbook import validate_roadbook


def export_roadbook_bundle(data, output_base):
    report = validate_roadbook(data)
    if report["status"] != "pass":
        codes = ", ".join(error["code"] for error in report["errors"])
        raise ValueError(f"roadbook validation failed: {codes}")
    if data.get("privacy", {}).get("output_scope") == "share" and sanitize_for_share(data) != data:
        raise ValueError("share roadbook must be sanitized before export")
    base = Path(output_base)
    base.parent.mkdir(parents=True, exist_ok=True)
    paths = {
        "normalized_json": base.with_suffix(".normalized.json"),
        "quality_json": base.with_suffix(".quality.json"),
        "html": base.with_suffix(".html"),
        "markdown": base.with_suffix(".md"),
        "ics": base.with_suffix(".ics"),
        "geojson": base.with_suffix(".geojson"),
    }
    rendered = {
        "markdown": markdown_text(data),
        "ics": ics_text(data),
        "geojson": geojson_data(data),
        "html": render_roadbook(data),
    }
    token = uuid4().hex
    temporary = {name: path.with_name(f".{path.name}.{token}.tmp") for name, path in paths.items()}
    try:
        write_json(temporary["normalized_json"], data)
        write_json(temporary["quality_json"], data.get("quality", {}))
        temporary["markdown"].write_text(rendered["markdown"], encoding="utf-8")
        with temporary["ics"].open("w", encoding="utf-8", newline="") as stream:
            stream.write(rendered["ics"])
        write_json(temporary["geojson"], rendered["geojson"])
        temporary["html"].write_text(rendered["html"], encoding="utf-8")
        for name, path in paths.items():
            temporary[name].replace(path)
    finally:
        for path in temporary.values():
            path.unlink(missing_ok=True)
    return {name: str(path) for name, path in paths.items()}
