---
name: agent-reach
description: >
  MUST USE when user wants to research/search/look up/find anything on the
  internet — e.g. "research this topic", "do a deep dive on X", "search the
  web for X", "see what people say about X", "look this up".

  Also MUST USE when user mentions any platform or shares any URL/link:
  Twitter/X, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu,
  Xiaoyuzhou Podcast, LinkedIn/jobs/recruiting, V2EX, Xueqiu (stocks), RSS.

  13 platforms, multi-backend routing (OpenCLI / per-platform CLIs / APIs).
  Zero config for 6 channels. Run `agent-reach doctor --json` to see which
  backend serves each platform right now.

  Triggers: "research", "deep dive", "search twitter", "search xiaohongshu",
  "watch this video", "search the web", "look this up", "youtube transcript",
  "search reddit", "read this link", "bilibili", "V2EX",
  "xiaoyuzhou", "podcast", "xueqiu", "stock quote", "雪球", "股票".
metadata:
  openclaw:
    homepage: https://github.com/Panniantong/Agent-Reach
---

# Agent Reach — Usage Guide

Upstream tools for 13 platforms. Call them directly.

Run `agent-reach doctor` to check which channels are available.

## ⚠️ Workspace Rules

**Never create files in the agent workspace.** Use `/tmp/` for temporary output and `~/.agent-reach/` for persistent data.

## Web — Any URL

```bash
curl -s "https://r.jina.ai/URL"
```

## Web Search (Exa)

```bash
mcporter call 'exa.web_search_exa(query: "query", numResults: 5)'
mcporter call 'exa.get_code_context_exa(query: "code question", tokensNum: 3000)'
```

## Twitter/X (twitter-cli)

```bash
twitter -c search "query" -n 10            # search (-c = compact JSON, LLM-friendly)
twitter -c tweet URL_OR_ID                 # read tweet + replies (supports /status/ URLs)
twitter -c article URL_OR_ID               # read a Twitter Article
twitter -c user-posts @username -n 20      # user timeline
twitter -c feed -n 20                      # home timeline
```

> Binary is `twitter` (`pipx install twitter-cli`, ≥ 0.8.5). The `bird` name in older docs has been retired. If `search` returns 404, run `pipx upgrade twitter-cli`.

## YouTube (yt-dlp)

```bash
yt-dlp --dump-json "URL"                     # video metadata
yt-dlp --write-sub --write-auto-sub --sub-lang "zh-Hans,zh,en" --skip-download -o "/tmp/%(id)s" "URL"
                                             # download subtitles, then read the .vtt file
yt-dlp --dump-json "ytsearch5:query"         # search
```

## Bilibili (bili-cli / OpenCLI)

> ⚠️ Do NOT use yt-dlp for bilibili — its risk control 412-blocks yt-dlp in
> every configuration (verified 2026-06). yt-dlp is for YouTube only.

```bash
bili video BVxxx                         # video detail, no login needed
bili search "query" --type video -n 5    # search
bili hot -n 10                           # trending
opencli bilibili subtitle BVxxx          # subtitles (desktop Chrome)
```

## Reddit (login required — no zero-config path)

> Anonymous .json endpoints are 403-blocked and official API registration is
> approval-gated (2025-11). Every backend needs a logged-in session.
> Check `agent-reach doctor --json` for the active backend.

```bash
opencli reddit search "query" -f yaml    # desktop, browser session
rdt search "query" --limit 10            # legacy/server, cookie login
rdt read POST_ID                         # post + comments
```

## GitHub (gh CLI)

```bash
gh search repos "query" --sort stars --limit 10
gh repo view owner/repo
gh search code "query" --language python
gh issue list -R owner/repo --state open
gh issue view 123 -R owner/repo
```

## XiaoHongShu (multi-backend — check doctor for active backend)

```bash
# Desktop preferred: OpenCLI (reuses browser session, zero config)
opencli xiaohongshu search "query" -f yaml
opencli xiaohongshu note "NOTE_URL" -f yaml

# Server: xiaohongshu-mcp via mcporter (QR login; always pass --timeout 120000)
mcporter call 'xiaohongshu.search_feeds(keyword: "query")' --timeout 120000
mcporter call 'xiaohongshu.get_feed_detail(feed_id: "xxx", xsec_token: "yyy")' --timeout 120000

# Legacy fallback: xhs-cli (upstream unmaintained since 2026-03)
xhs search "query"
xhs read NOTE_ID_OR_URL
```

> Requires login. Use Cookie-Editor to import cookies.

> **Tip: Clean bloated output.** The XHS API returns large JSON with many unused fields.
> Pipe through the formatter to save context:
> ```bash
> mcporter call 'xiaohongshu.search_feeds(keyword: "query")' | agent-reach format xhs
> ```
> This keeps only: title, content, author, engagement counts, image URLs, and tags.

## Xiaoyuzhou Podcast (groq-whisper + ffmpeg)

```bash
# Transcribe a single podcast episode (outputs text to /tmp/)
~/.agent-reach/tools/xiaoyuzhou/transcribe.sh "https://www.xiaoyuzhoufm.com/episode/EPISODE_ID"
```

