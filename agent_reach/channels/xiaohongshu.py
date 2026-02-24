# -*- coding: utf-8 -*-
"""XiaoHongShu (小红书) — via MCP server or cookie-based web scraping.

Backend priority:
1. mcporter + xiaohongshu MCP server (internal API, reliable)
2. Direct web scraping with cookies (fallback, may be blocked by anti-bot)

Swap to: any XHS access method
"""

import re
import json
import shutil
import subprocess
import requests
from urllib.parse import urlparse
from .base import Channel, ReadResult, SearchResult
from typing import List


class XiaoHongShuChannel(Channel):
    name = "xiaohongshu"
    description = "小红书笔记"
    backends = ["XHS MCP Server", "XHS Web API"]
    tier = 2

    def _has_mcporter(self):
        """Check if mcporter CLI is available and xiaohongshu MCP is configured."""
        if not shutil.which("mcporter"):
            return False
        try:
            result = subprocess.run(
                ["mcporter", "list"],
                capture_output=True, text=True, timeout=10,
            )
            return "xiaohongshu" in result.stdout
        except Exception:
            return False

    def _mcporter_call(self, tool_call: str, timeout: int = 30) -> str:
        """Call an MCP tool via mcporter and return the output."""
        result = subprocess.run(
            ["mcporter", "call", tool_call],
            capture_output=True, text=True, timeout=timeout,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr or result.stdout)
        return result.stdout

    def can_handle(self, url: str) -> bool:
        domain = urlparse(url).netloc.lower()
        return "xiaohongshu.com" in domain or "xhslink.com" in domain

    def check(self, config=None):
        if self._has_mcporter():
            # Check login status
            try:
                output = self._mcporter_call("xiaohongshu.check_login_status()")
                if "已登录" in output or "logged" in output.lower():
                    return "ok", "MCP 已连接，完整可用（阅读、搜索、发帖、评论、点赞）"
                else:
                    return "warn", "MCP 已连接但未登录。运行 agent-reach 后用小红书扫码登录"
            except Exception:
                return "warn", "mcporter 可用但小红书 MCP 连接失败，检查服务是否在运行"

        cookie = config.get("xhs_cookie") if config else None
        if cookie:
            return "ok", "Cookie 已配置（注意：服务器端可能被反爬拦截）"
        return "off", "需要配置 Cookie 才能访问。导入浏览器 Cookie 即可：agent-reach configure --from-browser chrome"

    async def read(self, url: str, config=None) -> ReadResult:
        note_id = self._extract_note_id(url)

        # Priority 1: mcporter + MCP server
        if self._has_mcporter() and note_id:
            try:
                return await self._read_via_mcp(note_id, url)
            except Exception:
                pass  # Fall through to web scraping

        # Priority 2: Web scraping with cookies
        cookie = config.get("xhs_cookie") if config else None
        if not cookie:
            return ReadResult(
                title="XiaoHongShu",
                content="⚠️ XiaoHongShu requires cookies to access.\n"
                        "Set up: agent-reach configure xhs-cookie \"YOUR_COOKIE_STRING\"\n"
                        "How to get it: install Cookie-Editor extension → go to xiaohongshu.com → Export → Header String\n\n"
                        "💡 Tip: If you have mcporter + xiaohongshu MCP server, it works without cookies.\n"
                        "Install: pip install mcporter && mcporter config add xiaohongshu http://localhost:18060/mcp",
                url=url,
                platform="xiaohongshu",
            )

        if not note_id:
            from agent_reach.channels.web import WebChannel
            return await WebChannel().read(url, config)

        return await self._read_via_web(note_id, url, cookie)

    async def search(self, query: str, config=None, **kwargs) -> List[SearchResult]:
        """Search XiaoHongShu via MCP server."""
        if not self._has_mcporter():
            raise ValueError(
                "XiaoHongShu search requires mcporter + xiaohongshu MCP server.\n"
                "Install: pip install mcporter && mcporter config add xiaohongshu http://localhost:18060/mcp"
            )

        limit = kwargs.get("limit", 10)
        output = self._mcporter_call(
            f'xiaohongshu.search_feeds(keyword: "{query}")',
            timeout=30,
        )

        results = []
        try:
            data = json.loads(output)
            for item in data.get("feeds", [])[:limit]:
                card = item.get("noteCard", {})
                user = card.get("user", {})
                interact = card.get("interactInfo", {})
                results.append(SearchResult(
                    title=card.get("displayTitle", ""),
                    url=f"https://www.xiaohongshu.com/explore/{item.get('id', '')}",
                    snippet=f"👤 {user.get('nickname', '')} · ❤ {interact.get('likedCount', '0')}",
                    score=0,
                ))
        except (json.JSONDecodeError, KeyError):
            pass

        return results

    async def _read_via_mcp(self, note_id: str, url: str) -> ReadResult:
        """Read a note via MCP server: search → get xsec_token → get detail."""
        # Step 1: Get xsec_token by listing feeds or searching
        # Try to find the note in recent feeds first
        output = self._mcporter_call("xiaohongshu.list_feeds()", timeout=15)
        xsec_token = None

        try:
            data = json.loads(output)
            for feed in data.get("feeds", []):
                if feed.get("id") == note_id:
                    xsec_token = feed.get("xsecToken", "")
                    break
        except (json.JSONDecodeError, KeyError):
            pass

        # If not found in feeds, search for it
        if not xsec_token:
            # Use a generic token - XHS MCP may accept it
            xsec_token = ""

        if not xsec_token:
            return ReadResult(
                title="XiaoHongShu",
                content=f"⚠️ 无法获取笔记 {note_id} 的访问令牌。\n"
                        "请先通过首页或搜索找到这篇笔记。",
                url=url,
                platform="xiaohongshu",
            )

        # Step 2: Get detail
        output = self._mcporter_call(
            f'xiaohongshu.get_feed_detail(feed_id: "{note_id}", xsec_token: "{xsec_token}")',
            timeout=15,
        )

        # Parse MCP output (it's typically formatted text, not JSON)
        title = ""
        content = output.strip()
        author = ""

        # Try to extract structured info if it's JSON
        try:
            data = json.loads(output)
            if isinstance(data, dict):
                title = data.get("title", data.get("displayTitle", ""))
                content = data.get("desc", data.get("content", output))
                author = data.get("user", {}).get("nickname", "")
        except (json.JSONDecodeError, ValueError):
            # MCP returns plain text - use as-is
            lines = content.split("\n")
            if lines:
                title = lines[0][:80]

        return ReadResult(
            title=title or f"XHS Note {note_id}",
            content=content,
            url=url,
            author=author,
            platform="xiaohongshu",
        )

    async def _read_via_web(self, note_id: str, url: str, cookie: str) -> ReadResult:
        """Read a note via direct web scraping (fallback)."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Cookie": cookie,
            "Referer": "https://www.xiaohongshu.com/",
        }

        resp = requests.get(
            f"https://www.xiaohongshu.com/explore/{note_id}",
            headers=headers,
            timeout=15,
            allow_redirects=False,
        )

        # Check for anti-bot redirect
        if resp.status_code in (301, 302):
            location = resp.headers.get("Location", "")
            if "404" in location or "sec_" in location:
                return ReadResult(
                    title="XiaoHongShu",
                    content="⚠️ XiaoHongShu blocked this request (anti-bot protection).\n"
                            "Web scraping doesn't work from server IPs.\n\n"
                            "💡 Better approach: use mcporter + xiaohongshu MCP server:\n"
                            "  mcporter config add xiaohongshu http://localhost:18060/mcp\n"
                            "  Then agent-reach will use the MCP API automatically.",
                    url=url,
                    platform="xiaohongshu",
                )

        resp.raise_for_status()
        html = resp.text

        title, content, author = self._parse_html(html)

        return ReadResult(
            title=title or f"XHS Note {note_id}",
            content=content or "Could not extract content. Cookie may be expired.",
            url=url,
            author=author,
            platform="xiaohongshu",
        )

    def _extract_note_id(self, url: str) -> str:
        """Extract note ID from various XHS URL formats."""
        path = urlparse(url).path
        parts = path.strip("/").split("/")
        if parts:
            return parts[-1]
        return ""

    def _parse_html(self, html: str):
        """Extract title, content, author from XHS HTML."""
        title = ""
        content = ""
        author = ""

        match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*?})\s*</script>', html, re.DOTALL)
        if match:
            try:
                state = json.loads(match.group(1).replace('undefined', 'null'))
                note_data = state.get("note", {}).get("noteDetailMap", {})
                if note_data:
                    first_note = list(note_data.values())[0]
                    note = first_note.get("note", {})
                    title = note.get("title", "")
                    content = note.get("desc", "")
                    author = note.get("user", {}).get("nickname", "")
            except (json.JSONDecodeError, KeyError, IndexError):
                pass

        if not title:
            m = re.search(r'<title>(.*?)</title>', html)
            if m:
                title = m.group(1)

        if not content:
            m = re.search(r'<meta name="description" content="(.*?)"', html)
            if m:
                content = m.group(1)

        return title, content, author
