# -*- coding: utf-8 -*-
"""
Channel base class — the universal interface for all platforms.

Every channel (YouTube, Twitter, GitHub, etc.) implements this interface.
The backend tool can be swapped anytime without changing anything else.

Example:
    class YouTubeChannel(Channel):
        name = "youtube"
        backends = ["yt-dlp"]  # current backend, can be swapped
        
        async def read(self, url, config):
            # Just call yt-dlp, return standardized dict
            ...
"""

import shutil
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class ReadResult:
    """Standardized read result. Every channel returns this."""
    title: str
    content: str
    url: str
    author: str = ""
    date: str = ""
    platform: str = ""
    extra: dict = None

    def __post_init__(self):
        self.extra = self.extra or {}

    def to_dict(self) -> dict:
        d = {
            "title": self.title,
            "content": self.content,
            "url": self.url,
            "platform": self.platform,
        }
        if self.author:
            d["author"] = self.author
        if self.date:
            d["date"] = self.date
        if self.extra:
            d["extra"] = self.extra
        return d


@dataclass
class SearchResult:
    """Standardized search result."""
    title: str
    url: str
    snippet: str = ""
    author: str = ""
    date: str = ""
    score: float = 0
    extra: dict = None

    def __post_init__(self):
        self.extra = self.extra or {}

    def to_dict(self) -> dict:
        d = {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
        }
        if self.author:
            d["author"] = self.author
        if self.date:
            d["date"] = self.date
        if self.extra:
            d["extra"] = self.extra
        return d


class Channel(ABC):
    """
    Base class for all channels.
    
    Subclasses just need to implement:
    - read(url, config) → ReadResult
    - can_handle(url) → bool
    - check(config) → (status, message)
    
    Optionally:
    - search(query, config, **kwargs) → list[SearchResult]
    """

    name: str = ""                    # e.g. "youtube"
    description: str = ""             # e.g. "YouTube video transcripts"
    backends: List[str] = []          # e.g. ["yt-dlp"] — what external tool is used
    requires_config: List[str] = []   # e.g. ["reddit_proxy"]
    requires_tools: List[str] = []    # e.g. ["yt-dlp"]
    tier: int = 0                     # 0=zero-config, 1=needs free key, 2=needs setup

    @abstractmethod
    async def read(self, url: str, config=None) -> ReadResult:
        """Read content from a URL. Must return ReadResult."""
        ...

    @abstractmethod
    def can_handle(self, url: str) -> bool:
        """Check if this channel can handle this URL."""
        ...

    def check(self, config=None) -> Tuple[str, str]:
        """
        Check if this channel is available.
        Returns (status, message) where status is 'ok'/'warn'/'off'/'error'.
        """
        # Check required tools
        for tool in self.requires_tools:
            if not shutil.which(tool):
                return "off", f"需要安装：pip install {tool}"

        # Check required config
        for key in self.requires_config:
            if config and not config.get(key):
                return "off", f"需要配置 {key}，运行 agent-reach setup"

        return "ok", f"{'、'.join(self.backends) if self.backends else '内置'}"

    async def search(self, query: str, config=None, **kwargs) -> List[SearchResult]:
        """Search this platform. Override if supported."""
        raise NotImplementedError(f"{self.name} does not support search")

    def can_search(self) -> bool:
        """Whether this channel supports search."""
        try:
            # Check if search is overridden
            return type(self).search is not Channel.search
        except:
            return False
