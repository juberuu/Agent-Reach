# Reddit 配置指南

## 功能说明

Reddit 封锁了几乎所有非浏览器的直接访问（包括数据中心和 ISP 代理 IP），JSON API 返回 403。

Agent Reach 通过 **Exa** 实现 Reddit 的搜索和阅读功能：
- **搜索**：`web_search_exa` + `includeDomains: ["reddit.com"]`
- **阅读完整帖子+评论**：`crawling_exa` 读取 Reddit URL 的缓存内容

免费，无需代理，无需 API Key。

## Agent 可自动完成的步骤

1. 检查 Exa 是否可用：
```bash
agent-reach doctor | grep -E "Reddit|Exa"
```

2. 如果 Exa 未安装，自动安装：
```bash
npm install -g mcporter
mcporter config add exa https://mcp.exa.ai/mcp
```

或一键安装：
```bash
agent-reach install --env=auto
```

## 使用示例

搜索 Reddit 内容：
```bash
mcporter call 'exa.web_search_exa(query: "python best practices", numResults: 5, includeDomains: ["reddit.com"])'
```

阅读完整帖子和评论：
```bash
mcporter call 'exa.crawling_exa(urls: ["https://www.reddit.com/r/python/comments/xxx/"], maxCharacters: 10000)'
```

## 需要用户手动做的步骤

无。Exa 通过 `agent-reach install --env=auto` 自动配置。
