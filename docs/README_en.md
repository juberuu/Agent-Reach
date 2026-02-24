# 👁️ Agent Reach

**Give your AI Agent eyes to see the entire internet.**

Your AI Agent is smart but blind. It can't browse Reddit, search Twitter, or read Bilibili videos. Agent Reach fixes this — once installed, your Agent can search and read content across 10+ platforms.

> Install once. Superpowers unlocked. Most features work with zero config, zero cost.

[中文文档](../README.md)

---

## Get Started in 30 Seconds

Copy this to your AI Agent (Claude Code, OpenClaw, Cursor, etc.):

```
Install Agent Reach: https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md
```

Your Agent handles everything. You answer 1-2 questions at most.

<details>
<summary>Manual install</summary>

```bash
pip install https://github.com/Panniantong/agent-reach/archive/main.zip
agent-reach install --env=auto
agent-reach doctor
```
</details>

---

## Works Out of the Box

No configuration needed:

- 🌐 **Web pages** — read any URL
- 📦 **GitHub** — repos, issues, PRs, code search
- 📺 **YouTube** — video transcripts
- 📺 **Bilibili** — video info + subtitles
- 📡 **RSS** — any feed
- 🐦 **Twitter** — read individual tweets

```bash
agent-reach read "https://github.com/openai/gpt-4"
agent-reach search-github "LLM framework"
```

---

## One Key Unlocks Search

Sign up at [Exa](https://exa.ai) (free, 1000 searches/month). One key unlocks **web + Reddit + Twitter search**:

```bash
agent-reach configure exa-key YOUR_KEY
agent-reach search "best open source LLM 2025"
agent-reach search-reddit "self-hosted LLM" --sub LocalLLaMA
agent-reach search-twitter "AI agent"
```

---

## Unlock More

### 🍪 Cookie-based (free, 2 minutes)

```bash
# Local: auto-import all cookies
agent-reach configure --from-browser chrome

# Server: use Cookie-Editor extension, export Header String
agent-reach configure twitter-cookies "cookie_string"
agent-reach configure xhs-cookie "cookie_string"
```

Unlocks: Twitter deep search, XiaoHongShu notes

### 🌐 Proxy ($1/month, servers only)

Reddit and Bilibili block server IPs. Local computers are fine.

```bash
agent-reach configure proxy http://user:pass@ip:port
```

Recommend [Webshare](https://webshare.io). One proxy covers both Reddit and Bilibili.

---

## Three Ways to Use

**CLI** · **Python API** · **MCP Server**

```bash
agent-reach read "URL"
agent-reach search "query"
agent-reach doctor
```

```python
from agent_reach import AgentReach
eyes = AgentReach()
result = asyncio.run(eyes.read("https://example.com"))
```

```json
{"mcpServers": {"agent-reach": {"command": "python", "args": ["-m", "agent_reach.integrations.mcp_server"]}}}
```

---

## Why Agent Reach?

Not a framework. Not an SDK. Just glue — beautifully simple glue.

- Aggregates the best free tools: Jina Reader, birdx, yt-dlp, Exa, feedparser
- Each channel is ~50 lines. Swap any backend by editing one file.
- CLI, MCP Server, Python API
- 99% free. The remaining 1% costs $1/month.

## Credits

[Jina Reader](https://r.jina.ai) · [birdx](https://github.com/runesleo/birdx) · [Exa](https://exa.ai) · [yt-dlp](https://github.com/yt-dlp/yt-dlp) · [feedparser](https://github.com/kurtmckee/feedparser)

## License

MIT
