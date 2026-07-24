# -*- coding: utf-8 -*-
"""Regression tests for P0 CLI safety and configuration failures."""

from __future__ import annotations

import subprocess
import sys
from argparse import Namespace
from pathlib import Path

import pytest

import agent_reach.cli as cli


class _MemoryConfig:
    def __init__(self):
        self.data = {}

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value


def test_browser_cookie_import_requires_explicit_platform(monkeypatch):
    """A bare --from-browser must fail before any browser credential access."""
    import agent_reach.config as config_module
    import agent_reach.cookie_extract as cookie_extract

    monkeypatch.setattr(config_module, "Config", _MemoryConfig)
    monkeypatch.setattr(cli, "_configure_logging", lambda _verbose=False: None)
    monkeypatch.setattr(
        cookie_extract,
        "configure_from_browser",
        lambda *_args, **_kwargs: pytest.fail("browser cookie reader must not run"),
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["agent-reach", "configure", "--from-browser", "chrome"],
    )

    with pytest.raises(SystemExit) as exc:
        cli.main()

    assert exc.value.code == 2


def test_browser_cookie_import_passes_explicit_platform_and_profile(
    monkeypatch, capsys
):
    """The CLI forwards an allowed minimal-cookie platform and exact profile."""
    import agent_reach.config as config_module
    import agent_reach.cookie_extract as cookie_extract

    captured = {}

    def fake_configure(browser, config, **kwargs):
        captured.update(browser=browser, config=config, **kwargs)
        return [("Twitter/X", True, "saved to config.yaml")]

    monkeypatch.setattr(config_module, "Config", _MemoryConfig)
    monkeypatch.setattr(cli, "_configure_logging", lambda _verbose=False: None)
    monkeypatch.setattr(cookie_extract, "configure_from_browser", fake_configure)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "agent-reach",
            "configure",
            "--from-browser",
            "chrome",
            "--platform",
            "xueqiu",
            "--profile",
            "Profile 2",
        ],
    )

    cli.main()

    assert captured["browser"] == "chrome"
    assert captured["platform"] == "xueqiu"
    assert captured["profile"] == "Profile 2"
    assert "Cookies configured" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("platform", "manual_key"),
    [("twitter", "twitter-cookies"), ("xiaohongshu", "xhs-cookies")],
)
def test_browser_cookie_import_rejects_cookie_editor_only_platforms(
    monkeypatch, capsys, platform, manual_key
):
    """Twitter/XHS browser stores are never opened by the automatic importer."""
    import agent_reach.cookie_extract as cookie_extract

    monkeypatch.setattr(cli, "_configure_logging", lambda _verbose=False: None)
    monkeypatch.setattr(
        cookie_extract,
        "configure_from_browser",
        lambda *_args, **_kwargs: pytest.fail("browser cookie reader must not run"),
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "agent-reach",
            "configure",
            "--from-browser",
            "chrome",
            "--platform",
            platform,
        ],
    )

    with pytest.raises(SystemExit) as exc:
        cli.main()

    assert exc.value.code == 2
    assert manual_key in capsys.readouterr().err


def test_install_does_not_implicitly_read_browser_cookies(monkeypatch, tmp_path, capsys):
    """Installing a cookie-backed channel prints an explicit command instead."""
    import agent_reach.config as config_module
    import agent_reach.cookie_extract as cookie_extract

    monkeypatch.setattr(config_module, "Config", _MemoryConfig)
    monkeypatch.setattr(
        cli.os.path,
        "expanduser",
        lambda value: value.replace("~", str(tmp_path)),
    )
    monkeypatch.setattr(cli, "_install_system_deps", lambda: None)
    monkeypatch.setattr(cli, "_install_mcporter", lambda: None)
    monkeypatch.setattr(cli, "_install_twitter_deps", lambda: None)
    monkeypatch.setattr(cli, "_install_skill", lambda: None)
    monkeypatch.setattr(
        "agent_reach.doctor.check_all",
        lambda _config: {},
    )
    monkeypatch.setattr(
        "agent_reach.doctor.format_report",
        lambda _results: "report",
    )
    monkeypatch.setattr(
        cookie_extract,
        "configure_from_browser",
        lambda *_args, **_kwargs: pytest.fail("install must not read browser cookies"),
    )

    cli._cmd_install(
        Namespace(
            env="local",
            proxy="",
            safe=False,
            dry_run=False,
            channels="twitter",
        )
    )

    output = capsys.readouterr().out
    assert "configure twitter-cookies" in output
    assert "Importing cookies from browser" not in output


@pytest.mark.parametrize("sync_legacy", [False, True])
def test_manual_twitter_cookie_legacy_copies_are_opt_in(
    monkeypatch, capsys, sync_legacy
):
    """The source-of-truth config is always written; legacy copies are optional."""
    import shutil

    import agent_reach.config as config_module
    import agent_reach.cookie_extract as cookie_extract

    calls = []
    config = _MemoryConfig()
    monkeypatch.setattr(config_module, "Config", lambda: config)
    monkeypatch.setattr(shutil, "which", lambda _name: None)
    monkeypatch.setattr(
        cookie_extract,
        "_sync_xfetch_session",
        lambda auth, ct0: calls.append(("xfetch", auth, ct0)),
    )
    monkeypatch.setattr(
        cookie_extract,
        "_sync_bird_env",
        lambda auth, ct0: calls.append(("bird", auth, ct0)),
    )

    cli._cmd_configure(
        Namespace(
            from_browser=None,
            key="twitter-cookies",
            value=["auth-value", "ct0-value"],
            sync_legacy_twitter=sync_legacy,
        )
    )

    assert config.get("twitter_auth_token") == "auth-value"
    assert config.get("twitter_ct0") == "ct0-value"
    assert bool(calls) is sync_legacy
    output = capsys.readouterr().out
    assert ("Legacy copies written" in output) is sync_legacy


