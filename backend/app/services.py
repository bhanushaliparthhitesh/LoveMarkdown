from __future__ import annotations

import re
from pathlib import Path


def optimize_markdown(markdown: str) -> str:
    """Normalize noisy spacing while preserving markdown structure."""
    lines = [line.rstrip() for line in markdown.replace("\r\n", "\n").split("\n")]
    collapsed = []
    blank_count = 0

    for line in lines:
        if line.strip():
            blank_count = 0
            collapsed.append(line)
        else:
            blank_count += 1
            if blank_count <= 1:
                collapsed.append("")

    return "\n".join(collapsed).strip() + "\n"


def estimate_tokens(text: str) -> int:
    """Estimate token count with tiktoken when available."""
    try:
        import tiktoken  # type: ignore

        encoder = tiktoken.get_encoding("cl100k_base")
        return len(encoder.encode(text))
    except Exception:
        words = len(re.findall(r"\S+", text))
        return max(1, int(words * 1.3)) if text.strip() else 0


def convert_file_to_markdown(path: Path) -> str:
    from markitdown import MarkItDown

    parser = MarkItDown()
    result = parser.convert(str(path))
    return result.text_content
