#!/usr/bin/env python3
"""Reduce allowlisted local travel notes to non-verbatim preference signals."""

from pathlib import Path


SUPPORTED_FILES = (
    "旅行偏好模型.md",
    "旅行体验评分体系.md",
    "合肥驻场旅行地图.md",
    "周末旅行体系.md",
    "装备体系.md",
    "中国徒步地图.md",
    "旅行愿望清单.md",
)

POSITIVE_TERMS = {
    "森林": "nature.forest",
    "湖泊": "nature.lake",
    "山脊": "nature.ridge",
    "云海": "nature.cloud_sea",
    "慢行": "pace.slow",
    "美食": "interest.food",
    "建筑": "interest.architecture",
    "摄影": "interest.photography",
    "徒步": "activity.hiking",
    "高铁": "transport.rail",
    "公共交通": "transport.public",
    "自驾": "transport.drive",
}
NEGATIVE_TERMS = {
    "排队": "friction.queues",
    "频繁搬酒店": "friction.hotel_moves",
    "商业化": "friction.commercialized",
    "赶路": "friction.rushed",
    "长下坡": "fatigue.long_descent",
}


def empty_profile():
    return {
        "positive_signals": [],
        "negative_signals": [],
        "weights": {},
        "rules": [],
        "files_considered": 0,
    }


def extract_profile(root):
    """Read direct allowlisted Markdown files and return derived signals only."""
    root = Path(root).expanduser().resolve()
    if not root.is_dir():
        raise ValueError("knowledge root must be an existing directory")

    profile = empty_profile()
    content_parts = []
    for filename in SUPPORTED_FILES:
        path = root / filename
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8").strip()
        if content:
            content_parts.append(content)
            profile["files_considered"] += 1
    content = "\n".join(content_parts)
    profile["positive_signals"] = sorted(
        signal for term, signal in POSITIVE_TERMS.items() if term in content
    )
    profile["negative_signals"] = sorted(
        signal for term, signal in NEGATIVE_TERMS.items() if term in content
    )
    profile["weights"] = {signal: 1 for signal in profile["positive_signals"]}
    if "friction.hotel_moves" in profile["negative_signals"]:
        profile["rules"].append("prefer_single_hotel")
    if "friction.queues" in profile["negative_signals"]:
        profile["rules"].append("avoid_peak_queues")
    return profile
