#!/usr/bin/env python3
"""Select a travel mode and apply transparent personalization policies."""

from copy import deepcopy


VALID_MODES = ("city", "hiking", "road_trip")
MODE_POLICIES = {
    "city": {
        "max_core_experiences_per_day": 4,
        "prefer_single_hotel": True,
        "required_sections": ["food", "rest_windows", "rain_alternatives"],
    },
    "hiking": {
        "required_sections": ["elevation", "supplies", "retreat_points", "stop_conditions"],
        "required_buffer_percent": 20,
    },
    "road_trip": {
        "required_sections": ["driving_segments", "fuel_or_charge", "parking", "stop_conditions"],
        "max_net_driving_hours": 6,
    },
}


def select_mode(request):
    explicit = request.get("primary_mode")
    if explicit:
        if explicit not in VALID_MODES:
            raise ValueError(f"unknown primary_mode: {explicit}")
        secondary = [m for m in request.get("secondary_modes", []) if m in VALID_MODES and m != explicit]
        return {"primary_mode": explicit, "secondary_modes": secondary, "confidence": 1.0, "reasons": ["explicit_request"]}

    haystack = " ".join(str(value) for value in request.values()).lower()
    matches = []
    keywords = {
        "hiking": ("徒步", "登山", "爬山", "trail", "hiking", "比赛"),
        "road_trip": ("自驾", "公路", "road trip", "房车"),
        "city": ("城市", "美食", "建筑", "city walk", "慢游"),
    }
    for mode, terms in keywords.items():
        if any(term in haystack for term in terms):
            matches.append(mode)
    primary = matches[0] if matches else "city"
    return {
        "primary_mode": primary,
        "secondary_modes": [mode for mode in matches[1:] if mode != primary],
        "confidence": 0.8 if matches else 0.5,
        "reasons": ["keyword_inference"] if matches else ["default_city"],
    }


def policy_for(mode, personalization):
    if mode not in MODE_POLICIES:
        raise ValueError(f"unknown mode: {mode}")
    policy = deepcopy(MODE_POLICIES[mode])
    if mode == "city" and personalization.get("pace") == "relaxed":
        policy["max_core_experiences_per_day"] = 3
    return policy


def apply_personalization(roadbook, profile, request):
    result = deepcopy(roadbook)
    personal = result.setdefault("personalization", {})
    personal["pace"] = request.get("pace", personal.get("pace", "balanced"))
    personal["signals"] = sorted(set(personal.get("signals", [])) | set(profile.get("positive_signals", [])))
    personal["avoid_signals"] = sorted(set(profile.get("negative_signals", [])))
    personal["applied_rules"] = sorted(set(personal.get("applied_rules", [])) | set(profile.get("rules", [])))
    personal["request_overrides_profile"] = True
    return result
