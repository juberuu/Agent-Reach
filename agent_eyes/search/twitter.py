# -*- coding: utf-8 -*-
"""Twitter search — uses birdx if available, falls back to Exa."""

import json
import shutil
import subprocess
from loguru import logger
from typing import Any, Dict, List, Optional


async def search_twitter(
    query: str,
    limit: int = 10,
    config=None,
) -> List[Dict[str, Any]]:
    """
    Search Twitter/X content.

    Strategy:
    1. If birdx is installed → use it (full search, timeline, threads)
    2. Otherwise → use Exa with site:x.com (basic search)

    Args:
        query: Search query
        limit: Number of results
        config: Optional Config instance

    Returns:
        List of {author, text, url, likes, retweets, date}
    """
    if shutil.which("birdx"):
        return await _search_birdx(query, limit)
    else:
        return await _search_exa(query, limit, config)


async def _search_birdx(query: str, limit: int) -> List[Dict[str, Any]]:
    """Search Twitter via birdx CLI."""
    logger.info(f"birdx search: {query} (n={limit})")
    try:
        # birdx --json returns [] for search, so use plain text output
        result = subprocess.run(
            ["birdx", "search", query, "-n", str(limit)],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            logger.error(f"birdx search failed: {result.stderr}")
            return []
        return _parse_birdx_text(result.stdout)
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        logger.error(f"birdx search failed: {e}")
        return []


def _parse_birdx_text(text: str) -> List[Dict[str, Any]]:
    """Parse birdx plain text output into structured data.
    
    Format:
        @handle (Display Name):
        Tweet text here
        possibly multiple lines
        date: Mon Feb 24 12:00:00 +0000 2026
        url: https://x.com/handle/status/123
        ──────────────────────────────────────────────────
    """
    results = []
    current: Dict[str, Any] = {}
    text_lines = []

    for line in text.strip().split("\n"):
        line = line.strip()

        # Separator between tweets
        if line.startswith("─"):
            if current:
                if text_lines:
                    current["text"] = "\n".join(text_lines).strip()
                results.append(current)
                current = {}
                text_lines = []
            continue

        # Author line: @handle (Display Name):
        if line.startswith("@") and line.endswith(":") and "(" in line:
            handle = line.split()[0]
            current["author"] = handle
            continue

        # Date line
        if line.startswith("date:"):
            current["date"] = line[5:].strip()
            continue

        # URL line
        if line.startswith("url:"):
            current["url"] = line[4:].strip()
            continue

        # Content line
        if current:
            text_lines.append(line)

    # Last tweet
    if current:
        if text_lines:
            current["text"] = "\n".join(text_lines).strip()
        results.append(current)

    return results


async def _search_exa(query: str, limit: int, config=None) -> List[Dict[str, Any]]:
    """Search Twitter via Exa (site:x.com)."""
    from agent_eyes.search.exa import search_web
    return await search_web(
        f"site:x.com {query}",
        num_results=limit,
        config=config,
    )


async def get_user_tweets(
    username: str,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """Get recent tweets from a user (requires birdx)."""
    if not shutil.which("birdx"):
        raise RuntimeError(
            "birdx not installed. Install: pip install birdx\n"
            "Then configure cookies: agent-eyes setup"
        )
    try:
        result = subprocess.run(
            ["birdx", "user-tweets", f"@{username.lstrip('@')}", "-n", str(limit)],
            capture_output=True, text=True, timeout=30,
        )
        return _parse_birdx_text(result.stdout)
    except subprocess.TimeoutExpired:
        logger.error("birdx timed out")
        return []
