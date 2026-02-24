# -*- coding: utf-8 -*-
"""Tests for the channel system."""

import pytest
from unittest.mock import patch, MagicMock

from agent_eyes.channels import get_channel_for_url, get_channel, get_all_channels
from agent_eyes.channels.base import ReadResult, SearchResult


class TestChannelRouting:
    def test_github_url(self):
        ch = get_channel_for_url("https://github.com/openai/gpt-4")
        assert ch.name == "github"

    def test_twitter_url(self):
        ch = get_channel_for_url("https://x.com/elonmusk/status/123")
        assert ch.name == "twitter"

    def test_youtube_url(self):
        ch = get_channel_for_url("https://youtube.com/watch?v=abc")
        assert ch.name == "youtube"

    def test_reddit_url(self):
        ch = get_channel_for_url("https://reddit.com/r/test")
        assert ch.name == "reddit"

    def test_bilibili_url(self):
        ch = get_channel_for_url("https://bilibili.com/video/BV1xx")
        assert ch.name == "bilibili"

    def test_rss_url(self):
        ch = get_channel_for_url("https://example.com/feed.xml")
        assert ch.name == "rss"

    def test_generic_url_fallback(self):
        ch = get_channel_for_url("https://example.com")
        assert ch.name == "web"

    def test_get_channel_by_name(self):
        ch = get_channel("github")
        assert ch is not None
        assert ch.name == "github"

    def test_all_channels_registered(self):
        channels = get_all_channels()
        names = [ch.name for ch in channels]
        assert "web" in names
        assert "github" in names
        assert "twitter" in names


class TestReadResult:
    def test_to_dict(self):
        r = ReadResult(title="Test", content="Body", url="https://example.com", platform="web")
        d = r.to_dict()
        assert d["title"] == "Test"
        assert d["content"] == "Body"
        assert d["platform"] == "web"

    def test_to_dict_optional_fields(self):
        r = ReadResult(title="T", content="C", url="u", author="A", date="2025-01-01")
        d = r.to_dict()
        assert d["author"] == "A"
        assert d["date"] == "2025-01-01"


class TestSearchResult:
    def test_to_dict(self):
        r = SearchResult(title="Test", url="https://example.com", snippet="A snippet")
        d = r.to_dict()
        assert d["title"] == "Test"
        assert d["snippet"] == "A snippet"


class TestGitHubChannel:
    @patch("agent_eyes.channels.github.requests.get")
    @pytest.mark.asyncio
    async def test_search(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "items": [{"full_name": "test/repo", "html_url": "https://github.com/test/repo",
                       "description": "A test", "stargazers_count": 100, "forks_count": 10,
                       "language": "Python", "updated_at": "2025-01-01"}]
        }
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        ch = get_channel("github")
        results = await ch.search("test query")
        assert len(results) == 1
        assert results[0].title == "test/repo"


class TestExaSearch:
    @patch("agent_eyes.channels.exa_search.requests.post")
    @pytest.mark.asyncio
    async def test_search(self, mock_post):
        from agent_eyes.config import Config
        config = Config(config_path="/tmp/test-exa-config.yaml")
        config.set("exa_api_key", "test-key")

        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "results": [{"title": "Result", "url": "https://example.com",
                         "text": "snippet", "publishedDate": "", "score": 0.9}]
        }
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        ch = get_channel("exa_search")
        results = await ch.search("test", config=config)
        assert len(results) == 1
        assert results[0].title == "Result"
