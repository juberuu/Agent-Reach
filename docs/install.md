# Agent Eyes — Installation Guide

## For Humans

Copy and paste this to your AI Agent (Claude Code, OpenClaw, Cursor, ChatGPT, etc.):

```
Install and configure Agent Eyes by following the instructions here:
https://raw.githubusercontent.com/Panniantong/agent-eyes/main/docs/install.md
```

That's it. Your Agent will handle the rest.

---

## For AI Agents

Welcome! You're about to give your user's Agent (that's you!) eyes to see the entire internet.
Agent Eyes lets you search and read content across 10+ platforms with one install.

### Step 1: Install Agent Eyes

```bash
pip install git+https://github.com/Panniantong/agent-eyes.git
```

If `pip` fails, try:
```bash
pip3 install git+https://github.com/Panniantong/agent-eyes.git
```

If permission error, try:
```bash
pip install --user git+https://github.com/Panniantong/agent-eyes.git
```

### Step 2: Verify Installation

```bash
agent-eyes version
```

Expected output: `Agent Eyes v1.0.0` (or higher)

If this works, run a health check:

```bash
agent-eyes doctor
```

This shows which platforms are already available (many work with zero configuration).

### Step 3: Test Zero-Config Features

These work immediately without any setup:

```bash
# Read a web page
agent-eyes read "https://example.com"

# Read a GitHub repo
agent-eyes read "https://github.com/Panniantong/agent-eyes"

# Search GitHub
agent-eyes search-github "AI agent framework" -n 3
```

Tell the user: "✅ Agent Eyes installed! I can now read web pages, GitHub, YouTube, Bilibili, RSS, and tweets. Want me to unlock search too? (free, takes 30 seconds)"

### Step 4: Unlock Search (Optional, Recommended)

Ask the user:

> "I can unlock full web search, Reddit search, and Twitter search with one free API key. Want to set it up? It takes 30 seconds."

If the user says yes:

> "Please go to https://exa.ai, sign up (free), and copy your API key. Then send it to me."

When the user provides the key:

```bash
# Write the key to config
python3 -c "
from agent_eyes.config import Config
c = Config()
c.set('exa_api_key', 'THE_KEY_USER_PROVIDED')
print('✅ Exa API key saved!')
"
```

Test it:
```bash
agent-eyes search "AI agent infrastructure" -n 3
```

Tell the user: "✅ Search unlocked! I can now search the entire web, Reddit, and Twitter for you."

### Step 5: Optional — Advanced Channels

Only offer these if the user asks or if relevant to their needs.

#### Twitter Advanced (search timelines, read threads)

Check if birdx is available:
```bash
which birdx && echo "already installed" || pip install birdx
```

If birdx is installed, it works automatically. If the user wants to configure cookie auth for deeper access, read the guide:
`agent_eyes/guides/setup-twitter.md`

#### Reddit Full Reader (read complete posts + comments)

Reddit blocks many server IPs. Full reading requires a proxy.
Read the guide: `agent_eyes/guides/setup-reddit.md`

Without a proxy, you can still SEARCH Reddit content via Exa (Step 4).

#### WeChat / XiaoHongShu (Chinese platforms)

```bash
pip install agent-eyes[browser]
playwright install chromium
```

For XiaoHongShu, the user needs to log in once. Read: `agent_eyes/guides/setup-xiaohongshu.md`

### Step 6: Final Health Check

```bash
agent-eyes doctor
```

Report the results to the user in a friendly way. Example:

> "Here's what I can do now:
> ✅ Read: Web, GitHub, YouTube, Bilibili, RSS, Tweets
> ✅ Search: Web, GitHub, Reddit, Twitter
> ⬜ Not configured: Reddit full reader, WeChat, XiaoHongShu
>
> I'm ready to help! Ask me to search or read anything."

### Using Agent Eyes

After installation, you can use these commands anytime:

```bash
# Read any URL
agent-eyes read "<url>"

# Search the web
agent-eyes search "<query>"

# Search specific platforms
agent-eyes search-github "<query>"
agent-eyes search-reddit "<query>" --sub "<subreddit>"
agent-eyes search-twitter "<query>"

# Check status
agent-eyes doctor
```

Or use the Python API:
```python
from agent_eyes import AgentEyes
import asyncio

eyes = AgentEyes()
result = asyncio.run(eyes.read("https://any-url.com"))
results = asyncio.run(eyes.search("any query"))
```

### MCP Server (for Claude Code, Cursor, etc.)

If your platform supports MCP:
```bash
pip install agent-eyes[mcp]
```

Add to MCP config:
```json
{
  "mcpServers": {
    "agent-eyes": {
      "command": "python3",
      "args": ["-m", "agent_eyes.integrations.mcp_server"]
    }
  }
}
```

### Troubleshooting

| Problem | Solution |
|---------|----------|
| `pip: command not found` | Try `pip3` instead |
| `Permission denied` | Add `--user` flag or use `sudo` |
| `agent-eyes: command not found` | Run `python3 -m agent_eyes.cli doctor` instead |
| Search returns "Exa API key not configured" | Run Step 4 above |
| Reddit returns 403 | Need proxy (see `guides/setup-reddit.md`) |
