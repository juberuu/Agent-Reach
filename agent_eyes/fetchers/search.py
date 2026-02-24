# -*- coding: utf-8 -*-
"""Search fetcher — semantic web search via Exa API.

Requires EXA_API_KEY env var. Get a free key at https://exa.ai
"""

import os
import requests
from loguru import logger
from typing import Dict, Any, List, Optional


EXA_API_URL = "https://api.exa.ai/search"


async def search_web(
    query: str,
    num_results: int = 5,
    search_type: str = "auto",
) -> List[Dict[str, Any]]:
    """
    Search the web using Exa semantic search.

    Args:
        query: Search query (supports site: prefix, e.g. "site:reddit.com AI agent")
        num_results: Number of results to return (default 5, max 10)
        search_type: "auto" (default) or "neural" or "keyword"

    Returns:
        List of search results with title, url, snippet
    """
    api_key = os.environ.get("EXA_API_KEY")
    if not api_key:
        raise ValueError(
            "EXA_API_KEY not set. Get a free key at https://exa.ai\n"
            "Then: export EXA_API_KEY=your_key_here"
        )

    logger.info(f"Exa search: {query} (n={num_results})")

    resp = requests.post(
        EXA_API_URL,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
        },
        json={
            "query": query,
            "numResults": min(num_results, 10),
            "type": search_type,
            "contents": {
                "text": {"maxCharacters": 500},
            },
        },
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()

    results = []
    for item in data.get("results", []):
        results.append({
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "snippet": item.get("text", ""),
            "published_date": item.get("publishedDate", ""),
            "score": item.get("score", 0),
        })

    return results


async def search_reddit_via_exa(
    query: str,
    subreddit: Optional[str] = None,
    num_results: int = 10,
) -> List[Dict[str, Any]]:
    """
    Search Reddit content via Exa (bypasses Reddit IP blocks).

    Args:
        query: Search query
        subreddit: Optional subreddit to limit search (e.g. "LocalLLaMA")
        num_results: Number of results

    Returns:
        List of Reddit posts found
    """
    if subreddit:
        full_query = f"site:reddit.com/r/{subreddit} {query}"
    else:
        full_query = f"site:reddit.com {query}"

    return await search_web(full_query, num_results=num_results)
