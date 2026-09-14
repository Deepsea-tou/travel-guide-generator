#!/usr/bin/env python3
"""Build, validate, sanitize, render, and export a Travel Roadbook bundle."""

import argparse
import json
from pathlib import Path

try:
    from .build_guide import enrich_routes
    from .export_roadbook import export_roadbook_bundle
    from .extract_local_profile import empty_profile, extract_profile
    from .guide_utils import load_json
    from .migrate_guide import migrate_to_v2
    from .roadbook_modes import apply_personalization, select_mode
    from .sanitize_share_version import sanitize_for_share
    from .season_advisor import build_season_tips
    from .validate_roadbook import validate_roadbook
except ImportError:
    from build_guide import enrich_routes
    from export_roadbook import export_roadbook_bundle
    from extract_local_profile import empty_profile, extract_profile
    from guide_utils import load_json
    from migrate_guide import migrate_to_v2
    from roadbook_modes import apply_personalization, select_mode
    from sanitize_share_version import sanitize_for_share
    from season_advisor import build_season_tips
    from validate_roadbook import validate_roadbook


def build_roadbook(source, output_base, knowledge_root=None, output_scope="personal"):
    if output_scope not in {"personal", "share"}:
        raise ValueError("output_scope must be personal or share")
    data = migrate_to_v2(source)
    profile = extract_profile(knowledge_root) if knowledge_root else empty_profile()
    selected = select_mode(data.get("trip", {}))
    data["trip"].update(selected)
    data = apply_personalization(data, profile, data.get("request", {}))
    enrich_routes(data)
    data["season_tips"] = build_season_tips(data)
    data.setdefault("privacy", {})["output_scope"] = output_scope
    report = validate_roadbook(data)
    data["quality"] = report
    if report["status"] != "pass":
        return {"status": report["status"], "report": report, "files": {}}
    if output_scope == "share":
        data = sanitize_for_share(data)
    files = export_roadbook_bundle(data, output_base)
    return {"status": report["status"], "report": report, "files": files}


def main():
    parser = argparse.ArgumentParser(description="构建 Travel Roadbook v2")
    parser.add_argument("input", help="路书 JSON 文件")
    parser.add_argument("--output", "--output-base", dest="output", help="输出基础路径")
    parser.add_argument("--knowledge-root", help="可选的本地旅行知识目录")
    parser.add_argument("--scope", choices=("personal", "share"), default="personal")
    args = parser.parse_args()
    output = args.output or str(Path(args.input).with_suffix(""))
    try:
        result = build_roadbook(load_json(args.input), output, args.knowledge_root, args.scope)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "error", "message": str(error), "files": {}}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["status"] == "pass" else 2)


if __name__ == "__main__":
    main()
