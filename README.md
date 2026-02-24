# 👁️ Agent Eyes

**一行命令，让你的 AI Agent 看见整个互联网。**

你的 AI Agent 很聪明，但几乎是个瞎子。Reddit 封 IP、Twitter API 要 $100/月、B站屏蔽服务器、小红书需要登录——每个平台都有自己的坑，你要一个一个去踩。

Agent Eyes 把最好的开源工具粘在一起，一次安装全部搞定。

---

## 支持的平台

| 平台 | 能力 | 配置难度 | 说明 |
|------|------|:--------:|------|
| 🌐 **网页** | 阅读 | 零配置 | 任意 URL → 干净 Markdown（[Jina Reader](https://github.com/jina-ai/reader) ⭐9.8K 驱动） |
| 🐦 **Twitter/X** | 阅读 · 搜索 | 零配置 / Cookie | 单条推文零配置可读（Jina Reader）。装 [birdx](https://github.com/runesleo/birdx) + Cookie 解锁搜索、时间线、发推 |
| 📕 **小红书** | 阅读 · 搜索 · **发帖 · 评论 · 点赞 · 收藏** | Cookie | 完整操作能力：发图文/视频笔记、回复评论、查看用户主页 |
| 🔍 **全网搜索** | 搜索 | 免费 Key | AI 语义搜索，一个 Key 搜全网 + Reddit + Twitter（[Exa](https://exa.ai) 驱动） |
| 📦 **GitHub** | 阅读 · 搜索 | 零配置 | 公开仓库代码、README、搜索（[GitHub API](https://docs.github.com/en/rest) 驱动）。设 token 可访问私有仓库 |
| 📺 **YouTube** | 阅读 | 零配置 | 1800+ 视频网站字幕提取（[yt-dlp](https://github.com/yt-dlp/yt-dlp) ⭐148K 驱动） |
| 📺 **B站** | 阅读 | 零配置 / 代理 | 视频信息 + 字幕。本地直接用，服务器需代理 |
| 📡 **RSS** | 阅读 | 零配置 | 任意 RSS/Atom 源（[feedparser](https://github.com/kurtmckee/feedparser) ⭐2.3K 驱动） |
| 📖 **Reddit** | 搜索 · 阅读 | 免费 / 代理 | 搜索通过 Exa 免费可用；完整阅读需代理 |

> **配置难度说明：** 零配置 = 装好即用 · 免费 Key = 30 秒注册 · Cookie = 从浏览器导出 · 代理 = $1/月

[English](docs/README_en.md)

---

## 30 秒上手

复制给你的 AI Agent（Claude Code、OpenClaw、Cursor 等）：

```
帮我安装 Agent Eyes：https://raw.githubusercontent.com/Panniantong/agent-eyes/main/docs/install.md
```

Agent 自动安装、检测环境、告诉你哪些功能已经可以用。

<details>
<summary>手动安装</summary>

```bash
pip install https://github.com/Panniantong/agent-eyes/archive/main.zip
agent-eyes install --env=auto
```
</details>

---

## 装好就能用

不需要任何配置：

```bash
agent-eyes read "https://任意网页"                          # 网页
agent-eyes read "https://github.com/openai/gpt-4"          # GitHub
agent-eyes read "https://www.youtube.com/watch?v=xxx"       # YouTube 字幕
agent-eyes read "https://www.bilibili.com/video/BVxxx"      # B站字幕
agent-eyes read "https://x.com/elonmusk/status/xxx"         # 推文
agent-eyes read "https://hnrss.org/frontpage"               # RSS
agent-eyes search-github "LLM 框架"                         # GitHub 搜索
```

---

## 按需解锁

不用的不用配。每一步都可以跳过。

### 🔍 搜索 — 免费，30 秒

一个 [Exa](https://exa.ai) Key（免费 1000 次/月），同时解锁三个搜索：

```bash
agent-eyes configure exa-key 你的KEY

agent-eyes search "2025 最好的开源 AI 工具"
agent-eyes search-reddit "best LLM" --sub LocalLLaMA
agent-eyes search-twitter "Claude Code"
```

### 🍪 Cookie — 免费，2 分钟

解锁 Twitter 发推/搜索 + 小红书全功能。本地电脑一键导入：

```bash
agent-eyes configure --from-browser chrome
```

> 服务器用户？装个 [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) 扩展，Export → Header String，粘贴给 Agent。

### 🌐 代理 — $1/月，仅服务器需要

Reddit 和 B站封服务器 IP。一个代理解决两个：

```bash
agent-eyes configure proxy http://用户名:密码@IP:端口
```

> Reddit 搜索通过 Exa 免费可用，不买代理也能搜。推荐 [Webshare](https://webshare.io)，$1/月。

---

## 状态一目了然

```
$ agent-eyes doctor

👁️  Agent Eyes Status
========================================

✅ Ready (no setup needed):
  ✅ GitHub repos and code — Public repos only
  ✅ Twitter/X posts — Full access (search + timeline + threads)
  ✅ YouTube video transcripts — yt-dlp
  ⚠️  Bilibili video info — May be blocked on servers
  ✅ RSS and Atom feeds — feedparser
  ✅ Web pages (any URL) — Jina Reader API

🔍 Search (need free Exa API key):
  ⬜ Semantic web search

🔧 Optional (advanced setup):
  ⬜ Reddit posts and comments — Need proxy
  ⬜ XiaoHongShu (小红书) — Need cookies

Status: 6/9 channels active
```

---

## 接入方式

### CLI
```bash
agent-eyes read "URL"
agent-eyes search "关键词"
agent-eyes doctor
```

### Python
```python
from agent_eyes import AgentEyes
import asyncio
eyes = AgentEyes()
asyncio.run(eyes.read("https://example.com"))
asyncio.run(eyes.search("AI agent"))
```

### MCP Server（Claude Code / Cursor）

<details>
<summary>配置</summary>

```json
{"mcpServers": {"agent-eyes": {"command": "python", "args": ["-m", "agent_eyes.integrations.mcp_server"]}}}
```
</details>

---

## 速查

| 命令 | 作用 |
|------|------|
| `agent-eyes doctor` | 查看状态 |
| `agent-eyes configure --from-browser chrome` | 一键导入 cookies |
| `agent-eyes configure exa-key KEY` | 解锁搜索 |
| `agent-eyes configure twitter-cookies "..."` | 解锁 Twitter |
| `agent-eyes configure xhs-cookie "..."` | 解锁小红书 |
| `agent-eyes configure proxy URL` | 解锁 Reddit + B站 |

---

## 设计

胶水，不是框架。每个频道 ~50 行代码，换后端改一个文件。

<details>
<summary>架构</summary>

```
web.py      → Jina Reader     github.py   → GitHub API
youtube.py  → yt-dlp          bilibili.py → Bilibili API
twitter.py  → birdx           reddit.py   → Reddit JSON
exa.py      → Exa Search      rss.py      → feedparser
xhs.py      → XHS Web API
```
</details>

## 致谢

[Jina Reader](https://github.com/jina-ai/reader) · [yt-dlp](https://github.com/yt-dlp/yt-dlp) · [birdx](https://github.com/runesleo/birdx) · [Exa](https://exa.ai) · [feedparser](https://github.com/kurtmckee/feedparser)

MIT License
