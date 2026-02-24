# 👁️ Agent Eyes

**Give your AI Agent eyes to see the entire internet.**

Agent Eyes is an open-source Agent capability aggregator. It combines the best free tools into one install, so any AI Agent can search and read the entire internet.

> Not a framework. Not a library. Just glue — beautifully simple glue that gives your Agent superpowers.

---

## Install (One Line)

**Copy this to your AI Agent** (Claude Code, OpenClaw, Cursor, ChatGPT, etc.):

```
Install and configure Agent Eyes by following the instructions here:
https://raw.githubusercontent.com/Panniantong/agent-eyes/main/docs/install.md
```

Your Agent reads the guide, installs everything, and configures itself. You just watch.

**Or install manually:**

```bash
pip install https://github.com/Panniantong/agent-eyes/archive/main.zip
agent-eyes doctor    # See what's available
agent-eyes setup     # Unlock more (optional)
```

# Read any URL (works immediately, no config needed)
agent-eyes read "https://github.com/openai/gpt-4"
agent-eyes read "https://www.bilibili.com/video/BV1xx411c7mD"

# Search GitHub (works immediately, no config needed)
agent-eyes search-github "LLM framework"

# Unlock search (one free API key)
agent-eyes setup
agent-eyes search "AI agent infrastructure 2025"
agent-eyes search-reddit "best self-hosted LLM" --sub LocalLLaMA
agent-eyes search-twitter "OpenClaw agent"
```

---

## Platform Support

### ✅ Zero Config (works out of the box)

| Platform | Read | Search | Notes |
|----------|:----:|:------:|-------|
| Web Pages | ✅ | — | Any URL via Jina Reader |
| GitHub | ✅ | ✅ | Repos, issues, PRs, code |
| Bilibili | ✅ | — | Videos with subtitles |
| YouTube | ✅ | — | Videos with subtitles (needs yt-dlp) |
| RSS | ✅ | — | Any RSS/Atom feed |
| Single Tweet | ✅ | — | Via Jina Reader |

### 🔑 One Free API Key (30 seconds to set up)

| Platform | Read | Search | Notes |
|----------|:----:|:------:|-------|
| Web (semantic) | — | ✅ | Exa API (1000 free/month) |
| Reddit | — | ✅ | Via Exa (site:reddit.com) |
| Twitter/X | — | ✅ | Via Exa (site:x.com) |

### ⚙️ Optional Setup

| Platform | Read | Search | What's Needed |
|----------|:----:|:------:|---------------|
| Reddit (full) | ✅ | — | ISP proxy (~$3-10/mo) |
| Twitter (advanced) | ✅ | ✅ | birdx + browser cookies (free) |
| WeChat Articles | ✅ | — | Playwright (free, auto-installed) |
| XiaoHongShu | ✅ | — | Playwright + one-time login (free) |
| Video Transcription | ✅ | — | Groq API key (free) |

---

## Three Ways to Use

### 1. Command Line (CLI)

```bash
agent-eyes read <url>                    # Read any URL
agent-eyes search "query"                # Search the web
agent-eyes search-reddit "query"         # Search Reddit
agent-eyes search-github "query"         # Search GitHub
agent-eyes search-twitter "query"        # Search Twitter
agent-eyes setup                         # Interactive setup wizard
agent-eyes doctor                        # Check platform status
```

### 2. MCP Server (for Claude Code, Cursor, etc.)

```bash
pip install agent-eyes[mcp]
python -m agent_eyes.integrations.mcp_server
```

Exposes 8 tools: `read_url`, `read_batch`, `detect_platform`, `search`, `search_reddit`, `search_github`, `search_twitter`, `get_status`

Add to your MCP config:

```json
{
  "mcpServers": {
    "agent-eyes": {
      "command": "python",
      "args": ["-m", "agent_eyes.integrations.mcp_server"]
    }
  }
}
```

### 3. Python Library

```python
from agent_eyes import AgentEyes
import asyncio

eyes = AgentEyes()

# Read
result = asyncio.run(eyes.read("https://github.com/openai/gpt-4"))
print(result["title"])
print(result["content"])

