#!/usr/bin/env python3
"""Save your API keys into .env without editing the file: paste each key at the prompt."""

from __future__ import annotations

from getpass import getpass
from pathlib import Path

ENV = Path(".env")
KEYS = [
    ("API_KEY", "Anthropic API key (it starts with sk-ant-)", "sk-ant-"),
    ("FINANCIAL_DATASETS_API_KEY", "class financialdatasets.ai key, or press Enter to skip", ""),
]


def main() -> int:
    lines = ENV.read_text(encoding="utf-8-sig").splitlines() if ENV.exists() else []
    for name, prompt, prefix in KEYS:
        value = getpass(f"Paste your {prompt}, then press Enter (the key stays hidden): ").strip()
        if not value:
            print(f"  {name}: skipped")
            continue
        if prefix and not value.startswith(prefix):
            print(f"  {name}: not saved, because it does not start with {prefix}")
            continue
        entry = f"{name}={value}"
        found = [i for i, line in enumerate(lines) if line.strip().startswith(f"{name}=")]
        if found:
            lines[found[0]] = entry
        else:
            lines.append(entry)
        print(f"  {name}: saved ({value[:4]}...)")
    ENV.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Done. .env is listed in .gitignore, so these keys never reach GitHub.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
