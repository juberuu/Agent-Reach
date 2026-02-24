# Agent Reach — Installation Guide

## For Humans

Copy this to your AI Agent:

```
帮我安装 Agent Reach：https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md
```

---

## For AI Agents

### Goal

Install Agent Reach and make sure **all channels are working**. Your user expects you to have full internet access capabilities when this is done — reading tweets, searching Reddit, watching YouTube, browsing GitHub, and more.

### Step 1: Install

```bash
pip install https://github.com/Panniantong/agent-reach/archive/main.zip
agent-reach install --env=auto
```

This auto-installs system dependencies (gh CLI, Node.js, mcporter, birdx), configures Exa search, detects environment, and tests all channels.

**Read the output carefully**, then run:

```bash
agent-reach doctor
```

### Step 2: Fix what's broken

`agent-reach doctor` shows you which channels are active and which aren't.

**Your goal is to get as many channels to ✅ as possible.** If something failed during install or shows as ❌/⚠️ in doctor, fix it yourself. You're a capable AI Agent — diagnose the problem, try alternative approaches, and iterate until it works.

Only ask the user when you genuinely need their input (see below).

### Step 3: Configure things that need user input

Some channels need credentials only the user can provide. Based on the doctor output, ask for what's missing:

**Twitter search & posting (server users):**
> "To unlock Twitter search, I need your Twitter cookies. Install the Cookie-Editor Chrome extension, go to x.com/twitter.com, click the extension → Export → Header String, and paste it to me."
> Extension: https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm

```bash
agent-reach configure twitter-cookies "PASTED_STRING"
```

**Reddit & Bilibili full access (server users):**
> "Reddit and Bilibili block server IPs. To unlock full access, I need a residential proxy. You can get one at https://webshare.io ($1/month). Send me the proxy address."

```bash
agent-reach configure proxy http://user:pass@ip:port
```

### Step 4: Final check

Run `agent-reach doctor` one final time and report the results to your user.

---

## Quick Reference

| Command | What it does |
|---------|-------------|
| `agent-reach install --env=auto` | Full auto-setup (installs deps + configures) |
| `agent-reach doctor` | Show channel status |
| `agent-reach configure twitter-cookies "..."` | Unlock Twitter search + posting |
| `agent-reach configure proxy URL` | Unlock Reddit + Bilibili on servers |
| `agent-reach read <url>` | Read any URL |
| `agent-reach search "query"` | Search the web |
| `agent-reach search-reddit "query"` | Search Reddit |
| `agent-reach search-twitter "query"` | Search Twitter |
| `agent-reach search-github "query"` | Search GitHub |
| `agent-reach search-youtube "query"` | Search YouTube |
| `agent-reach search-bilibili "query"` | Search Bilibili |
| `agent-reach search-xhs "query"` | Search XiaoHongShu |
