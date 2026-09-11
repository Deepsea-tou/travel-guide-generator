#!/usr/bin/env python3
"""Export Travel Roadbook v2 bundles using the proven legacy formats."""

from pathlib import Path

try:
    from .export_guide import geojson_data, ics_text, markdown_text
    from .guide_utils import write_json
    from .render_roadbook import render_file
except ImportError:
    from export_guide import geojson_data, ics_text, markdown_text
    from guide_utils import write_json
    from render_roadbook import render_file


def export_roadbook_bundle(data, output_base):
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
    write_json(paths["normalized_json"], data)
    write_json(paths["quality_json"], data.get("quality", {}))
    paths["markdown"].write_text(markdown_text(data), encoding="utf-8")
    with paths["ics"].open("w", encoding="utf-8", newline="") as stream:
        stream.write(ics_text(data))
    write_json(paths["geojson"], geojson_data(data))

    render_file(data, paths["html"])
    return {name: str(path) for name, path in paths.items()}
