# Agent Eyes — Installation Guide

## For Humans

Copy and paste this to your AI Agent (Claude Code, OpenClaw, Cursor, etc.):

```
Install and configure Agent Eyes by following the instructions here:
https://raw.githubusercontent.com/Panniantong/agent-eyes/main/docs/install.md
```

That's it. Your Agent will handle the rest.

---

## For AI Agents

You are installing Agent Eyes — a tool that gives you (the Agent) eyes to see the entire internet.
Follow this decision tree exactly. Do not skip steps.

### Step 1: Ask user 3 questions

Ask the user these questions to determine install flags:

**Q1: Are you on a local computer or a server/VPS?**
- Local → `--env=local`
- Server/VPS → `--env=server`

**Q2: Do you want web search? (free, recommended)**
- Yes → `--search=yes`
- No → `--search=no`

**Q3: (Only if server) Do you have a residential proxy for Reddit/Bilibili?**
- Yes → `--proxy=http://user:pass@ip:port` (ask user for the proxy URL)
- No / Don't know → omit `--proxy`
- Tell user: "Reddit and Bilibili block server IPs. You can get a proxy at https://www.webshare.io for $1/month. Want to set it up later?"

### Step 2: Install

```bash
pip install git+https://github.com/Panniantong/agent-eyes.git
```

If fails, try `pip3` or add `--user`.

### Step 3: Run installer with flags

Based on answers from Step 1, construct and run ONE command:

```bash
agent-eyes install --env=<local|server> --search=<yes|no> [--proxy=<proxy_url>]
```

**Examples:**
- Local, wants search: `agent-eyes install --env=local --search=yes`
- Server, wants search, has proxy: `agent-eyes install --env=server --search=yes --proxy=http://user:pass@ip:port`
- Server, wants search, no proxy: `agent-eyes install --env=server --search=yes`
- Local, no search: `agent-eyes install --env=local --search=no`

### Step 4: Configure Exa key (only if --search=yes)

The installer will tell you search needs a key. Ask the user:

> "Web search needs a free API key. Go to https://exa.ai, sign up, copy your API Key, and send it to me."

When user provides the key, run:

```bash
agent-eyes configure exa-key THE_KEY_USER_PROVIDED
```

This automatically tests the key and confirms it works.

### Step 5: Configure proxy (only if --env=server and user wants Reddit/Bilibili)

If the user wants to set up a proxy (now or later), they need to:
1. Go to https://www.webshare.io and sign up ($1/month for residential proxy)
2. Get their proxy URL (format: `http://username:password@ip:port`)
3. Send it to you

Then run:

```bash
agent-eyes configure proxy THE_PROXY_URL
```

This automatically tests the proxy against Reddit and confirms it works.

### Step 6: Final verification

```bash
agent-eyes doctor
```

Report results to the user. Example:

> "✅ Agent Eyes is ready! Here's what I can do:
> - 📖 Read: Web, GitHub, YouTube, Bilibili, RSS, Tweets
> - 🔍 Search: Web, GitHub, Reddit, Twitter
> 
> Try it: ask me to search or read anything!"

### Summary of commands

| Action | Command |
|--------|---------|
| Install | `pip install git+https://github.com/Panniantong/agent-eyes.git` |
| One-shot setup | `agent-eyes install --env=local --search=yes` |
| Add Exa key | `agent-eyes configure exa-key YOUR_KEY` |
| Add proxy | `agent-eyes configure proxy http://user:pass@ip:port` |
| Add GitHub token | `agent-eyes configure github-token YOUR_TOKEN` |
| Health check | `agent-eyes doctor` |
| Read URL | `agent-eyes read <url>` |
| Search web | `agent-eyes search "query"` |
| Search GitHub | `agent-eyes search-github "query"` |
| Search Reddit | `agent-eyes search-reddit "query"` |
| Search Twitter | `agent-eyes search-twitter "query"` |

### Troubleshooting

| Problem | Solution |
|---------|----------|
| `pip: command not found` | Try `pip3` |
| `Permission denied` | Add `--user` flag |
| `agent-eyes: command not found` | Use `python3 -m agent_eyes.cli` instead |
| Search returns "Exa API key not configured" | `agent-eyes configure exa-key YOUR_KEY` |
| Reddit returns 403 | `agent-eyes configure proxy http://user:pass@ip:port` |
