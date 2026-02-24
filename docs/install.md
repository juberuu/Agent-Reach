# Agent Eyes — Installation Guide

## For Humans

Copy this to your AI Agent:

```
帮我安装 Agent Eyes：https://raw.githubusercontent.com/Panniantong/agent-eyes/main/docs/install.md
```

---

## For AI Agents

### Step 1: Install

```bash
pip install https://github.com/Panniantong/agent-eyes/archive/main.zip || pip3 install https://github.com/Panniantong/agent-eyes/archive/main.zip
agent-eyes install --env=auto
```

This single command does everything automatically:
- Detects local computer vs server
- Auto-imports browser cookies on local (Twitter, XiaoHongShu, Bilibili)
- Auto-detects Exa API key if already in environment
- Tests all channels
- Shows what's working and what needs setup

**Read the output carefully.** It tells you exactly what happened and what's next.

### Step 2: Only if needed — configure what's missing

Based on the install output, you may need to configure one or two things.
Only ask the user for items the install output says are missing.

**If search is not configured:**
> "Want to unlock web search? Go to https://exa.ai → sign up (free) → send me the API key."

```bash
agent-eyes configure exa-key THE_KEY
```

**If cookies were not auto-imported (server users):**
> "To unlock Twitter and XiaoHongShu, install the Cookie-Editor Chrome extension, go to the site, click Export → Header String, and paste it to me."
> Extension: https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm

```bash
agent-eyes configure twitter-cookies "PASTED_STRING"
agent-eyes configure xhs-cookie "PASTED_STRING"
```

**If on server and wants Reddit/Bilibili full access:**
> "Reddit and Bilibili block server IPs. Get a proxy at https://webshare.io ($1/month) and send me the address."

```bash
agent-eyes configure proxy http://user:pass@ip:port
```

### Step 3: Verify

```bash
agent-eyes doctor
```

Report what's active. Users can configure more anytime by asking.

---

## Quick Reference

| Command | What it does |
|---------|-------------|
| `agent-eyes install --env=auto` | Full auto-setup |
| `agent-eyes doctor` | Show status |
| `agent-eyes configure exa-key KEY` | Unlock search |
| `agent-eyes configure twitter-cookies "..."` | Unlock Twitter |
| `agent-eyes configure xhs-cookie "..."` | Unlock XiaoHongShu |
| `agent-eyes configure proxy URL` | Unlock Reddit + Bilibili (server) |
| `agent-eyes read URL` | Read any URL |
| `agent-eyes search "query"` | Search the web |
