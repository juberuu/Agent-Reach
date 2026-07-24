# -*- coding: utf-8 -*-
"""Behavior tests for cross-platform path and remediation helpers."""

import subprocess

from agent_reach.utils import paths


def test_posix_ytdlp_fix_is_single_line_executable_and_idempotent(
    monkeypatch, tmp_path
):
    monkeypatch.setattr(paths.sys, "platform", "linux")
    monkeypatch.setattr(paths.Path, "home", classmethod(lambda cls: tmp_path))

    command = paths.render_ytdlp_fix_command()

    assert "\n" not in command
    subprocess.run(["/bin/sh", "-c", command], check=True)
    subprocess.run(["/bin/sh", "-c", command], check=True)

    config = tmp_path / ".config" / "yt-dlp" / "config"
    assert config.read_text(encoding="utf-8") == "--js-runtimes node\n"
