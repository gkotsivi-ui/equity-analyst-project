#!/usr/bin/env python3
"""Save your API keys into .env without editing the file: paste each key at the prompt."""

from __future__ import annotations

from pathlib import Path

ENV = Path(".env")
KEYS = [
    ("API_KEY", "Anthropic API key (it starts with sk-ant-)", "sk-ant-"),
    ("FINANCIAL_DATASETS_API_KEY", "class financialdatasets.ai key, or press Enter to skip", ""),
]


def save(name: str, value: str) -> None:
    """Replace or add one NAME=value line, reading .env fresh so other lines stay as they are."""
    lines = ENV.read_text(encoding="utf-8-sig").splitlines() if ENV.exists() else []
    found = [i for i, line in enumerate(lines) if line.strip().startswith(f"{name}=")]
    if found:
        lines[found[0]] = f"{name}={value}"
    else:
        lines.append(f"{name}={value}")
    ENV.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    for name, prompt, prefix in KEYS:
        # Visible on purpose: a hidden prompt looks as if typing does not work.
        value = input(f"\nPaste your {prompt}, then press Enter:\n> ").strip()
        if not value:
            print(f"  {name}: skipped")
            continue
        if prefix and not value.startswith(prefix):
            print(f"  {name}: not saved, because it does not start with {prefix}")
            continue
        save(name, value)
        print(f"  {name}: saved ({value[:4]}...)")
    print("\nDone. .env is listed in .gitignore, so these keys never reach GitHub. You can close this tab.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
