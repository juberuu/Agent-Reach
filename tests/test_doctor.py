# -*- coding: utf-8 -*-
"""Tests for doctor module."""

import pytest
from agent_eyes.config import Config
from agent_eyes.doctor import check_all, format_report


@pytest.fixture
def tmp_config(tmp_path):
    return Config(config_path=tmp_path / "config.yaml")


class TestDoctor:
    def test_zero_config_channels_ok(self, tmp_config):
        results = check_all(tmp_config)
        assert results["web"]["status"] == "ok"
        assert results["github"]["status"] == "ok"
        assert results["bilibili"]["status"] in ("ok", "warn")  # warn on servers
        assert results["rss"]["status"] == "ok"

    def test_exa_off_without_key(self, tmp_config):
        results = check_all(tmp_config)
        assert results["exa_search"]["status"] == "off"

    def test_exa_on_with_key(self, tmp_config):
        tmp_config.set("exa_api_key", "test-key")
        results = check_all(tmp_config)
        assert results["exa_search"]["status"] == "ok"

    def test_format_report(self, tmp_config):
        results = check_all(tmp_config)
        report = format_report(results)
        assert "Agent Eyes" in report
        assert "✅" in report
        assert "channels active" in report
