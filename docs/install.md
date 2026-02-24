# Agent Eyes — Installation Guide

## For Humans

Copy this to your AI Agent:

```
Install Agent Eyes: https://raw.githubusercontent.com/Panniantong/agent-eyes/main/docs/install.md
```

---

## For AI Agents

Install Agent Eyes and set it up for the user. Minimize friction — ask as few questions as possible.

### Step 1: Install and check

```bash
pip install git+https://github.com/Panniantong/agent-eyes.git || pip3 install git+https://github.com/Panniantong/agent-eyes.git
agent-eyes install --env=auto
```

That's it. This installs the package, auto-detects the environment, and shows what's working.

### Step 2: Tell user what's ready + offer ONE upgrade

Tell the user what already works, then offer the single highest-value upgrade:

> "✅ Agent Eyes installed! Here's what I can already do:
> - Read web pages, GitHub repos, RSS feeds, YouTube transcripts
> - Read individual tweets
>
> **Want me to unlock search too?** One free API key lets me search the entire web, Reddit, and Twitter for you.
> Just go to https://exa.ai → sign up (free, 1000 searches/month) → send me the API key.
>
> Or say 'skip' and I'm ready to use as-is."

If the user provides a key:
```bash
agent-eyes configure exa-key THE_KEY
```

If the user says skip, move to Step 4.

### Step 3: Offer additional channels

After Exa is configured (or skipped), briefly mention what else is available:

> "I can also unlock these with cookies from your browser (2 min each):
> 🐦 **Twitter** deep search — timelines, threads, advanced search
> 📕 **XiaoHongShu** — read notes and comments
>
> Want any of these? Or say 'done' and we're good to go."

Only proceed with channels the user explicitly asks for.

#### How to get cookies (for any platform)

When the user wants to set up a cookie-based channel, give them the SIMPLEST method:

**Method 1 — Browser extension (easiest):**
> "Install the 'Cookie-Editor' extension for Chrome/Firefox (free). Open [the site], click the extension icon, click 'Export' → 'Header String'. Paste it to me."

**Method 2 — Manual (if they don't want to install an extension):**
> "Open [the site] in Chrome. Press F12. Click 'Application' tab at the top. Click 'Cookies' on the left. Find and copy the values I need."

#### Twitter setup
Cookie-Editor export, or manually copy **auth_token** and **ct0** from x.com cookies.
```bash
agent-eyes configure twitter-cookies AUTH_TOKEN CT0
```

#### XiaoHongShu setup
Cookie-Editor export the full cookie string from xiaohongshu.com.
```bash
agent-eyes configure xhs-cookie COOKIE_STRING
```

#### YouTube (only mention if user has age-restricted video needs)
No cookies needed for public videos. For age-restricted/member content:
```bash
agent-eyes configure youtube-cookies chrome
```
(yt-dlp reads cookies directly from the browser — just tell it which browser)

#### Bilibili
- Local computer: already works
- Server: needs proxy (see below)

#### Reddit full reader + Bilibili on server
Only offer this if `agent-eyes install` detected server environment:
> "Reddit and Bilibili block server IPs. Reddit search already works (via Exa), but for reading full posts you'd need a $1/month proxy from https://webshare.io. Want to set that up?"

```bash
agent-eyes configure proxy http://user:pass@ip:port
```

### Step 4: Done

```bash
agent-eyes doctor
```

Summarize naturally:
> "✅ Ready! Here's everything I can do: [list channels]. Try asking me to search or read something!"

**Remember**: the user can always come back and say "set up Twitter" or "add a proxy" later. You just run the corresponding `agent-eyes configure` command.

---

## Quick Reference

| Command | What it does |
|---------|-------------|
| `agent-eyes doctor` | Show all channels and status |
| `agent-eyes configure exa-key KEY` | Unlock search (web + Reddit + Twitter) |
| `agent-eyes configure twitter-cookies TOKEN CT0` | Unlock Twitter deep search |
| `agent-eyes configure xhs-cookie COOKIE` | Unlock XiaoHongShu |
| `agent-eyes configure youtube-cookies BROWSER` | Unlock age-restricted YouTube |
| `agent-eyes configure proxy URL` | Unlock Reddit reader + Bilibili (server) |
| `agent-eyes read URL` | Read any URL |
| `agent-eyes search "query"` | Search the web |