> Requires `ffmpeg` and a Groq API key (free).
> Configure the key with `agent-reach configure groq-key YOUR_KEY`.
> On first run, install the tools with `agent-reach install --env=auto`.
> Run `agent-reach doctor` to check status.
> Output Markdown files are saved to `/tmp/` by default.

## LinkedIn (mcporter)

```bash
mcporter call 'linkedin.get_person_profile(linkedin_url: "https://linkedin.com/in/username")'
mcporter call 'linkedin.search_people(keyword: "AI engineer", limit: 10)'
```

Fallback: `curl -s "https://r.jina.ai/https://linkedin.com/in/username"`

## V2EX (public API)

```bash
# Hot topics
curl -s "https://www.v2ex.com/api/topics/hot.json" -H "User-Agent: agent-reach/1.0"

# Topics in a node (node_name examples: python, tech, jobs, qna)
curl -s "https://www.v2ex.com/api/topics/show.json?node_name=python&page=1" -H "User-Agent: agent-reach/1.0"

# Topic details (extract topic_id from URLs like https://www.v2ex.com/t/1234567)
curl -s "https://www.v2ex.com/api/topics/show.json?id=TOPIC_ID" -H "User-Agent: agent-reach/1.0"

# Topic replies
curl -s "https://www.v2ex.com/api/replies/show.json?topic_id=TOPIC_ID&page=1" -H "User-Agent: agent-reach/1.0"

# User profile
curl -s "https://www.v2ex.com/api/members/show.json?username=USERNAME" -H "User-Agent: agent-reach/1.0"
```

Python example (`V2EXChannel`):

```python
from agent_reach.channels.v2ex import V2EXChannel

ch = V2EXChannel()

# Get hot topics (default 20 items)
# Returned fields: id, title, url, replies, node_name, node_title, content(first 200 chars), created
topics = ch.get_hot_topics(limit=10)
for t in topics:
    print(f"[{t['node_title']}] {t['title']} ({t['replies']} replies) {t['url']}")
    print(f"  id={t['id']} created={t['created']}")

# Get latest topics for a specific node
# Returned fields: id, title, url, replies, node_name, node_title, content(first 200 chars), created
node_topics = ch.get_node_topics("python", limit=5)
for t in node_topics:
    print(t["id"], t["title"], t["url"])

# Get one topic plus replies
# Returned fields: id, title, url, content, replies_count, node_name, node_title,
#                  author, created, replies (list of {author, content, created})
topic = ch.get_topic(1234567)
print(topic["title"], "—", topic["author"])
for r in topic["replies"]:
    print(f"  {r['author']}: {r['content'][:80]}")

# Get user info
# Returned fields: id, username, url, website, twitter, psn, github, btc, location, bio, avatar, created
user = ch.get_user("Livid")
print(user["username"], user["bio"], user["github"])

# Search (not supported by the public V2EX API; returns guidance instead)
result = ch.search("asyncio")
print(result[0]["error"])  # Use built-in site search or the Exa channel instead
```

> No auth required. Results are public JSON. V2EX node names are listed at https://www.v2ex.com/planes

## Xueqiu (public API)

```python
from agent_reach.channels.xueqiu import XueqiuChannel

ch = XueqiuChannel()

# Get stock quotes (symbol examples: SH600519 mainland China, SZ000858 Shenzhen, AAPL US, 00700 HK)
# Returned fields: symbol, name, current, percent, chg, high, low, open, last_close,
#                  volume, amount, market_capital, turnover_rate, pe_ttm, timestamp
quote = ch.get_stock_quote("AAPL")
print(f"{quote['name']} ({quote['symbol']}): {quote['current']} ({quote['percent']}%)")

# Search stocks
# Returned fields: symbol, name, exchange
stocks = ch.search_stock("Apple", limit=5)
for s in stocks:
    print(f"{s['name']} ({s['symbol']}) - {s['exchange']}")

# Hot posts
# Returned fields: id, title, text(first 200 chars), author, likes, url
posts = ch.get_hot_posts(limit=10)
for p in posts:
    print(f"{p['author']}: {p['text'][:50]}... ({p['likes']} likes)")

# Hot stocks (stock_type=10 popularity ranking, stock_type=12 watchlist ranking)
# Returned fields: symbol, name, current, percent, rank
hot = ch.get_hot_stocks(limit=10, stock_type=10)
for s in hot:
    print(f"#{s['rank']} {s['name']} ({s['symbol']}): {s['current']} ({s['percent']}%)")
```

> No login required. Agent Reach auto-fetches session cookies, and all public APIs can be used directly.

## RSS (feedparser)

```python
python3 -c "
import feedparser
for e in feedparser.parse('FEED_URL').entries[:5]:
    print(f'{e.title} — {e.link}')
"
```

## Troubleshooting

- **Channel not working?** Run `agent-reach doctor` — it shows status and fix instructions.
- **Twitter fetch failed?** Ensure `undici` is installed: `npm install -g undici`. Configure a proxy if needed: `agent-reach configure proxy URL`.

## Setting Up a Channel ("help me configure XXX")

If a channel needs setup (cookies, Docker, etc.), fetch the install guide:
https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md

The user only provides cookies. Everything else is your job.
