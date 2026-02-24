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
Follow this guide step by step. Do not improvise.

### Step 1: Install

```bash
pip install git+https://github.com/Panniantong/agent-eyes.git
```

If fails: try `pip3`, or add `--user`, or `--break-system-packages`.

Verify:
```bash
agent-eyes version
```

### Step 2: Detect environment

Ask the user:

> "First question: are you running on a **local computer** or a **server/VPS**?"

This determines what works out of the box and what needs extra setup.

### Step 3: Show channel menu

Present this menu to the user. Adjust the details based on their environment (local vs server).

**IMPORTANT**: Make sure the user understands what each tier means and what they get/miss.

---

> **Agent Eyes supports these channels. Let me help you choose what to set up.**
>
> ---
>
> **🟢 Already active — works right now, nothing needed:**
>
> | Channel | What it does |
> |---------|-------------|
> | ✅ Web pages | Read any URL on the internet |
> | ✅ GitHub | Read repos, issues, PRs + search repositories |
> | ✅ RSS | Read any RSS/Atom feed |
>
> These 3 channels are always available. No setup needed.
>
> ---
>
> **🔵 Cookie-based — free, just need to export cookies from your browser (~2 min each):**
>
> | Channel | What it does | Without cookies |
> |---------|-------------|-----------------|
> | 🐦 Twitter/X | Read tweets, search timelines, read threads | Can still read individual tweet URLs (basic mode) |
> | 📺 YouTube | Video transcripts (public + age-restricted) | Public videos work without cookies; age-restricted/member-only videos need cookies |
> | 📺 Bilibili | Video info + subtitles | [LOCAL: works without cookies ✅] [SERVER: ⚠️ blocked — needs proxy, see below] |
> | 📕 XiaoHongShu | Read XHS notes + comments | Falls back to basic web reading (less content) |
>
> **How to export cookies**: open the site in Chrome → F12 → Application → Cookies → copy the values. I'll walk you through it for each one you choose.
>
> ---
>
> **🟡 Free API key — one key unlocks 3 search capabilities (~30 seconds):**
>
> | Channel | What it unlocks |
> |---------|----------------|
> | 🔍 Exa Search (RECOMMENDED) | **Web search + Reddit search + Twitter search** — one free key powers all three |
>
> Without Exa: I can read URLs you give me, but I cannot search the internet for you.
> With Exa: I can find information across the entire web, Reddit, and Twitter.
>
> Free tier: 1000 searches/month at https://exa.ai — more than enough for most users.
>
> ---
>
> **🟠 Proxy-based — needed only on servers, $1/month shared across channels:**
>
> | Channel | Why proxy needed | Without proxy |
> |---------|-----------------|---------------|
> | 📖 Reddit | Reddit blocks server IPs | **Reddit search still works via Exa (free!)** — you just can't read full posts with all comments |
> | 📺 Bilibili | Bilibili blocks server IPs | Won't work from server |
>
> [ONLY SHOW THIS SECTION IF USER SAID "SERVER"]
> [IF LOCAL: Skip this section — Reddit and Bilibili work directly on local computers]
>
> One proxy works for both. Recommend: https://www.webshare.io ($1/month residential proxy).
> Same proxy also works for Bilibili cookies-based access.
>
> ---
>
> **Which channels do you want me to set up?**
> (I recommend: **Exa Search** for sure, plus any cookie-based channels you actually use)

---

Wait for the user to choose. Then go to Step 4.

### Step 4: Run base installer

```bash
agent-eyes install --env=<local|server>
```

### Step 5: Configure each selected channel

Run the corresponding command for each channel the user chose.
Every configure command auto-tests and gives instant feedback (✅ or ❌).

---

#### Exa Search

Tell user: "Go to https://exa.ai, sign up (free), copy your API Key, and send it to me."

```bash
agent-eyes configure exa-key THE_KEY
```

---

#### Twitter/X

Tell user:
> "Open https://x.com in Chrome (make sure you're logged in).
> Press F12 → Application → Cookies → https://x.com
> Find these two values: **auth_token** and **ct0**
> Copy both and send them to me."

```bash
agent-eyes configure twitter-cookies AUTH_TOKEN CT0
```

---

#### YouTube (cookies for age-restricted videos)

Tell user:
> "Most YouTube videos work without any setup. If you want access to age-restricted or member-only videos:
> Which browser do you use? (chrome/firefox/edge/safari)"

```bash
agent-eyes configure youtube-cookies chrome
```
(replace `chrome` with whatever browser they use — yt-dlp reads cookies directly from the browser)

---

#### Bilibili

**If local**: Already works. No setup needed.

**If server**: Needs proxy (same proxy as Reddit, see Proxy section below).

If user also wants cookies for member-only content:
> "Open https://bilibili.com in Chrome (logged in).
> F12 → Application → Cookies → find **SESSDATA**
> Send it to me."

(For now, Bilibili public API works without cookies. Cookie support is for future member-only content.)

---

#### XiaoHongShu

Tell user:
> "Open https://www.xiaohongshu.com in Chrome (make sure you're logged in).
> Press F12 → Application → Cookies → https://www.xiaohongshu.com
> Select all cookies, right-click → Copy All
> Or just copy the full cookie string from a network request header.
> Send it to me."

```bash
agent-eyes configure xhs-cookie THE_COOKIE_STRING
```

---

#### Proxy (Reddit + Bilibili on server)

Tell user:
> "Reddit and Bilibili block server IPs. You need a residential proxy to access them.
> 1. Go to https://www.webshare.io
> 2. Sign up and get a residential proxy ($1/month is enough)
> 3. Copy your proxy address (format: http://username:password@ip:port)
> 4. Send it to me"

```bash
agent-eyes configure proxy THE_PROXY_URL
```

This configures the proxy for both Reddit and Bilibili at once.

---

### Step 6: Final health check

```bash
agent-eyes doctor
```

Summarize what's working for the user. Example:

> "✅ All done! Here's what I can do now:
>
> 📖 **Read**: Web, GitHub, YouTube, Bilibili, Twitter, XiaoHongShu, RSS
> 🔍 **Search**: Web, GitHub, Reddit, Twitter
>
> Try it out — ask me to search or read anything!"

---

## Quick Reference

| Action | Command |
|--------|---------|
| Install | `pip install git+https://github.com/Panniantong/agent-eyes.git` |
| Base setup | `agent-eyes install --env=<local\|server>` |
| Add Exa key | `agent-eyes configure exa-key YOUR_KEY` |
| Add Twitter | `agent-eyes configure twitter-cookies AUTH_TOKEN CT0` |
| Add YouTube | `agent-eyes configure youtube-cookies chrome` |
| Add XiaoHongShu | `agent-eyes configure xhs-cookie COOKIE_STRING` |
| Add proxy | `agent-eyes configure proxy http://user:pass@ip:port` |
| Health check | `agent-eyes doctor` |
| Read URL | `agent-eyes read <url>` |
| Search web | `agent-eyes search "query"` |
| Search GitHub | `agent-eyes search-github "query"` |
| Search Reddit | `agent-eyes search-reddit "query"` |
| Search Twitter | `agent-eyes search-twitter "query"` |
