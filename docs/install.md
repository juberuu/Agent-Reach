# Agent Eyes — Installation Guide

## For Humans

Copy this to your AI Agent:

```
Install Agent Eyes: https://raw.githubusercontent.com/Panniantong/agent-eyes/main/docs/install.md
```

---

## For AI Agents

Install Agent Eyes and set it up with minimal user effort.

### Step 1: Install and check

```bash
pip install git+https://github.com/Panniantong/agent-eyes.git || pip3 install git+https://github.com/Panniantong/agent-eyes.git
agent-eyes install --env=auto
```

### Step 2: One-click cookie import (LOCAL COMPUTERS ONLY)

If the environment was detected as **local**, offer to grab all cookies at once:

> "I can automatically import your cookies from Chrome to unlock Twitter, XiaoHongShu, and Bilibili — all at once, one command. Want me to do that?
> (Make sure Chrome is closed first)"

If yes:
```bash
pip install browser-cookie3
agent-eyes configure --from-browser chrome
```

This extracts cookies for ALL supported platforms in one shot. No F12, no manual copying.

If user uses a different browser:
```bash
agent-eyes configure --from-browser firefox   # or edge, brave, opera
```

If the environment is **server** or the user declines, skip to Step 3.

### Step 3: Offer search upgrade

> "Want to unlock web search? One free API key lets me search the entire web, Reddit, and Twitter.
> → Go to https://exa.ai → sign up (free) → send me the API key.
> Or say 'skip'."

If user provides key:
```bash
agent-eyes configure exa-key THE_KEY
```

### Step 4: Server-only — offer proxy

Only if auto-detected as server:

> "Reddit and Bilibili block server IPs. Reddit search still works free via Exa, but for full access you'd need a cheap proxy ($1/month).
> → Get one at https://webshare.io if interested. Or skip — search still works!"

If user provides proxy:
```bash
agent-eyes configure proxy http://user:pass@ip:port
```

### Step 5: Done

```bash
agent-eyes doctor
```

> "✅ All set! [list what's active]. Try asking me to search or read something!"

**Users can always configure more later** by saying things like "set up Twitter for Agent Eyes" or "add my XiaoHongShu cookies".

---

## Manual configure (one channel at a time)

These commands are for manual setup or adding individual channels later:

| Command | What it does |
|---------|-------------|
| `agent-eyes configure --from-browser chrome` | Import ALL cookies at once |
| `agent-eyes configure exa-key KEY` | Unlock search (web + Reddit + Twitter) |
| `agent-eyes configure twitter-cookies TOKEN CT0` | Twitter deep search (manual) |
| `agent-eyes configure xhs-cookie COOKIE` | XiaoHongShu (manual) |
| `agent-eyes configure youtube-cookies chrome` | Age-restricted YouTube |
| `agent-eyes configure proxy URL` | Reddit + Bilibili on servers |
| `agent-eyes doctor` | Show all channels and status |
| `agent-eyes read URL` | Read any URL |
| `agent-eyes search "query"` | Search the web |
