# -*- coding: utf-8 -*-
"""Exa semantic search — the search backbone for Agent Reach.

Backend priority:
1. mcporter + Exa MCP server (OAuth, no API key needed)
2. Direct Exa API (requires EXA_API_KEY)

Swap to: Tavily, SerpAPI, or any search API
"""

import os
import json
import shutil
import subprocess
import requests
from .base import Channel, SearchResult
from typing import List


class ExaSearchChannel(Channel):
    name = "exa_search"
    description = "全网语义搜索（同时支持 Reddit/Twitter 搜索）"
    backends = ["Exa MCP Server", "Exa API"]
    tier = 1

    API_URL = "https://api.exa.ai/search"

    def _has_mcporter_exa(self):
        """Check if mcporter CLI is available and exa MCP is configured."""
        if not shutil.which("mcporter"):
            return False
        try:
            result = subprocess.run(
                ["mcporter", "list"],
                capture_output=True, text=True, timeout=10,
            )
            return "exa" in result.stdout
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
        return False  # Search-only channel, doesn't read URLs

    async def read(self, url: str, config=None) -> None:
        raise NotImplementedError("Exa is a search engine, not a reader")

    def check(self, config=None):
        # Priority 1: mcporter
        if self._has_mcporter_exa():
            return "ok", "MCP 已连接，免 Key 直接可用（全网搜索 + Reddit + Twitter）"

        # Priority 2: API key
        key = None
        if config:
            key = config.get("exa_api_key")
        if not key:
            key = os.environ.get("EXA_API_KEY")
        if key:
            return "ok", "API Key 已配置，全网搜索可用"

        return "off", "注册 exa.ai 获取免费 Key，配置一下就能用。或安装 mcporter 免 Key 使用"

    def _get_key(self, config=None) -> str:
        if config:
            key = config.get("exa_api_key")
            if key:
                return key
        key = os.environ.get("EXA_API_KEY")
        if key:
            return key
        return ""

    async def search(self, query: str, config=None, **kwargs) -> List[SearchResult]:
        limit = kwargs.get("limit", 5)

        # Priority 1: mcporter + Exa MCP
        if self._has_mcporter_exa():
            return await self._search_via_mcp(query, limit)

        # Priority 2: Direct API
        api_key = self._get_key(config)
        if not api_key:
            raise ValueError(
                "Exa search not configured.\n\n"
                "Option 1 (easiest): Install mcporter — no API key needed:\n"
                "  npm install -g mcporter && mcporter config add exa https://mcp.exa.ai/mcp\n\n"
                "Option 2: Get a free API key:\n"
                "  Sign up at https://exa.ai (1000 searches/month free)\n"
                "  Then run: agent-reach configure exa-key YOUR_KEY"
            )

        return await self._search_via_api(query, api_key, limit)

    async def _search_via_mcp(self, query: str, limit: int) -> List[SearchResult]:
        """Search via mcporter + Exa MCP server."""
        # Escape quotes in query
        safe_query = query.replace('"', '\\"')
        output = self._mcporter_call(
            f'exa.web_search_exa(query: "{safe_query}", numResults: {min(limit, 10)})',
            timeout=30,
        )

        # mcporter returns formatted text blocks like:
        # Title: ...
        # URL: ...
        # Published Date: ...
        # Text: ...
        results = []
        current = {}

        for line in output.split("\n"):
            line = line.strip()
            if line.startswith("Title: "):
                if current.get("title"):
                    results.append(SearchResult(
                        title=current.get("title", ""),
                        url=current.get("url", ""),
                        snippet=current.get("text", ""),
                        date=current.get("date", ""),
                        score=0,
                    ))
                current = {"title": line[7:]}
            elif line.startswith("URL: "):
                current["url"] = line[5:]
            elif line.startswith("Published Date: "):
                current["date"] = line[16:]
            elif line.startswith("Text: "):
                current["text"] = line[6:]
            elif current.get("text") is not None and line:
                # Continue text block
                current["text"] += " " + line

        # Don't forget the last entry
        if current.get("title"):
            results.append(SearchResult(
                title=current.get("title", ""),
                url=current.get("url", ""),
                snippet=current.get("text", "")[:500],
                date=current.get("date", ""),
                score=0,
            ))

        return results[:limit]

    async def _search_via_api(self, query: str, api_key: str, limit: int) -> List[SearchResult]:
        """Search via direct Exa API."""
        resp = requests.post(
            self.API_URL,
            headers={"Content-Type": "application/json", "x-api-key": api_key},
            json={
                "query": query,
                "numResults": min(limit, 10),
                "type": "auto",
                "contents": {"text": {"maxCharacters": 500}},
            },
            timeout=15,
        )
        resp.raise_for_status()

        results = []
        for item in resp.json().get("results", []):
            results.append(SearchResult(
                title=item.get("title", ""),
                url=item.get("url", ""),
                snippet=item.get("text", ""),
                date=item.get("publishedDate", ""),
                score=item.get("score", 0),
            ))
        return results
