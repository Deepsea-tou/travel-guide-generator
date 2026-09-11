#!/usr/bin/env python3
"""Migrate legacy travel-guide data to the Travel Roadbook v2 contract."""

from copy import deepcopy


def migrate_to_v2(source):
    """Return a v2 copy of *source* without modifying the caller's object."""
    if not isinstance(source, dict):
        raise ValueError("guide root must be an object")
    data = deepcopy(source)
    version = str(data.get("schema_version", "1.0"))
    if version == "2.0":
        return data
    if version != "1.0":
        raise ValueError(f"unsupported schema_version: {version}")

    preferences = data.setdefault("preferences", {})
    primary_mode = preferences.pop("primary_mode", "city")
    data["schema_version"] = "2.0"
    data.setdefault("trip", {"primary_mode": primary_mode, "secondary_modes": []})
    data.setdefault(
        "personalization",
        {
            "pace": preferences.get("pace", "balanced"),
            "signals": [],
            "applied_rules": [],
        },
    )
    data.setdefault(
        "privacy",
        {"output_scope": "personal", "private_paths": [], "sensitive_fields": []},
    )
    data.setdefault("quality", {"status": "unchecked", "checks": []})
    return data
