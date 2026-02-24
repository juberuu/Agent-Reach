# -*- coding: utf-8 -*-
"""
x-reader MCP Server — expose content reading as MCP tools.

Usage:
    python mcp_server.py                    # stdio transport (for Claude Code)
    python mcp_server.py --transport sse    # SSE transport (for web clients)

Claude Code config (~/.claude/claude_desktop_config.json):
    {
        "mcpServers": {
            "agent-eyes": {
                "command": "python",
                "args": ["/path/to/x-reader/mcp_server.py"]
            }
        }
    }
"""

import asyncio
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

from agent_eyes.reader import UniversalReader
from agent_eyes.schema import UnifiedInbox

mcp = FastMCP(
    "agent-eyes",
    instructions="Give your AI Agent eyes to see the entire internet. Search, read, and extract content from any platform.",
)

reader = UniversalReader(inbox=UnifiedInbox())


@mcp.tool()
async def read_url(url: str) -> str:
    """
    Read content from any URL and return structured result.

    Supports: YouTube, Bilibili, X/Twitter, WeChat, Xiaohongshu,
    Telegram, RSS, and any generic web page.

    Returns JSON with: title, content, url, source_type, platform metadata.
    """
    import json

    content = await reader.read(url)
    result = content.to_dict()
    # Keep it readable
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def read_batch(urls: list[str]) -> str:
    """
    Read multiple URLs concurrently. Returns JSON array of results.

    Failed URLs are logged but don't block other results.
    """
    import json

    contents = await reader.read_batch(urls)
    results = [c.to_dict() for c in contents]
    return json.dumps(results, ensure_ascii=False, indent=2)


@mcp.tool()
async def list_inbox() -> str:
    """
    List all items in the content inbox.

    Returns JSON array of previously fetched content.
    """
    import json

    items = [item.to_dict() for item in reader.inbox.items]
    return json.dumps(items, ensure_ascii=False, indent=2)


@mcp.tool()
async def detect_platform(url: str) -> str:
    """
    Detect which platform a URL belongs to.

    Returns the platform name: youtube, bilibili, twitter, wechat,
    xhs, reddit, github, telegram, rss, or generic.
    """
    return reader._detect_platform(url)


# ==================== Search Tools (NEW in Agent Eyes) ====================

@mcp.tool()
async def search(query: str, num_results: int = 5) -> str:
    """
    Search the entire web using semantic search (powered by Exa).

    Great for finding articles, blog posts, discussions on any topic.
    Supports site: prefix, e.g. "site:reddit.com AI agent" to limit to specific sites.

    Requires EXA_API_KEY env var. Get a free key at https://exa.ai

    Args:
        query: Search query
        num_results: Number of results (1-10, default 5)
    """
    import json
    from agent_eyes.fetchers.search import search_web

    results = await search_web(query, num_results=num_results)
    return json.dumps(results, ensure_ascii=False, indent=2)


@mcp.tool()
async def search_reddit(query: str, subreddit: str = "", limit: int = 10) -> str:
    """
    Search Reddit posts. Bypasses Reddit IP blocks via Exa.

    Args:
        query: Search query
        subreddit: Optional subreddit name (e.g. "LocalLLaMA"). Empty = all of Reddit.
        limit: Number of results (default 10)
    """
    import json
    from agent_eyes.fetchers.search import search_reddit_via_exa

    sub = subreddit if subreddit else None
    results = await search_reddit_via_exa(query, subreddit=sub, num_results=limit)
    return json.dumps(results, ensure_ascii=False, indent=2)


@mcp.tool()
async def search_github(query: str, limit: int = 5) -> str:
    """
    Search GitHub repositories by keyword.

    Returns repos sorted by stars. No API key needed for public repos.

    Args:
        query: Search query (e.g. "LLM agent framework", "language:python RAG")
        limit: Number of results (default 5)
    """
    import json
    from agent_eyes.fetchers.github import search_github as _search_gh

    results = await _search_gh(query, limit=limit)
    return json.dumps(results, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import sys

    transport = "stdio"
    if "--transport" in sys.argv:
        idx = sys.argv.index("--transport")
        if idx + 1 < len(sys.argv):
            transport = sys.argv[idx + 1]

    mcp.run(transport=transport)
