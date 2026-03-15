from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from .config import load_config
from .fred_client import FredClient
from .io_utils import ensure_directories
from .key_manager import read_api_key
from .processing import (
    clean_series,
    generate_features,
    merge_frequency_series,
    store_frequency_outputs,
    transform_series,
)


def pipeline(config_path: str | Path) -> None:
    config = load_config(config_path)

    ensure_directories(
        [
            config.output_paths.raw,
            config.output_paths.processed,
            config.output_paths.masters,
            config.output_paths.features,
        ]
    )

    api_key = read_api_key(config.api_key_file)
    client = FredClient(api_key=api_key)

    for frequency, series_ids in config.frequencies.items():
        raw_series: dict[str, pd.DataFrame] = {}
        processed_frames: list[pd.DataFrame] = []

        for series_id in series_ids:
            raw_df = client.fetch_series(series_id, config.start_date, config.end_date)
            raw_series[series_id] = raw_df
            processed_frames.append(transform_series(clean_series(raw_df)))

        master_df = merge_frequency_series(processed_frames)
        feature_df = generate_features(master_df, config.feature_windows)

        store_frequency_outputs(
            frequency=frequency,
            series_data=raw_series,
            master_df=master_df,
            feature_df=feature_df,
            raw_dir=config.output_paths.raw,
            processed_dir=config.output_paths.processed,
            masters_dir=config.output_paths.masters,
            features_dir=config.output_paths.features,
        )


def run() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Download FRED economic series by frequency, clean + merge into masters, "
            "and generate features."
        )
    )
    parser.add_argument(
        "--config",
        default="config.yaml",
        help="Path to YAML configuration file (default: config.yaml)",
    )
    args = parser.parse_args()

    pipeline(args.config)


if __name__ == "__main__":
    run()
