# -*- coding: utf-8 -*-
"""Reddit — search and read via Exa (no direct Reddit API needed)."""

import shutil
import subprocess
from .base import Channel


def _exa_available() -> bool:
    """Return True if mcporter is installed and Exa MCP is configured."""
    mcporter = shutil.which("mcporter")
    if not mcporter:
        return False
    try:
        r = subprocess.run(
            [mcporter, "config", "list"], capture_output=True,
            encoding="utf-8", errors="replace", timeout=5
        )
        return "exa" in r.stdout.lower()
    except Exception:
        return False


class RedditChannel(Channel):
    name = "reddit"
    description = "Reddit 帖子和评论（通过 Exa 搜索和阅读）"
    backends = ["Exa via mcporter"]
    tier = 0

    def can_handle(self, url: str) -> bool:
        from urllib.parse import urlparse
        d = urlparse(url).netloc.lower()
        return "reddit.com" in d or "redd.it" in d

    def check(self, config=None):
        if _exa_available():
            return "ok", "通过 Exa 搜索和阅读 Reddit 内容（免费，无需代理）"
        return "off", (
            "需要 mcporter + Exa MCP。安装：\n"
            "  npm install -g mcporter\n"
            "  mcporter config add exa https://mcp.exa.ai/mcp"
        )
