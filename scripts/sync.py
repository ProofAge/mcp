#!/usr/bin/env python3
"""Copy the MCP tool list from the docs checkout into tools.json.

Usage: python3 scripts/sync.py [path/to/facts.json]
Default path: ../proofage-docs/data/facts.json
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "proofage-docs" / "data" / "facts.json"
    tools = json.loads(src.read_text(encoding="utf-8"))["mcp_tools"]
    (ROOT / "tools.json").write_text(
        json.dumps(tools, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Wrote tools.json: {len(tools)} tools from {src}")


if __name__ == "__main__":
    main()
