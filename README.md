# 👁️ Agent Eyes

**Give your AI Agent eyes to see the entire internet.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Agent Eyes is an open-source infrastructure tool that gives any AI Agent the ability to **search** and **read** the entire internet. One install, 10+ platforms, unified output.

> 🙏 Built on the shoulders of [x-reader](https://github.com/runesleo/x-reader) by [@runes_leo](https://x.com/runes_leo). Thank you for the foundation!

## Why Agent Eyes?

Your AI Agent is blind. It can only see what you manually feed it.

Agent Eyes gives it **eyes** — the ability to:
- **Search** the web, Reddit, GitHub with a single command
- **Read** any URL from 10+ platforms (articles, videos, tweets, posts)
- **Transcribe** videos and podcasts to text

Without this, your Agent is a chatbot waiting for instructions.  
With this, it can autonomously find and consume information — just like you do.

## Quick Start

```bash
# Install
pip install git+https://github.com/Panniantong/agent-eyes.git

# Search the web
agent-eyes search "AI agent framework 2026"

# Read any URL
agent-eyes read https://reddit.com/r/LocalLLaMA/comments/xxx
agent-eyes read https://github.com/openai/codex
agent-eyes read https://mp.weixin.qq.com/s/xxx
agent-eyes read https://x.com/elonmusk/status/xxx

# Your Agent now has eyes 👁️
```

## Supported Platforms

| Platform | Read URL | Search | Notes |
|----------|:--------:|:------:|-------|
| 🔍 Web (any) | ✅ | ✅ Exa | Semantic search across the entire web |
| 🟠 Reddit | ✅ | ✅ | Posts + comments. Proxy support via `REDDIT_PROXY` |
| 🐙 GitHub | ✅ | ✅ | Repos (README), Issues, PRs |
| 🐦 X / Twitter | ✅ | — | Tweets and threads |
| 💬 WeChat (微信公众号) | ✅ | — | Anti-scraping bypass via Playwright |
| 📕 Xiaohongshu (小红书) | ✅ | — | Session persistence for login-gated content |
| ▶️ YouTube | ✅ | — | Subtitles + Whisper transcription |
| 📺 Bilibili (B站) | ✅ | — | Official API |
| ✈️ Telegram | ✅ | — | Channel message sync |
| 📡 RSS | ✅ | — | Any RSS/Atom feed |
| 🎙️ Podcasts | ✅ | — | 小宇宙, Apple Podcasts (via Whisper) |

## Three Layers

Use the layers you need:

| Layer | What | For |
|-------|------|-----|
| **CLI** | `agent-eyes read/search` | Quick command-line use |
| **MCP Server** | 7 tools for any AI Agent | OpenClaw, Claude Code, etc. |
| **Python Library** | `from agent_eyes import UniversalReader` | Custom integrations |

### As MCP Server (recommended for Agents)

```bash
# Start the server
python mcp_server.py

# Or with SSE transport
python mcp_server.py --transport sse
```

MCP Tools exposed:

| Tool | Description |
|------|-------------|
| `read_url(url)` | Read any URL → structured content |
| `read_batch(urls)` | Read multiple URLs concurrently |
| `search(query)` | Semantic web search (Exa) |
| `search_reddit(query, subreddit?)` | Search Reddit |
| `search_github(query)` | Search GitHub repos |
| `list_inbox()` | View previously fetched content |
| `detect_platform(url)` | Identify platform from URL |

### As Python Library

```python
import asyncio
from agent_eyes.reader import UniversalReader

async def main():
    reader = UniversalReader()
    
    # Read any URL
    content = await reader.read("https://github.com/openai/codex")
    print(content.title)
    print(content.content[:500])

asyncio.run(main())
```

## Install

```bash
# Basic install
pip install git+https://github.com/Panniantong/agent-eyes.git

# With browser fallback (for WeChat/XHS anti-scraping)
pip install "agent-eyes[browser] @ git+https://github.com/Panniantong/agent-eyes.git"
playwright install chromium

# With Telegram support
pip install "agent-eyes[telegram] @ git+https://github.com/Panniantong/agent-eyes.git"

# Everything
pip install "agent-eyes[all] @ git+https://github.com/Panniantong/agent-eyes.git"
playwright install chromium
```

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `EXA_API_KEY` | For search | Free key from [exa.ai](https://exa.ai) |
| `REDDIT_PROXY` | For Reddit (if IP blocked) | `http://user:pass@host:port` |
| `GITHUB_TOKEN` | No (higher rate limits) | GitHub personal access token |
| `GROQ_API_KEY` | For Whisper | Free key from [groq.com](https://console.groq.com/keys) |
| `TG_API_ID` | Telegram only | From https://my.telegram.org |
| `TG_API_HASH` | Telegram only | From https://my.telegram.org |

## What's New (vs x-reader)

Agent Eyes extends x-reader with:

- 🟠 **Reddit support** — Read posts + comments, search subreddits. Proxy support for blocked IPs.
- 🐙 **GitHub support** — Read repos (README), issues, PRs. Search repositories.
- 🔍 **Web search** — Semantic search across the entire web via Exa.
- 🎯 **Agent-first design** — MCP Server with 7 tools, ready to plug into any AI Agent.

## Philosophy

This is **Agent infrastructure**. In the Web 4.0 era where AI Agents act on behalf of humans, the first capability they need is the ability to **see the world**.

Agent Eyes is the sensory layer — the eyes — that every Agent needs.

## Credits

- [x-reader](https://github.com/runesleo/x-reader) by [@runes_leo](https://x.com/runes_leo) — the original universal content reader that inspired and powers the core of Agent Eyes
- [Jina Reader](https://jina.ai/reader/) — universal web content extraction
- [Exa](https://exa.ai) — semantic web search API
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — video/audio extraction

## License

MIT — use it, fork it, build on it.