def test_doctor_never_installs_or_updates_skill(monkeypatch, capsys):
    """A diagnostic command is read-only and must not mutate agent instructions."""
    import agent_reach.config as config_module

    monkeypatch.setattr(config_module, "Config", _MemoryConfig)
    monkeypatch.setattr("agent_reach.doctor.check_all", lambda _config: {})
    monkeypatch.setattr("agent_reach.doctor.format_report", lambda _results: "report")
    monkeypatch.setattr(
        cli,
        "_install_skill",
        lambda *_args, **_kwargs: pytest.fail("doctor must not install skill"),
    )

    cli._cmd_doctor(Namespace(json=False))

    assert "report" in capsys.readouterr().out


def _docker_result(args, returncode=0, stdout="", stderr=""):
    return subprocess.CompletedProcess(args, returncode, stdout, stderr)


def test_xhs_docker_cookie_copy_succeeds_without_local_os_binding_error(
    monkeypatch, capsys
):
    """The Docker branch must be able to unlink its temporary file."""
    calls = []

    def fake_which(name):
        if name == "docker":
            return "/usr/bin/docker"
        return None

    def fake_run(args, **_kwargs):
        calls.append(args)
        if args[1] == "ps":
            return _docker_result(args, stdout="xiaohongshu-mcp\n")
        if args[1:3] == ["exec", "xiaohongshu-mcp"]:
            return _docker_result(args, stdout="/app/data/cookies.json\n")
        return _docker_result(args)

    monkeypatch.setattr("shutil.which", fake_which)
    monkeypatch.setattr(subprocess, "run", fake_run)

    cli._configure_xhs_cookies("web_session=xhs_secret")

    output = capsys.readouterr().out
    assert "Cookies written to xiaohongshu-mcp:/app/data/cookies.json" in output
    assert "cannot access local variable 'os'" not in output
    assert any(call[1] == "cp" for call in calls)


def test_xhs_docker_cookie_copy_always_removes_temporary_file(monkeypatch, capsys):
    """Failed docker cp must not leave a plaintext cookie file behind."""
    copied_from = []

    def fake_which(name):
        if name == "docker":
            return "/usr/bin/docker"
        return None

    def fake_run(args, **_kwargs):
        if args[1] == "ps":
            return _docker_result(args, stdout="xiaohongshu-mcp\n")
        if args[1:3] == ["exec", "xiaohongshu-mcp"]:
            return _docker_result(args, stdout="/app/data/cookies.json\n")
        if args[1] == "cp":
            copied_from.append(args[2])
            return _docker_result(args, returncode=1, stderr="copy failed")
        return _docker_result(args)

    monkeypatch.setattr("shutil.which", fake_which)
    monkeypatch.setattr(subprocess, "run", fake_run)

    cli._configure_xhs_cookies("web_session=xhs_secret")

    assert copied_from
    assert not Path(copied_from[0]).exists()
    assert "Failed to copy cookies: copy failed" in capsys.readouterr().out


def test_system_install_uses_platform_specific_ytdlp_config(
    monkeypatch, tmp_path
):
    """macOS installation writes the same config path that doctor reads."""
    import shutil

    import agent_reach.utils.paths as paths

    monkeypatch.setattr(paths.sys, "platform", "darwin")
    monkeypatch.setattr(paths.Path, "home", classmethod(lambda cls: tmp_path))
    monkeypatch.setattr(
        cli.os.path,
        "expanduser",
        lambda value: str(tmp_path / ".legacy-config")
        if value == "~/.config/yt-dlp"
        else value.replace("~", str(tmp_path)),
    )
    monkeypatch.setattr(
        shutil,
        "which",
        lambda name: f"/usr/bin/{name}" if name in {"gh", "node", "npm"} else None,
    )
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda args, **_kwargs: _docker_result(
            args,
            stdout="/tmp/npm-root\n" if args[1:3] == ["root", "-g"] else "",
        ),
    )

    cli._install_system_deps()

    config_path = (
        tmp_path / "Library" / "Application Support" / "yt-dlp" / "config"
    )
    assert config_path.read_text(encoding="utf-8") == "--js-runtimes node\n"
    assert not (tmp_path / ".legacy-config" / "config").exists()


def test_mcporter_install_adds_exa_to_home_scope(monkeypatch):
    """Installer config remains available across working directories."""
    import shutil

    calls = []

    monkeypatch.setattr(
        shutil,
        "which",
        lambda name: "/usr/bin/mcporter" if name == "mcporter" else None,
    )

    def fake_run(args, **_kwargs):
        calls.append(args)
        if args[:3] == ["mcporter", "config", "list"]:
            return _docker_result(args, stdout='{"servers": []}')
        return _docker_result(args)

    monkeypatch.setattr(subprocess, "run", fake_run)

    cli._install_mcporter()

    assert [
        "mcporter",
        "config",
        "add",
        "exa",
        "https://mcp.exa.ai/mcp",
        "--scope",
        "home",
    ] in calls