# Search
results = asyncio.run(eyes.search("AI agent framework"))
for r in results:
    print(f"{r['title']} — {r['url']}")

# Search Reddit
results = asyncio.run(eyes.search_reddit("best LLM", subreddit="LocalLLaMA"))

# Health check
print(eyes.doctor_report())
```

---

## Configuration

### Interactive Setup

```bash
agent-eyes setup
```

Walks you through configuring each platform step by step. Only asks for what you want to set up.

### Agent-Readable Guides

Each platform has a detailed setup guide in `agent_eyes/guides/`. These are designed for AI Agents to read and follow — the Agent handles the technical steps, and only asks the user for things that require human action (logging in, copying API keys, buying proxies).

| Guide | What It Configures |
|-------|-------------------|
| `setup-exa.md` | Exa search API key (free) |
| `setup-reddit.md` | Reddit ISP proxy |
| `setup-twitter.md` | Twitter birdx cookies |
| `setup-xiaohongshu.md` | XiaoHongShu login |
| `setup-wechat.md` | WeChat Playwright |
| `setup-groq.md` | Groq Whisper API key (free) |

### Manual Config

Config file: `~/.agent-eyes/config.yaml`

```yaml
exa_api_key: "exa-..."
github_token: "ghp_..."
reddit_proxy: "http://user:pass@ip:port"
groq_api_key: "gsk_..."
```

Environment variables also work (uppercase): `EXA_API_KEY`, `GITHUB_TOKEN`, etc.

---

## Health Check

```bash
$ agent-eyes doctor

👁️  Agent Eyes Status
========================================

✅ Ready (no setup needed):
  ✅ Web Pages
  ✅ GitHub
  ✅ Bilibili
  ✅ RSS
  ✅ Tweet (single)
  ✅ GitHub Search

🔍 Search (need free Exa API key):
  ⬜ Web Search
  ⬜ Reddit Search
  ⬜ Twitter Search

🔧 Optional (advanced setup):
  ⬜ Twitter Advanced — Install birdx for timeline/deep search
  ⬜ Reddit Reader — Need proxy for full post reading
  ⬜ WeChat — pip install agent-eyes[browser]
  ⬜ XiaoHongShu — pip install agent-eyes[browser]

Status: 7/13 platforms active
Run `agent-eyes setup` to unlock more!
```

---

## Architecture

Agent Eyes is pure glue. Every channel is a thin wrapper (~50 lines) around an external tool. **Swap any backend by changing one file.**

```
┌─────────────────────────────────────────┐
│           Agent Eyes (pure glue)         │
│                                          │
│  ┌─────────────────────────────────────┐│
│  │  Pluggable Channels                 ││
│  │                                     ││
│  │  web.py      → Jina Reader API      ││
│  │  github.py   → GitHub API           ││
│  │  twitter.py  → birdx + Jina         ││
│  │  youtube.py  → yt-dlp               ││
│  │  reddit.py   → Reddit JSON API      ││
│  │  bilibili.py → Bilibili API         ││
│  │  rss.py      → feedparser           ││
│  │  exa.py      → Exa Search API       ││
│  │                                     ││
│  │  ↑ Swap any backend, nothing else   ││
│  │    changes. Just edit one file.     ││
│  └─────────────────────────────────────┘│
│  ┌──────────┐ ┌──────────────────────┐  │
│  │ Config   │ │ Integrations         │  │
│  │ Doctor   │ │ CLI · MCP · Skill    │  │
│  │ Guides   │ │ Python API           │  │
│  └──────────┘ └──────────────────────┘  │
└─────────────────────────────────────────┘
```

**Design principle**: Agent Eyes doesn't reinvent wheels. It aggregates the best free tools and makes them accessible to any AI Agent with one install.

---

## Credits

Agent Eyes stands on the shoulders of these amazing open-source projects:

- **[Jina Reader](https://r.jina.ai)** — web page reading
- **[birdx](https://github.com/runesleo/birdx)** by [@runes_leo](https://x.com/runes_leo) — Twitter access
- **[Exa](https://exa.ai)** — semantic search
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** — YouTube transcripts
- **[feedparser](https://github.com/kurtmckee/feedparser)** — RSS/Atom feeds

## License

MIT
