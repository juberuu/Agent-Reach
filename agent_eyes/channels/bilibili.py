# -*- coding: utf-8 -*-
"""Bilibili — via public API (free, no config needed).

Backend: Bilibili public API
Swap to: any Bilibili access method
"""

import requests
from urllib.parse import urlparse, parse_qs
from .base import Channel, ReadResult


class BilibiliChannel(Channel):
    name = "bilibili"
    description = "Bilibili video info and subtitles"
    backends = ["Bilibili API"]
    tier = 0

    def can_handle(self, url: str) -> bool:
        domain = urlparse(url).netloc.lower()
        return "bilibili.com" in domain or "b23.tv" in domain

    def check(self, config=None):
        proxy = config.get("bilibili_proxy") if config else None
        if proxy:
            return "ok", "Via proxy"
        # Detect if we're on a server (same logic as cli._detect_environment)
        import os
        indicators = [
            os.path.exists("/var/run/docker.sock"),
            os.path.exists("/etc/cloud"),
            "SSH_CONNECTION" in os.environ,
            "container" in os.environ.get("container", ""),
        ]
        is_server = any(indicators)
        if is_server:
            return "warn", "May be blocked on servers. Fix: agent-eyes configure proxy URL"
        return "ok", "Local access"

    async def read(self, url: str, config=None) -> ReadResult:
        # Proxy support (Bilibili blocks server IPs)
        proxy = config.get("bilibili_proxy") if config else None
        proxies = {"http": proxy, "https": proxy} if proxy else None

        # Extract BV id from URL
        path = urlparse(url).path
        bv_id = ""
        for part in path.split("/"):
            if part.startswith("BV"):
                bv_id = part
                break

        if not bv_id:
            # Fallback to Jina Reader
            from agent_eyes.channels.web import WebChannel
            return await WebChannel().read(url, config)

        # Get video info
        resp = requests.get(
            "https://api.bilibili.com/x/web-interface/view",
            params={"bvid": bv_id},
            headers={"User-Agent": "Mozilla/5.0"},
            proxies=proxies,
            timeout=15,
        )
        resp.raise_for_status()
        api_data = resp.json()

        # Check for API errors (IP blocked, video not found, etc.)
        if api_data.get("code") != 0:
            msg = api_data.get("message", "Unknown error")
            # Bilibili returns -404 when server IP is blocked
            if api_data.get("code") in (-404, -403, -412):
                return ReadResult(
                    title=f"Bilibili: {bv_id}",
                    content=f"⚠️ Bilibili blocked this request ({msg}). "
                            f"This usually means the server IP is blocked. "
                            f"Try: agent-eyes configure proxy http://user:pass@ip:port",
                    url=url,
                    platform="bilibili",
                )
            return ReadResult(
                title=f"Bilibili: {bv_id}",
                content=f"Bilibili API error: {msg} (code: {api_data.get('code')})",
                url=url,
                platform="bilibili",
            )

        data = api_data.get("data", {})

        title = data.get("title", "")
        desc = data.get("desc", "")
        author = data.get("owner", {}).get("name", "")

        # Try to get subtitles
        subtitle_text = ""
        subtitle_list = data.get("subtitle", {}).get("list", [])
        if subtitle_list:
            sub_url = subtitle_list[0].get("subtitle_url", "")
            if sub_url:
                if sub_url.startswith("//"):
                    sub_url = "https:" + sub_url
                sr = requests.get(sub_url, timeout=10)
                if sr.ok:
                    sub_data = sr.json()
                    lines = [item.get("content", "") for item in sub_data.get("body", [])]
                    subtitle_text = "\n".join(lines)

        content = desc
        if subtitle_text:
            content += f"\n\n## Transcript\n{subtitle_text}"

        return ReadResult(
            title=title,
            content=content,
            url=url,
            author=author,
            platform="bilibili",
            extra={"view": data.get("stat", {}).get("view", 0),
                   "like": data.get("stat", {}).get("like", 0)},
        )
