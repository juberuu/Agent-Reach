# -*- coding: utf-8 -*-
"""YouTube — via yt-dlp (free, pip install yt-dlp).

Backend: yt-dlp (https://github.com/yt-dlp/yt-dlp)
Swap to: any YouTube subtitle extractor
"""

import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from .base import Channel, ReadResult


class YouTubeChannel(Channel):
    name = "youtube"
    description = "YouTube 视频字幕"
    backends = ["yt-dlp"]
    requires_tools = ["yt-dlp"]
    tier = 0

    def can_handle(self, url: str) -> bool:
        domain = urlparse(url).netloc.lower()
        return "youtube.com" in domain or "youtu.be" in domain

    async def read(self, url: str, config=None) -> ReadResult:
        if not shutil.which("yt-dlp"):
            raise RuntimeError("yt-dlp not installed. Install: pip install yt-dlp")

        with tempfile.TemporaryDirectory() as tmpdir:
            # Get video info
            info = self._get_info(url)
            title = info.get("title", url)
            author = info.get("uploader", "")

            # Try to get subtitles
            transcript = self._get_subtitles(url, tmpdir)

            if not transcript:
                transcript = f"[Video: {title}]\n[No subtitles available. Use Groq Whisper for transcription.]"

            return ReadResult(
                title=title,
                content=transcript,
                url=url,
                author=author,
                platform="youtube",
                extra={
                    "duration": info.get("duration"),
                    "view_count": info.get("view_count"),
                    "upload_date": info.get("upload_date"),
                },
            )

    def _get_info(self, url: str) -> dict:
        try:
            result = subprocess.run(
                ["yt-dlp", "--dump-json", "--no-download", url],
                capture_output=True, text=True, timeout=30,
            )
            if result.returncode == 0:
                return json.loads(result.stdout)
        except (subprocess.TimeoutExpired, json.JSONDecodeError):
            pass
        return {}

    def _get_subtitles(self, url: str, tmpdir: str) -> str:
        """Extract subtitles using yt-dlp."""
        try:
            subprocess.run(
                ["yt-dlp", "--write-auto-sub", "--write-sub",
                 "--sub-lang", "en,zh-Hans,zh",
                 "--skip-download", "--sub-format", "vtt",
                 "-o", f"{tmpdir}/%(id)s.%(ext)s", url],
                capture_output=True, text=True, timeout=30,
            )

            # Find and read subtitle file
            for f in Path(tmpdir).glob("*.vtt"):
                text = f.read_text(errors="replace")
                # Strip VTT headers and timestamps
                lines = []
                for line in text.split("\n"):
                    line = line.strip()
                    if not line or line.startswith("WEBVTT") or "-->" in line or line.isdigit():
                        continue
                    if line not in lines[-1:]:  # deduplicate
                        lines.append(line)
                return "\n".join(lines)
        except subprocess.TimeoutExpired:
            pass
        return ""
