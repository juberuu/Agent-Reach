"""Helpers for interpreting mcporter's machine-readable config output."""

from __future__ import annotations

import json


class McporterConfigError(ValueError):
    """Raised when mcporter's advertised JSON output is not trustworthy."""


def configured_server_names(output: str) -> set[str]:
    """Return exact configured server names from ``mcporter ... --json``.

    Paths, descriptions, endpoints, and other metadata are deliberately
    ignored: only each server object's ``name`` field is a routing signal.
    """
    try:
        payload = json.loads(output)
    except (json.JSONDecodeError, TypeError) as exc:
        raise McporterConfigError("mcporter 返回的 JSON 无法解析") from exc

    if not isinstance(payload, dict) or not isinstance(payload.get("servers"), list):
        raise McporterConfigError("mcporter JSON 缺少 servers 列表")

    return {
        name.casefold()
        for server in payload["servers"]
        if isinstance(server, dict)
        if isinstance(name := server.get("name"), str) and name.strip()
    }
