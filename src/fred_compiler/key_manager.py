from __future__ import annotations

from pathlib import Path


def read_api_key(key_file: str | Path) -> str:
    key_path = Path(key_file)
    if not key_path.exists():
        raise FileNotFoundError(f"API key file not found: {key_path}")

    key = key_path.read_text(encoding="utf-8").strip()
    if not key:
        raise ValueError(f"API key file is empty: {key_path}")
    return key
