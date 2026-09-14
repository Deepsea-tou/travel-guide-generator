#!/usr/bin/env python3
"""Quality, safety, freshness, and privacy checks for roadbook v2."""

from copy import deepcopy
from datetime import date, datetime
import json

try:
    from .roadbook_modes import policy_for
    from .sanitize_share_version import contains_local_path
    from .validate_guide import issue, validate_guide
except ImportError:
    from roadbook_modes import policy_for
    from sanitize_share_version import contains_local_path
    from validate_guide import issue, validate_guide


def _add(collection, level, code, message, path):
    collection.append(issue(level, code, message, path))


def _legacy_report(data, today):
    legacy = deepcopy(data)
    legacy["schema_version"] = "1.0"
    for source in legacy.get("sources", []):
        if source.get("verified_at") and not source.get("checked_at"):
            source["checked_at"] = source["verified_at"]
    return validate_guide(legacy, today=today)


def _validate_sources(data, errors, warnings, today):
    for index, source in enumerate(data.get("sources", [])):
        path = f"sources[{index}]"
        verified = source.get("verified_at") or source.get("checked_at")
        if source.get("dynamic") and not verified and not source.get("estimated"):
            _add(errors, "error", "source.verification.missing", "动态事实缺少核实日期", path)
            continue
        if not verified:
            continue
        try:
            age = (today - datetime.strptime(verified, "%Y-%m-%d").date()).days
        except (TypeError, ValueError):
            _add(errors, "error", "source.verification.invalid", "核实日期格式应为 YYYY-MM-DD", path)
            continue
        limit = 3 if source.get("category") in {"weather", "disruption"} else 30
        if source.get("dynamic") and age > limit:
            _add(warnings, "warning", "source.stale", f"动态信息已超过 {limit} 天，临行前复核", path)


def _validate_mode(data, errors, warnings):
    mode = data.get("trip", {}).get("primary_mode")
    try:
        policy = policy_for(mode, data.get("personalization", {}))
    except ValueError as error:
        _add(errors, "error", "trip.mode.invalid", str(error), "trip.primary_mode")
        return
    days = data.get("days", [])
    for index, day in enumerate(days):
        base = f"days[{index}]"
        if mode == "city":
            count = len(day.get("items", []))
            if count > policy["max_core_experiences_per_day"]:
                _add(warnings, "warning", "city.schedule.dense", "核心体验过多，建议降低密度", base)
            for field in ("rest_windows", "rain_alternatives"):
                if not day.get(field):
                    _add(warnings, "warning", f"city.{field}.missing", f"城市行程缺少 {field}", base)
        elif mode == "hiking":
            for field in ("elevation", "supplies", "water", "retreat_points", "latest_pass", "mandatory_gear", "stop_conditions"):
                if not day.get(field):
                    _add(errors, "error", f"hiking.{field}.missing", f"徒步日缺少 {field}", base)
        elif mode == "road_trip":
            for field in ("driving_segments", "fuel_or_charge", "parking", "stop_conditions"):
                if not day.get(field):
                    _add(errors, "error", f"road_trip.{field}.missing", f"自驾日缺少 {field}", base)
            minutes = sum(int(segment.get("duration_min", 0)) for segment in day.get("driving_segments", []))
            if minutes > policy["max_net_driving_hours"] * 60:
                _add(warnings, "warning", "road_trip.driving.excessive", "单日净驾驶超过建议上限", base)


def _validate_privacy(data, errors):
    if data.get("privacy", {}).get("output_scope") != "share":
        return
    privacy = data.get("privacy", {})
    if "sensitive_fields" not in privacy or "private_paths" not in privacy:
        _add(errors, "error", "privacy.inventory.missing", "分享版缺少明确的敏感字段与路径清单", "privacy")
    images = data.get("images", [])
    if images and any(not image.get("metadata_checked") for image in images):
        _add(errors, "error", "privacy.image_metadata.unchecked", "分享图片尚未完成元数据检查", "images")
    encoded = json.dumps(data, ensure_ascii=False)
    markers = ("file:" + "//", ".chatgpt" + "-projects")
    if any(marker in encoded for marker in markers) or contains_local_path(data):
        _add(errors, "error", "privacy.local_path", "分享版包含本地路径", "$")


def _validate_shapes(data, errors):
    budget = data.get("budget")
    if budget is None:
        return
    if not isinstance(budget, dict):
        _add(errors, "error", "budget.invalid", "budget 必须是对象", "budget")
        return
    selected = budget.get("selected")
    profiles = budget.get("profiles", {})
    if selected:
        if not isinstance(profiles, dict) or not isinstance(profiles.get(selected, {}), dict):
            _add(errors, "error", "budget.profile.invalid", "所选预算档必须是对象", "budget.profiles")
            return
        profile = profiles.get(selected, {})
    else:
        profile = budget
    if "categories" in profile and not isinstance(profile["categories"], dict):
        _add(errors, "error", "budget.categories.invalid", "预算分类必须是对象", "budget.categories")


def validate_roadbook(data, today=None):
    today = today or date.today()
    errors, warnings, conflicts = [], [], []
    if not isinstance(data, dict):
        return {"valid": False, "status": "fail", "errors": [issue("error", "root.invalid", "路书根节点必须是对象", "$")], "warnings": [], "conflicts": [], "checks": []}
    if data.get("schema_version") != "2.0":
        _add(errors, "error", "schema.version", "schema_version 必须为 2.0", "schema_version")
    legacy = _legacy_report(data, today)
    errors.extend(legacy["errors"])
    warnings.extend(legacy["warnings"])
    conflicts.extend(legacy["conflicts"])
    _validate_sources(data, errors, warnings, today)
    _validate_mode(data, errors, warnings)
    _validate_privacy(data, errors)
    _validate_shapes(data, errors)
    valid = not errors and not conflicts
    return {
        "valid": valid,
        "status": "pass" if valid else "fail",
        "errors": errors,
        "warnings": warnings,
        "conflicts": conflicts,
        "checks": ["schema", "schedule", "sources", "mode", "privacy"],
    }
