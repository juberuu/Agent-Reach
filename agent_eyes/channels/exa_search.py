# -*- coding: utf-8 -*-
"""Exa semantic search — the search backbone for Agent Eyes.

Backend: Exa API (https://exa.ai) — free 1000 searches/month
Swap to: Tavily, SerpAPI, or any search API
"""

import os
import requests
from .base import Channel, SearchResult
from typing import List


class ExaSearchChannel(Channel):
    name = "exa_search"
    description = "全网语义搜索（同时支持 Reddit/Twitter 搜索）"
    backends = ["Exa API"]
    requires_config = ["exa_api_key"]
    tier = 1

    API_URL = "https://api.exa.ai/search"

    def can_handle(self, url: str) -> bool:
        return False  # Search-only channel, doesn't read URLs

    async def read(self, url: str, config=None) -> None:
        raise NotImplementedError("Exa is a search engine, not a reader")

    def _get_key(self, config=None) -> str:
        if config:
            key = config.get("exa_api_key")
            if key:
                return key
        key = os.environ.get("EXA_API_KEY")
        if key:
            return key
        raise ValueError(
            "Exa API key not configured.\n"
            "Get a free key at https://exa.ai (1000 searches/month free)\n"
            "Then run: agent-eyes setup"
        )

    async def search(self, query: str, config=None, **kwargs) -> List[SearchResult]:
        api_key = self._get_key(config)
        limit = kwargs.get("limit", 5)

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
