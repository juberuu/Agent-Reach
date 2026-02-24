# Agent Eyes — Installation Guide

## For Humans

Copy this to your AI Agent:

```
Install and configure Agent Eyes: https://raw.githubusercontent.com/Panniantong/agent-eyes/main/docs/install.md
```

---

## For AI Agents

Follow these steps exactly. Minimize questions to the user.

### Step 1: Install + auto-detect

```bash
pip install git+https://github.com/Panniantong/agent-eyes.git || pip3 install git+https://github.com/Panniantong/agent-eyes.git
agent-eyes doctor
```

Read the doctor output. It tells you:
- What's already working (zero-config channels)
- What needs a key/cookie/proxy

Also auto-detect the environment:
```bash
agent-eyes install --env=auto
```
This command auto-detects local vs server (checks if running in SSH, Docker, or cloud VM).

### Step 2: Show ONE simple summary to user

Based on doctor output, tell the user what's already working and what ONE thing you recommend:

> "✅ Agent Eyes installed! You already have: web pages, GitHub, RSS, YouTube.
>
> **One recommendation**: get a free Exa API key to unlock web search + Reddit search + Twitter search.
> → Go to https://exa.ai, sign up (free), and send me the API key.
>
> (I can also set up Twitter, Bilibili, XiaoHongShu, and Reddit later — just ask anytime.)"

**Key principle**: only ask for ONE thing now. Don't overwhelm with choices.

### Step 3: Configure Exa (if user provides key)

```bash
agent-eyes configure exa-key THE_KEY
```

After success, tell user:

> "✅ Done! I can now search the web, Reddit, and Twitter for you.
>
> Want me to set up any of these too? (just say which ones)
> - 🐦 Twitter deep search (need browser cookies, 2 min)
> - 📕 XiaoHongShu (need browser cookies, 2 min)
> - 📺 Bilibili (need browser cookies, 2 min)
> - 📖 Reddit full reader (need $1/month proxy — search already works via Exa!)
>
> Or just say 'all' and I'll walk you through each one."

### Step 4: Configure additional channels (only if user asks)

For each channel the user asks for, use the appropriate command:

**Twitter:**
Ask: "Open x.com in Chrome → F12 → Application → Cookies → copy **auth_token** and **ct0**"
```bash
agent-eyes configure twitter-cookies AUTH_TOKEN CT0
```

**XiaoHongShu:**
Ask: "Open xiaohongshu.com in Chrome → F12 → Network → click any request → copy the Cookie header value"
```bash
agent-eyes configure xhs-cookie COOKIE_STRING
```

**YouTube (age-restricted only):**
Ask: "Which browser do you use?"
```bash
agent-eyes configure youtube-cookies chrome
```

**Bilibili:**
- Auto-detected as local → already works, nothing needed
- Auto-detected as server → needs proxy (same as Reddit, see below)

**Reddit full reader + Bilibili (server only):**
Ask: "Reddit/Bilibili block server IPs. Get a $1/month residential proxy at webshare.io, then send me the proxy address."
```bash
agent-eyes configure proxy http://user:pass@ip:port
```

### Step 5: Final status

```bash
agent-eyes doctor
```

> "✅ All set! Here's what I can do:
> [list active channels]
>
> Try: 'search Reddit for ...' or 'read this URL: ...'"

---

## Configure anything later

Users can ask their Agent to configure new channels anytime:
- "Help me set up Twitter for Agent Eyes"
- "I got a proxy, configure it for Agent Eyes"
- "Add my XiaoHongShu cookies"

The Agent runs `agent-eyes configure <channel> <value>` — each command auto-tests.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `agent-eyes doctor` | Show what's working |
| `agent-eyes configure exa-key KEY` | Unlock web/Reddit/Twitter search |
| `agent-eyes configure twitter-cookies TOKEN CT0` | Unlock Twitter deep search |
| `agent-eyes configure xhs-cookie COOKIE` | Unlock XiaoHongShu |
| `agent-eyes configure youtube-cookies chrome` | Unlock age-restricted YouTube |
| `agent-eyes configure proxy URL` | Unlock Reddit + Bilibili (server) |
| `agent-eyes read <url>` | Read any URL |
| `agent-eyes search "query"` | Search the web |
