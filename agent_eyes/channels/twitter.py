# -*- coding: utf-8 -*-
"""Twitter/X — via birdx CLI (free) or Jina Reader fallback.

Backend: birdx (https://github.com/runesleo/birdx) for search/timeline
         Jina Reader for single tweets
Swap to: any Twitter access tool
"""

import shutil
import subprocess
from urllib.parse import urlparse
from .base import Channel, ReadResult, SearchResult
from typing import List
import requests


class TwitterChannel(Channel):
    name = "twitter"
    description = "Twitter/X posts"
    backends = ["birdx", "Jina Reader"]
    tier = 0  # Single tweet reading is zero-config

    def can_handle(self, url: str) -> bool:
        domain = urlparse(url).netloc.lower()
        return "x.com" in domain or "twitter.com" in domain

    def check(self, config=None):
        # Basic reading always works (Jina fallback)
        if shutil.which("birdx"):
            return "ok", "Full access (search + timeline + threads)"
        return "ok", "Read-only (single tweets via Jina). Install birdx for search + timelines"
        return "ok", "Jina Reader (single tweets only)"

    async def read(self, url: str, config=None) -> ReadResult:
        # Try birdx first
        if shutil.which("birdx"):
            return await self._read_birdx(url)
        # Fallback: Jina Reader
        return await self._read_jina(url)

    async def _read_birdx(self, url: str) -> ReadResult:
        result = subprocess.run(
            ["birdx", "read", url],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            return await self._read_jina(url)

        text = result.stdout.strip()
        # Extract author from first line
        author = ""
        lines = text.split("\n")
        if lines and lines[0].startswith("@"):
            author = lines[0].split()[0]

        return ReadResult(
            title=text[:100],
            content=text,
            url=url,
            author=author,
            platform="twitter",
        )

    async def _read_jina(self, url: str) -> ReadResult:
        resp = requests.get(
            f"https://r.jina.ai/{url}",
            headers={"Accept": "text/markdown"},
            timeout=15,
        )
        resp.raise_for_status()
        text = resp.text
        title = text[:100] if text else url

        return ReadResult(
            title=title,
            content=text,
            url=url,
            platform="twitter",
        )

    async def search(self, query: str, config=None, **kwargs) -> List[SearchResult]:
        limit = kwargs.get("limit", 10)

        if shutil.which("birdx"):
            return await self._search_birdx(query, limit)

        # Fallback to Exa
        return await self._search_exa(query, limit, config)

    async def _search_birdx(self, query: str, limit: int) -> List[SearchResult]:
        try:
            result = subprocess.run(
                ["birdx", "search", query, "-n", str(limit)],
                capture_output=True, text=True, timeout=30,
            )
            if result.returncode != 0:
                return []

            return self._parse_birdx_output(result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return []

    def _parse_birdx_output(self, text: str) -> List[SearchResult]:
        """Parse birdx text output into SearchResults."""
        results = []
        current = {}
        text_lines = []

        for line in text.strip().split("\n"):
            line = line.strip()
            if line.startswith("─"):
                if current:
                    current["text"] = "\n".join(text_lines).strip()
                    results.append(SearchResult(
                        title=current.get("text", "")[:80],
                        url=current.get("url", ""),
                        snippet=current.get("text", ""),
                        author=current.get("author", ""),
                        date=current.get("date", ""),
                    ))
                    current = {}
                    text_lines = []
                continue
            if line.startswith("@") and line.endswith(":") and "(" in line:
                current["author"] = line.split()[0]
                continue
            if line.startswith("date:"):
                current["date"] = line[5:].strip()
                continue
            if line.startswith("url:"):
                current["url"] = line[4:].strip()
                continue
            if current is not None:
                text_lines.append(line)

        if current and text_lines:
            current["text"] = "\n".join(text_lines).strip()
            results.append(SearchResult(
                title=current.get("text", "")[:80],
                url=current.get("url", ""),
                snippet=current.get("text", ""),
                author=current.get("author", ""),
                date=current.get("date", ""),
            ))
        return results

    async def _search_exa(self, query: str, limit: int, config=None) -> List[SearchResult]:
        from agent_eyes.channels.exa_search import ExaSearchChannel
        exa = ExaSearchChannel()
        return await exa.search(f"site:x.com {query}", config=config, limit=limit)
