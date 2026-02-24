# -*- coding: utf-8 -*-
"""Environment health checker — powered by channels.

Each channel knows how to check itself. Doctor just collects the results.
"""

from typing import Dict
from agent_eyes.config import Config
from agent_eyes.channels import get_all_channels


def check_all(config: Config) -> Dict[str, dict]:
    """Check all channels and return status dict."""
    results = {}
    for ch in get_all_channels():
        status, message = ch.check(config)
        results[ch.name] = {
            "status": status,
            "name": ch.description,
            "message": message,
            "tier": ch.tier,
            "backends": ch.backends,
        }
    return results


def format_report(results: Dict[str, dict]) -> str:
    """Format results as a readable text report."""
    lines = []
    lines.append("👁️  Agent Eyes Status")
    lines.append("=" * 40)

    ok_count = sum(1 for r in results.values() if r["status"] == "ok")
    total = len(results)

    # Tier 0 — zero config
    lines.append("")
    lines.append("✅ Ready (no setup needed):")
    for key, r in results.items():
        if r["tier"] == 0:
            if r["status"] == "ok":
                lines.append(f"  ✅ {r['name']} — {r['message']}")
            elif r["status"] == "warn":
                lines.append(f"  ⚠️  {r['name']} — {r['message']}")
            elif r["status"] in ("off", "error"):
                lines.append(f"  ❌ {r['name']} — {r['message']}")

    # Tier 1 — needs free key
    tier1 = {k: r for k, r in results.items() if r["tier"] == 1}
    if tier1:
        lines.append("")
        lines.append("🔍 Search (need free Exa API key):")
        for key, r in tier1.items():
            icon = "✅" if r["status"] == "ok" else "⬜"
            lines.append(f"  {icon} {r['name']}")

    # Tier 2 — optional setup
    tier2 = {k: r for k, r in results.items() if r["tier"] == 2}
    if tier2:
        lines.append("")
        lines.append("🔧 Optional (advanced setup):")
        for key, r in tier2.items():
            icon = "✅" if r["status"] == "ok" else "⬜"
            lines.append(f"  {icon} {r['name']} — {r['message']}")

    lines.append("")
    lines.append(f"Status: {ok_count}/{total} channels active")
    if ok_count < total:
        lines.append("Run `agent-eyes setup` to unlock more!")

    return "\n".join(lines)
