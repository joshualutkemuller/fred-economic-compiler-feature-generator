from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass
class PathsConfig:
    raw: Path
    processed: Path
    masters: Path
    features: Path


@dataclass
class AppConfig:
    api_key_file: Path
    start_date: str
    end_date: str | None
    frequencies: dict[str, list[str]]
    output_paths: PathsConfig
    feature_windows: list[int]


def load_config(config_path: str | Path) -> AppConfig:
    config_path = Path(config_path)
    with config_path.open("r", encoding="utf-8") as handle:
        data: dict[str, Any] = yaml.safe_load(handle)

    paths = data.get("output_paths", {})
    return AppConfig(
        api_key_file=Path(data["api_key_file"]),
        start_date=data.get("start_date", "1900-01-01"),
        end_date=data.get("end_date"),
        frequencies=data.get("frequencies", {}),
        output_paths=PathsConfig(
            raw=Path(paths.get("raw", "output/raw")),
            processed=Path(paths.get("processed", "output/processed")),
            masters=Path(paths.get("masters", "output/masters")),
            features=Path(paths.get("features", "output/features")),
        ),
        feature_windows=data.get("feature_windows", [4, 12]),
    )
