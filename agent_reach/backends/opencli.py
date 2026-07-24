# -*- coding: utf-8 -*-
"""OpenCLI backend probing.

OpenCLI (github.com/jackwener/opencli) drives the user's real Chrome via a
browser-bridge extension + local daemon, reusing existing login sessions —
zero per-platform configuration, desktop-only (no headless).

Probing notes (verified live):
  - `opencli doctor` AUTO-STARTS the daemon — a side effect, so health
    checks must use `opencli daemon status` (pure query) instead.
  - Exit codes are always 0; status must be parsed from text output.
  - "Extension: disconnected" can mean a sleeping service worker, a disabled
    extension, or an extension that was never loaded. Disk files distinguish
    possible installation sources, but only a live daemon connection proves
    the browser actually loaded and enabled the extension.
"""

import glob
import os
from dataclasses import dataclass

from agent_reach.probe import probe_command

OPENCLI_PACKAGE = "@jackwener/opencli"
OPENCLI_EXTENSION_ID = "ildkmabpimmkaediidaifkhjpohdnifk"
OPENCLI_EXTENSION_URL = (
    f"https://chromewebstore.google.com/detail/opencli/{OPENCLI_EXTENSION_ID}"
)

# OpenCLIApp 0.1.35 injected this now-unsupported variable into every child.
# OpenCLI >=1.8.5 rejects it before even handling ``--version``.  Doctor is a
# read-only observer, so strip the stale app setting only from its child probes.
_UNSUPPORTED_APP_ENV = ("OPENCLI_DAEMON_PORT",)

#: Chromium-family profile roots that contain <Profile>/Extensions/<id>/
_CHROME_PROFILE_ROOTS = (
    "~/Library/Application Support/Google/Chrome",  # macOS Chrome
    "~/Library/Application Support/Chromium",       # macOS Chromium
    "~/Library/Application Support/Microsoft Edge",  # macOS Edge
    "~/.config/google-chrome",                      # Linux Chrome
    "~/.config/chromium",                           # Linux Chromium
    "~/.config/microsoft-edge",                     # Linux Edge
)

_OPENCLI_UNPACKED_EXTENSION = "~/.opencli/extension"


def _extension_installed_on_disk() -> bool:
    """True if store-installed OpenCLI files exist in a browser profile.

    This is disk evidence only: a user may have disabled or removed the
    extension while stale files remain, so callers must not treat it as proof
    that the extension is loaded, connected, or usable.
    """
    roots = [os.path.expanduser(p) for p in _CHROME_PROFILE_ROOTS]
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:  # Windows
        roots.append(os.path.join(local_app_data, "Google", "Chrome", "User Data"))
        roots.append(os.path.join(local_app_data, "Microsoft", "Edge", "User Data"))
    for root in roots:
        if glob.glob(os.path.join(root, "*", "Extensions", OPENCLI_EXTENSION_ID)):
            return True
    return False


def _unpacked_extension_files_present() -> bool:
    """True when OpenCLI's unpacked extension source contains a manifest.

    ``~/.opencli/extension`` is downloaded source, not browser state.  Its
    existence never proves the user completed “Load unpacked” or left the
    extension enabled.
    """
    unpacked = os.path.expanduser(_OPENCLI_UNPACKED_EXTENSION)
    return os.path.isfile(os.path.join(unpacked, "manifest.json"))


@dataclass
class OpenCLIStatus:
    installed: bool = False
    broken: bool = False
    daemon_running: bool = False
    extension_connected: bool = False
    extension_installed: bool = False
    unpacked_extension_files: bool = False
    version: str = ""
    hint: str = ""

    @property
    def ready(self) -> bool:
        """True only when the backend is provably usable now.

        Only a live daemon connection proves that a browser loaded and enabled
        the extension. Disk files alone are deliberately not enough.
        """
        return self.installed and not self.broken and self.extension_connected


def opencli_status(timeout: int = 10) -> OpenCLIStatus:
    """Probe OpenCLI install + daemon/extension state without side effects."""
    version_probe = probe_command(
        "opencli",
        ["--version"],
        timeout=timeout,
        package=OPENCLI_PACKAGE,
        remove_env=_UNSUPPORTED_APP_ENV,
    )
    if version_probe.status == "missing":
        return OpenCLIStatus(installed=False)
    if not version_probe.ok:
        return OpenCLIStatus(
            installed=True,
            broken=True,
            hint=(
                "opencli 命令存在但无法执行（node 环境损坏），重装：\n"
                f"  npm install -g {OPENCLI_PACKAGE}"
            ),
        )

    st = OpenCLIStatus(installed=True, version=version_probe.output.strip())

    daemon_probe = probe_command(
        "opencli",
        ["daemon", "status"],
        timeout=timeout,
        package=OPENCLI_PACKAGE,
        remove_env=_UNSUPPORTED_APP_ENV,
    )
    output = daemon_probe.output if daemon_probe.ok else ""
    # `opencli daemon status` prints lines like:
    #   Daemon: running (PID 37389) / Daemon: not running
    #   Extension: connected / Extension: disconnected
    for line in output.splitlines():
        line = line.strip().lower()
        if line.startswith("daemon:"):
            st.daemon_running = "not running" not in line and "running" in line
        elif line.startswith("extension:"):
            st.extension_connected = "disconnected" not in line and "connected" in line

    if not st.extension_connected:
        st.extension_installed = _extension_installed_on_disk()
        st.unpacked_extension_files = _unpacked_extension_files_present()
        if st.extension_installed:
            st.hint = (
                "检测到 Chrome/Edge 的 OpenCLI 扩展文件，但扩展当前未连接；"
                "仅凭磁盘文件无法确认它已加载或启用。\n"
                "  打开浏览器扩展页确认 OpenCLI 已启用，再运行一个 opencli 命令验证"
            )
        elif st.unpacked_extension_files:
            st.hint = (
                "检测到 ~/.opencli/extension/ 源文件，但文件存在不代表已经在"
                " Chrome/Edge 中“加载已解压的扩展程序”。\n"
                "  请在浏览器扩展页加载并启用该目录，再运行一个 opencli 命令验证"
            )
        else:
            st.hint = (
                "OpenCLI 已安装，但未检测到已连接的浏览器扩展。\n"
                f"  1. 安装并启用扩展（Chrome/Edge）：{OPENCLI_EXTENSION_URL}\n"
                "  2. 保持浏览器打开，再运行一个 opencli 命令验证"
            )
    return st


def opencli_summary(st: OpenCLIStatus) -> str:
    """One-line state description for channel messages / install output."""
    if not st.installed:
        return "OpenCLI 未安装"
    if st.broken:
        return "OpenCLI 无法执行（node 环境损坏）"
    if st.extension_connected:
        return f"OpenCLI 可用（浏览器登录态，v{st.version}）"
    if st.extension_installed:
        return "OpenCLI 已安装，检测到扩展文件但当前未连接（无法确认已加载）"
    if st.unpacked_extension_files:
        return "OpenCLI 已安装，检测到 unpacked 源文件但尚未确认浏览器已加载"
    if st.daemon_running:
        return "OpenCLI 已安装，等待 Chrome 扩展安装"
    return "OpenCLI 已安装（daemon 未运行，使用时自动启动；需 Chrome 扩展）"
