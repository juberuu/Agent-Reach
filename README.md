# 👁️ Agent Eyes

**让你的 AI Agent 看见整个互联网。**

你的 AI Agent 很聪明，但是它看不见。它不能帮你刷 Reddit、搜 Twitter、读 B站视频。Agent Eyes 解决这个问题——装好之后，Agent 就能搜索和阅读互联网上几乎所有内容。

> 装一次，能力拉满。大部分功能零配置、零花费。

[English](docs/README_en.md)

---

## 30 秒上手

把这句话复制给你的 AI Agent：

```
帮我安装 Agent Eyes：https://raw.githubusercontent.com/Panniantong/agent-eyes/main/docs/install.md
```

> 💡 不知道怎么发？打开你的 Agent 对话框（Claude Code 终端、OpenClaw 聊天、Cursor Chat），直接粘贴上面这段话就行。

Agent 会自动装好并告诉你哪些功能已经可以用了。你最多需要回答 1-2 个问题。

<details>
<summary>想手动装？点这里</summary>

```bash
pip install https://github.com/Panniantong/agent-eyes/archive/main.zip
agent-eyes install --env=auto
agent-eyes doctor
```
</details>

---

## 装好就能用的

不需要任何配置，装好直接用：

- 🌐 **网页** — 给个 URL，帮你读出来
- 📦 **GitHub** — 仓库、Issue、PR、代码搜索
- 📺 **YouTube** — 自动提取视频字幕
- 📺 **B站** — 视频信息 + 字幕提取
- 📡 **RSS** — 任意订阅源
- 🐦 **Twitter** — 读单条推文

```bash
agent-eyes read "https://github.com/openai/gpt-4"
agent-eyes read "https://www.bilibili.com/video/BV1xx411c7mD"
agent-eyes search-github "LLM 框架"
```

---

## 一个 Key 解锁搜索

注册 [Exa](https://exa.ai)（免费，1000 次/月），一个 Key 同时解锁 **全网搜索 + Reddit 搜索 + Twitter 搜索**：

```bash
agent-eyes configure exa-key 你的KEY

agent-eyes search "2025 最好的开源 LLM"
agent-eyes search-reddit "best self-hosted LLM" --sub LocalLLaMA
agent-eyes search-twitter "AI agent"
```

> 没有 Exa Key 也能用——只是不能搜索，读取功能不受影响。

---

## 解锁更多平台

### 🍪 Cookie 解锁（免费，2 分钟）

本地电脑一键导入所有 cookies：

```bash
agent-eyes configure --from-browser chrome
```

> 关掉 Chrome 再运行。支持 chrome / firefox / edge / brave / opera。

服务器用户？装个 [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) 浏览器扩展，在网站上点一下 Export → Header String，粘贴给 Agent 就行。

Cookie 能解锁：

| 平台 | 额外能力 |
|------|---------|
| 🐦 Twitter | 时间线搜索、完整线程、高级搜索 |
| 📕 小红书 | 笔记内容 + 评论 |

### 🌐 代理解锁（$1/月，仅服务器需要）

Reddit 和 B站封服务器 IP。本地电脑不受影响。

```bash
agent-eyes configure proxy http://用户名:密码@IP:端口
```

> 推荐 [Webshare](https://webshare.io)，$1/月。一个代理同时解锁 Reddit + B站。
>
> 不买也行——Reddit **搜索** 通过 Exa 免费可用，只是不能读完整帖子。

---

## 三种使用方式

### 命令行

```bash
agent-eyes read "https://任意URL"
agent-eyes search "任意搜索词"
agent-eyes search-github "关键词"
agent-eyes search-reddit "关键词"
agent-eyes search-twitter "关键词"
agent-eyes doctor
```

### Python

```python
from agent_eyes import AgentEyes
import asyncio

eyes = AgentEyes()
result = asyncio.run(eyes.read("https://example.com"))
results = asyncio.run(eyes.search("AI agent"))
```

### MCP Server（Claude Code / Cursor）

```bash
pip install agent-eyes[mcp]
```

```json
{
  "mcpServers": {
    "agent-eyes": {
      "command": "python",
      "args": ["-m", "agent_eyes.integrations.mcp_server"]
    }
  }
}
```

---

## 配置速查

| 命令 | 作用 |
|------|------|
| `agent-eyes doctor` | 查看所有频道状态 |
| `agent-eyes configure --from-browser chrome` | 一键导入 cookies（本地）|
| `agent-eyes configure exa-key KEY` | 解锁全网搜索 |
| `agent-eyes configure twitter-cookies "..."` | 解锁 Twitter 高级 |
| `agent-eyes configure xhs-cookie "..."` | 解锁小红书 |
| `agent-eyes configure proxy URL` | 解锁 Reddit + B站（服务器）|

---

## 为什么用 Agent Eyes？

**不是框架，不是 SDK，就是胶水。**

- 把最好的免费工具粘在一起：Jina Reader、birdx、yt-dlp、Exa、feedparser
- 每个平台就是一个 ~50 行的薄封装，换后端只改一个文件
- CLI、MCP Server、Python API 三种接入方式
- 99% 功能免费，剩下 1% 也就 $1/月

<details>
<summary>架构图</summary>

```
┌─────────────────────────────────────────┐
│           Agent Eyes（纯胶水）             │
│                                          │
│  web.py      → Jina Reader API           │
│  github.py   → GitHub API                │
│  twitter.py  → birdx + Jina              │
│  youtube.py  → yt-dlp                    │
│  reddit.py   → Reddit JSON API           │
│  bilibili.py → Bilibili API              │
│  rss.py      → feedparser                │
│  exa.py      → Exa Search API            │
│  xhs.py      → XHS Web API               │
│                                          │
│  CLI · MCP Server · Python API            │
└─────────────────────────────────────────┘
```
</details>

---

## 致谢

- [Jina Reader](https://r.jina.ai) — 网页阅读
- [birdx](https://github.com/runesleo/birdx) by [@runes_leo](https://x.com/runes_leo) — Twitter
- [Exa](https://exa.ai) — 语义搜索
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — YouTube
- [feedparser](https://github.com/kurtmckee/feedparser) — RSS

## License

MIT
