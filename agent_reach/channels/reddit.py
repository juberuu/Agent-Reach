# -*- coding: utf-8 -*-
"""Reddit — search and read via rdt-cli (public-clis/rdt-cli).

NOTE: Reddit requires authentication since 2024. All API requests
(including public subreddit reads) return HTTP 403 without a valid
session cookie. Run `rdt login` after installation to authenticate.
"""

import json
import shutil
import subprocess

from agent_reach.utils.process import utf8_subprocess_env

from .base import Channel

_CREDENTIAL_FILE = "~/.config/rdt-cli/credential.json"
# Pinned to the 0.4.2 state — PyPI still only has 0.4.1 (upstream issue #10).
_RDT_GIT_SOURCE = "git+https://github.com/public-clis/rdt-cli.git@5e4fb3720d5c174e976cd425ccc3b879d52cac66"

#: shell 对"找到但不可执行/找不到"使用的退出码（对齐 agent_reach.probe）
_BROKEN_EXIT_CODES = (126, 127)

#: rdt 应从固定 git 源安装（PyPI 落后），断链处方与 probe 默认的 pipx/uv 不同
_RDT_BROKEN_HINT = (
    "rdt 命令存在但无法执行——通常是系统 Python 升级后 venv 解释器丢失。\n"
    "PyPI 版本落后，推荐用固定 git 源强制重装：\n"
    f"  pipx install --force '{_RDT_GIT_SOURCE}'"
)


class RedditChannel(Channel):
    name = "reddit"
    description = "Reddit 帖子和评论"
    backends = ["rdt-cli"]
    tier = 1  # Reddit requires login since 2024 (rdt login) — not zero-config

    def can_handle(self, url: str) -> bool:
        from urllib.parse import urlparse

        d = urlparse(url).netloc.lower()
        return "reddit.com" in d or "redd.it" in d

    def check(self, config=None):
        self.active_backend = None

        rdt = shutil.which("rdt")
        if not rdt:
            return "off", (
                "需要安装 rdt-cli。PyPI 版本可能暂时落后，推荐直接从 GitHub 安装：\n"
                f"  pipx install '{_RDT_GIT_SOURCE}'\n"
                "如已确认 PyPI 版本已更新，也可使用：\n"
                "  pipx install rdt-cli\n"
                "  uv tool install rdt-cli\n"
                "最新源码：https://github.com/public-clis/rdt-cli\n"
                "安装后运行 `rdt login` 登录（需先在浏览器登录 reddit.com）"
            )

        # 不走 probe_command：实测 `rdt status --json` 成功时（rc=0）也会向 stderr
        # 打网络重试日志，probe 把 stdout+stderr 合并后 JSON 解析必炸。
        # 故保留手写 subprocess（stdout 单独捕获），但异常分类对齐 probe 语义：
        # exec 失败/126/127 → broken（venv 断链处方），TimeoutExpired → 超时。
        try:
            r = subprocess.run(
                [rdt, "status", "--json"],
                capture_output=True,
                encoding="utf-8",
                errors="replace",
                timeout=10,
                env=utf8_subprocess_env(),
            )
        except subprocess.TimeoutExpired:
            return "error", "rdt 响应超时（>10s），Reddit 状态未知。稍后重试或运行 `rdt status` 查看详情"
        except OSError:
            # 含 FileNotFoundError：which 命中但 exec 失败 = venv 断链（probe 的 broken）
            return "error", _RDT_BROKEN_HINT

        if r.returncode in _BROKEN_EXIT_CODES:
            return "error", _RDT_BROKEN_HINT

        if r.returncode != 0:
            detail = (r.stderr or r.stdout or "").strip().splitlines()
            tail = detail[-1] if detail else "无输出"
            return "error", f"rdt 异常退出（exit {r.returncode}）：{tail}。运行 `rdt status` 查看详情"

        # 进程正常退出 → rdt 本身是活的（无论登录与否），后端即为可用
        self.active_backend = "rdt-cli"

        try:
            data = json.loads(r.stdout or "")
        except json.JSONDecodeError:
            data = None
        if not isinstance(data, dict):
            return "warn", "rdt-cli 可用但状态输出无法解析，运行 `rdt status` 查看登录状态"

        info = data.get("data")
        if not isinstance(info, dict):
            info = {}
        authenticated = info.get("authenticated", False)
        username = info.get("username") or ""

        if authenticated:
            suffix = f"（已登录：{username}）" if username else ""
            return "ok", (f"rdt-cli 可用{suffix}（搜索帖子、阅读全文、查看评论）")

        return "warn", (
            "rdt-cli 已安装但未登录。Reddit 自 2024 年起要求认证，"
            "未登录时所有请求均返回 403。\n\n"
            "方法一（自动）：运行 `rdt login`\n"
            "  先在浏览器登录 reddit.com，再运行此命令自动提取 Cookie。\n\n"
            "方法二（手动，适用于 Chrome/Edge 127+ 无法自动提取时）：\n"
            "  1. Chrome 应用商店安装 Cookie-Editor 扩展：\n"
            "     https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm\n"
            "  2. 在浏览器打开 reddit.com（确保已登录）\n"
            "  3. 点击 Cookie-Editor 图标，找到 `reddit_session`，复制其 Value\n"
            f"  4. 将以下内容写入 {_CREDENTIAL_FILE}：\n"
            '     {"cookies": {"reddit_session": "<粘贴 Value>"}, '
            '"source": "manual", "username": "<你的用户名>", '
            '"modhash": null, "saved_at": 0, "last_verified_at": null}\n\n'
            "验证：`rdt status --json` 确认 authenticated: true"
        )
