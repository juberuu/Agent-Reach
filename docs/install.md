# Agent Eyes — Installation Guide

## For Humans

Copy and paste this to your AI Agent (Claude Code, OpenClaw, Cursor, etc.):

```
Install and configure Agent Eyes by following the instructions here:
https://raw.githubusercontent.com/Panniantong/agent-eyes/main/docs/install.md
```

Your Agent will handle everything. You just answer a few questions.

---

## For AI Agents

You are installing Agent Eyes — giving yourself eyes to see the entire internet.
Follow this guide step by step. Do not skip steps.

### Step 1: Install

```bash
pip install git+https://github.com/Panniantong/agent-eyes.git
```

If fails: try `pip3`, or add `--user`, or `--break-system-packages`.

Verify:
```bash
agent-eyes version
```

### Step 2: Ask environment

Ask the user:

> "You're installing Agent Eyes! First question: are you running on a **local computer** or a **server/VPS**?"

Remember their answer — it affects which channels need extra setup.

### Step 3: Show channel menu

Show the user this menu. Explain each option clearly.

**Present it like this** (adjust the Bilibili line based on Step 2 answer):

---

> Here are all the channels Agent Eyes supports. I'll help you set up whichever ones you want.
>
> **Already active — no setup needed ✅**
> These work right now, nothing to configure:
> - ✅ **Web pages** — read any URL
> - ✅ **GitHub** — read repos, issues, PRs + search repos
> - ✅ **RSS** — read any RSS/Atom feed
> - ✅ **YouTube** — video transcripts via yt-dlp
> - ✅ **Twitter basic** — read individual tweets
>
> **Recommended — free, takes 30 seconds each 🔍**
> - 🔍 **Exa Search** (STRONGLY RECOMMENDED)
>   - What it unlocks: **full web search + Reddit search + Twitter search**
>   - What you need: one free API key from https://exa.ai (1000 searches/month free)
>   - Without it: I can read URLs you give me, but can't search the internet for you
>
> **Optional — easy setup 🔧**
> - 🐦 **Twitter Advanced** — search timelines, read threads, deep search
>   - What you need: export cookies from your browser (free, 2 minutes)
>   - Without it: I can still search Twitter via Exa and read individual tweets
>
> - 📺 **Bilibili** [IF LOCAL: "already works ✅"] [IF SERVER: "⚠️ needs proxy — Bilibili blocks server IPs. Proxy costs ~$1/month at webshare.io. Without it, Bilibili won't work from your server."]
>
> **Optional — more setup 🔨**
> - 📖 **Reddit Full Reader** — read complete posts + all comments
>   - What you need: residential proxy (~$1/month at https://webshare.io)
>   - Without it: I can still **search** Reddit content via Exa (free!), just can't read full posts with all comments
>   - [IF SERVER: "Same proxy works for both Reddit and Bilibili"]
>
> - 💬 **WeChat** — read WeChat public articles
>   - What you need: install browser component (~150MB download)
>
> - 📕 **XiaoHongShu** — read XHS notes
>   - What you need: browser component + scan QR code once to login
>
> **Which ones would you like me to set up?** (I recommend at least Exa Search)

---

Wait for user to choose. Then proceed to Step 4.

### Step 4: Run installer

```bash
agent-eyes install --env=<local|server>
```

### Step 5: Configure selected channels

For each channel the user selected, run the corresponding configure command.
Each command auto-tests after configuring.

#### If user selected: Exa Search

Tell the user:
> "Go to https://exa.ai, sign up (free), and send me your API Key."

When they provide it:
```bash
agent-eyes configure exa-key THE_KEY
```
Expected: `✅ exa-key configured! Testing search... ✅ Search works!`

#### If user selected: Reddit Full Reader and/or Bilibili (on server)

Tell the user:
> "Reddit and Bilibili need a residential proxy. Steps:
> 1. Go to https://www.webshare.io
> 2. Sign up and get a proxy ($1/month plan is enough)
> 3. Copy your proxy address (format: http://username:password@ip:port)
> 4. Send it to me"

When they provide it:
```bash
agent-eyes configure proxy THE_PROXY_URL
```
Expected: `✅ proxy configured! Testing Reddit... ✅ Reddit accessible!`

#### If user selected: Twitter Advanced

Tell the user:
> "Twitter Advanced needs cookies from your browser. Steps:
> 1. Open https://x.com in Chrome and make sure you're logged in
> 2. Press F12 → Application tab → Cookies → https://x.com
> 3. Find and copy these two values: **auth_token** and **ct0**
> 4. Send them to me"

When they provide cookies:
```bash
# birdx cookie setup (if birdx is available)
which birdx || pip install birdx
# Configure birdx with cookies (method varies by birdx version)
```

#### If user selected: WeChat

```bash
pip install agent-eyes[browser]
playwright install chromium
```
Tell user: "✅ WeChat is ready! Send me any WeChat article URL."

#### If user selected: XiaoHongShu

```bash
pip install agent-eyes[browser]
playwright install chromium
```
Tell user: "I'll need you to scan a QR code once to log in. Ready?" Then read the guide: read the file at `agent_eyes/guides/setup-xiaohongshu.md` for detailed steps.

### Step 6: Final check

```bash
agent-eyes doctor
```

Summarize results for the user naturally. Example:

> "✅ All done! Here's what I can do now:
> - 📖 Read: Web, GitHub, YouTube, RSS, Tweets, Reddit, Bilibili
> - 🔍 Search: Web, GitHub, Reddit, Twitter
>
> Try asking me things like:
> - 'Search Reddit for best self-hosted LLM'
> - 'Read this GitHub repo: [URL]'
> - 'What's trending on Twitter about AI agents?'"

---

## Quick Reference

| Action | Command |
|--------|---------|
| Install | `pip install git+https://github.com/Panniantong/agent-eyes.git` |
| Setup | `agent-eyes install --env=<local\|server>` |
| Add Exa key | `agent-eyes configure exa-key YOUR_KEY` |
| Add proxy | `agent-eyes configure proxy http://user:pass@ip:port` |
| Health check | `agent-eyes doctor` |
| Read any URL | `agent-eyes read <url>` |
| Search web | `agent-eyes search "query"` |
| Search GitHub | `agent-eyes search-github "query"` |
| Search Reddit | `agent-eyes search-reddit "query"` |
| Search Twitter | `agent-eyes search-twitter "query"` |
