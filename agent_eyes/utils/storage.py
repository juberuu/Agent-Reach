# -*- coding: utf-8 -*-
"""
Storage utilities — save content to JSON inbox and optional Markdown file.

Implements the "atomic archiving" from the tweet:
- unified_inbox.json (for AI/programmatic use)
- markdown file (for human reading, e.g. Obsidian)
"""

import json
import os
from datetime import datetime
from pathlib import Path
from loguru import logger

from agent_eyes.schema import UnifiedContent


def save_to_json(item: UnifiedContent, filepath: str = "unified_inbox.json"):
    """Append content to JSON inbox file."""
    path = Path(filepath)
    data = []

    if path.exists():
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            data = []

    data.append(item.to_dict())

    # Keep last 500 entries to prevent unbounded growth
    data = data[-500:]

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    logger.info(f"Saved to JSON: {path}")


def save_to_markdown(item: UnifiedContent, filepath: str = None):
    """
    Append content to a Markdown file (e.g. Obsidian vault).

    Supports two output modes:
    - OUTPUT_DIR: Write to {OUTPUT_DIR}/content_hub.md
    - OBSIDIAN_VAULT: Write to {OBSIDIAN_VAULT}/01-收集箱/x-reader-inbox.md

    If neither is set, skips markdown output.
    """
    if not filepath:
        # Priority 1: Obsidian vault
        vault_path = os.getenv("OBSIDIAN_VAULT", "")
        if vault_path:
            filepath = os.path.join(vault_path, "01-收集箱", "x-reader-inbox.md")
        else:
            # Priority 2: generic output dir
            output_dir = os.getenv("OUTPUT_DIR", "")
            if not output_dir:
                return
            filepath = os.path.join(output_dir, "content_hub.md")

    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    emoji = {
        "telegram": "📢", "rss": "📰", "bilibili": "🎬",
        "xhs": "📕", "twitter": "🐦", "wechat": "💬",
        "youtube": "▶️", "manual": "✏️",
    }.get(item.source_type.value, "📄")

    with open(path, 'a', encoding='utf-8') as f:
        f.write(f"\n## {emoji} {item.title}\n")
        f.write(f"- Source: {item.source_name} ({item.source_type.value})\n")
        f.write(f"- URL: {item.url}\n")
        f.write(f"- Fetched: {item.fetched_at[:16]}\n\n")
        f.write(f"{item.content[:2000]}\n")
        f.write("\n---\n")

    logger.info(f"Saved to Markdown: {path}")


def save_content(item: UnifiedContent, json_path: str = None, md_path: str = None):
    """Save content to both JSON and Markdown."""
    inbox_file = json_path or os.getenv("INBOX_FILE", "unified_inbox.json")
    save_to_json(item, inbox_file)
    save_to_markdown(item, md_path)
