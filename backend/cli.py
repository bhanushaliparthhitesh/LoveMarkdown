from __future__ import annotations

import argparse
from pathlib import Path

from app.services import convert_file_to_markdown, estimate_tokens, optimize_markdown


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert documents to AI-ready Markdown")
    parser.add_argument("input", type=Path, help="Path to source document")
    parser.add_argument("-o", "--output", type=Path, help="Output markdown file path")
    args = parser.parse_args()

    markdown = convert_file_to_markdown(args.input)
    optimized = optimize_markdown(markdown)

    if args.output:
        args.output.write_text(optimized, encoding="utf-8")
        print(f"Saved optimized markdown to {args.output}")

    print(f"Estimated tokens: {estimate_tokens(optimized)}")


if __name__ == "__main__":
    main()
