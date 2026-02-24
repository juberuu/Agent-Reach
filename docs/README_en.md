# 👁️ Agent Eyes

**Give your AI Agent eyes to see the entire internet.**

Your AI Agent is smart but blind. It can't browse Reddit, search Twitter, or read Bilibili videos. Agent Eyes fixes this — once installed, your Agent can search and read content across 10+ platforms.

> Install once. Superpowers unlocked. Most features work with zero config, zero cost.

[中文文档](../README.md)

---

## Get Started in 30 Seconds

Copy this to your AI Agent (Claude Code, OpenClaw, Cursor, etc.):

```
Install Agent Eyes: https://raw.githubusercontent.com/Panniantong/agent-eyes/main/docs/install.md
```

Your Agent handles everything. You answer 1-2 questions at most.

<details>
<summary>Manual install</summary>

```bash
pip install https://github.com/Panniantong/agent-eyes/archive/main.zip
agent-eyes install --env=auto
agent-eyes doctor
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
agent-eyes read "https://github.com/openai/gpt-4"
agent-eyes search-github "LLM framework"
```

---

## One Key Unlocks Search

Sign up at [Exa](https://exa.ai) (free, 1000 searches/month). One key unlocks **web + Reddit + Twitter search**:

```bash
agent-eyes configure exa-key YOUR_KEY
agent-eyes search "best open source LLM 2025"
agent-eyes search-reddit "self-hosted LLM" --sub LocalLLaMA
agent-eyes search-twitter "AI agent"
```

---

## Unlock More

### 🍪 Cookie-based (free, 2 minutes)

```bash
# Local: auto-import all cookies
agent-eyes configure --from-browser chrome

# Server: use Cookie-Editor extension, export Header String
agent-eyes configure twitter-cookies "cookie_string"
agent-eyes configure xhs-cookie "cookie_string"
```

Unlocks: Twitter deep search, XiaoHongShu notes

### 🌐 Proxy ($1/month, servers only)

Reddit and Bilibili block server IPs. Local computers are fine.

```bash
agent-eyes configure proxy http://user:pass@ip:port
```

Recommend [Webshare](https://webshare.io). One proxy covers both Reddit and Bilibili.

---

## Three Ways to Use

**CLI** · **Python API** · **MCP Server**

```bash
agent-eyes read "URL"
agent-eyes search "query"
agent-eyes doctor
```

```python
from agent_eyes import AgentEyes
eyes = AgentEyes()
result = asyncio.run(eyes.read("https://example.com"))
```

```json
{"mcpServers": {"agent-eyes": {"command": "python", "args": ["-m", "agent_eyes.integrations.mcp_server"]}}}
```

---

## Why Agent Eyes?

Not a framework. Not an SDK. Just glue — beautifully simple glue.

- Aggregates the best free tools: Jina Reader, birdx, yt-dlp, Exa, feedparser
- Each channel is ~50 lines. Swap any backend by editing one file.
- CLI, MCP Server, Python API
- 99% free. The remaining 1% costs $1/month.

## Credits

[Jina Reader](https://r.jina.ai) · [birdx](https://github.com/runesleo/birdx) · [Exa](https://exa.ai) · [yt-dlp](https://github.com/yt-dlp/yt-dlp) · [feedparser](https://github.com/kurtmckee/feedparser)

## License

MIT
