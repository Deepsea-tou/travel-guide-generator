#!/usr/bin/env python3
"""Create a publishable roadbook without private fields or local provenance."""

from copy import deepcopy
import json
import re


class PrivacyError(ValueError):
    """Raised when a share payload still contains private material."""


LOCAL_KEYS = {
    "source_path", "local_path", "knowledge_root", "private_paths",
    "raw_content", "conversation_text", "cookie", "api_key",
}
_DROP = object()
_URL_PATTERN = re.compile(r"https?://[^\s]+", re.IGNORECASE)
_FILE_URL_PATTERN = re.compile(r"\bfile://", re.IGNORECASE)
_POSIX_PATH_PATTERN = re.compile(r'''(?:^|[\s"'(=])/(?!/)(?:[^/\s"'<>]+/)+[^/\s"'<>]+''')
_WINDOWS_PATH_PATTERN = re.compile(r'''(?:^|[\s"'(=])[A-Za-z]:[\\/](?:[^\\/\s"'<>]+[\\/])*[^\\/\s"'<>]+''')


def contains_local_path(value):
    """Return True when nested data contains a local absolute filesystem path."""
    if isinstance(value, dict):
        return any(contains_local_path(key) or contains_local_path(child) for key, child in value.items())
    if isinstance(value, list):
        return any(contains_local_path(child) for child in value)
    if not isinstance(value, str):
        return False
    if _FILE_URL_PATTERN.search(value):
        return True
    without_urls = _URL_PATTERN.sub("", value)
    return bool(_POSIX_PATH_PATTERN.search(without_urls) or _WINDOWS_PATH_PATTERN.search(without_urls))


def _clean(value, sensitive_fields):
    if isinstance(value, dict):
        if value.get("privacy") == "private":
            return _DROP
        cleaned = {}
        for key, child in value.items():
            if key in sensitive_fields or key.lower() in LOCAL_KEYS:
                continue
            result = _clean(child, sensitive_fields)
            if result is _DROP:
                continue
            if result in ({}, []) and child not in ({}, []):
                continue
            cleaned[key] = result
        return cleaned
    if isinstance(value, list):
        return [result for child in value if (result := _clean(child, sensitive_fields)) is not _DROP]
    return deepcopy(value)


def _assert_publishable(data, sensitive_values):
    encoded = json.dumps(data, ensure_ascii=False)
    markers = ("file:" + "//", ".chatgpt" + "-projects")
    if any(marker in encoded for marker in markers) or contains_local_path(data):
        raise PrivacyError("share output contains a local path")
    if any(value and str(value) in encoded for value in sensitive_values):
        raise PrivacyError("share output contains a configured sensitive value")


def _scalar_values(value):
    if isinstance(value, dict):
        return [item for child in value.values() for item in _scalar_values(child)]
    if isinstance(value, list):
        return [item for child in value for item in _scalar_values(child)]
    return [value]


def _collect_sensitive_values(value, sensitive_fields):
    if isinstance(value, dict):
        collected = []
        for key, child in value.items():
            if key in sensitive_fields:
                collected.extend(_scalar_values(child))
            else:
                collected.extend(_collect_sensitive_values(child, sensitive_fields))
        return collected
    if isinstance(value, list):
        return [item for child in value for item in _collect_sensitive_values(child, sensitive_fields)]
    return []


def sanitize_for_share(source):
    """Return a recursively sanitized copy and reject residual local paths."""
    if not isinstance(source, dict):
        raise PrivacyError("roadbook root must be an object")
    privacy = source.get("privacy", {})
    sensitive_fields = set(privacy.get("sensitive_fields", []))
    sensitive_values = _collect_sensitive_values(source, sensitive_fields)
    result = _clean(source, sensitive_fields)
    result.setdefault("privacy", {})
    result["privacy"] = {"output_scope": "share", "private_paths": [], "sensitive_fields": []}
    _assert_publishable(result, sensitive_values)
    return result
