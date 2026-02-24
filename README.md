# 👁️ Agent Eyes

**一行命令，让你的 AI Agent 看见整个互联网。**

你的 AI Agent 很聪明，但几乎是个瞎子。Reddit 封 IP、Twitter API 要 $100/月、B站屏蔽服务器、小红书需要登录——每个平台都有自己的坑，你要一个一个去踩。

Agent Eyes 把互联网上最好的开源工具粘在一起，一次安装全部搞定：

| 工具 | 它解决了什么 | Stars |
|------|------------|:-----:|
| [Jina Reader](https://github.com/jina-ai/reader) | 任意网页 → 干净 Markdown，处理 JS 渲染，去掉广告 | ⭐ 9.8K |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | **1800+ 个视频网站**的字幕提取（YouTube、B站、TikTok…） | ⭐ 148K |
| [Exa](https://exa.ai) | AI 语义搜索引擎，一个 Key 搜全网 + Reddit + Twitter | — |
| [birdx](https://github.com/runesleo/birdx) | 不花 $100/月，用 Cookie 就能搜 Twitter 时间线和线程 | — |
| [feedparser](https://github.com/kurtmckee/feedparser) | 万能 RSS/Atom 解析 | ⭐ 2.3K |

> 不造轮子，只做胶水。统一安装、统一配置、统一接口。

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

不需要任何配置，装完直接用：

```bash
agent-eyes read "https://任意网页"                          # Jina Reader 驱动
agent-eyes read "https://github.com/openai/gpt-4"          # GitHub 仓库/Issue/PR
agent-eyes read "https://www.youtube.com/watch?v=xxx"       # yt-dlp 驱动
agent-eyes read "https://www.bilibili.com/video/BVxxx"      # B站字幕
agent-eyes read "https://x.com/elonmusk/status/xxx"         # 推文
agent-eyes read "https://hnrss.org/frontpage"               # RSS 订阅
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

解锁 Twitter 高级搜索 + 小红书。本地电脑一键导入：

```bash
agent-eyes configure --from-browser chrome
```

> 服务器用户？装个 [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) 扩展，Export → Header String，粘贴给 Agent。

### 🌐 代理 — $1/月，仅服务器需要

Reddit 和 B站封服务器 IP。一个代理解决两个：

```bash
agent-eyes configure proxy http://用户名:密码@IP:端口
```

> Reddit 搜索通过 Exa 免费可用，不买代理也能搜，只是读不了完整帖子。
> 推荐 [Webshare](https://webshare.io)，$1/月。

---

## 状态一目了然

```
$ agent-eyes doctor

👁️  Agent Eyes Status
✅ Web [Jina Reader]      ✅ GitHub [API]          ✅ RSS [feedparser]
✅ YouTube [yt-dlp]       ✅ Bilibili [API]        ✅ Twitter [birdx]
⬜ Search [need Exa key]  ⬜ XiaoHongShu [cookies] ⬜ Reddit [proxy]

6/9 active
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
