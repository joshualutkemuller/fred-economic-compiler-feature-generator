from __future__ import annotations

from pathlib import Path

import pandas as pd

from .io_utils import write_dataframe


def clean_series(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    cleaned = df.copy()
    cleaned = cleaned[~cleaned.index.duplicated(keep="last")]
    cleaned = cleaned.sort_index()
    cleaned = cleaned.replace([float("inf"), float("-inf")], pd.NA)
    return cleaned


def transform_series(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    transformed = df.copy()
    transformed = transformed.interpolate(method="time", limit_direction="both")
    transformed = transformed.ffill().bfill()
    return transformed


def merge_frequency_series(series_frames: list[pd.DataFrame]) -> pd.DataFrame:
    if not series_frames:
        return pd.DataFrame()

    merged = pd.concat(series_frames, axis=1, join="outer").sort_index()
    merged.index.name = "date"
    return merged


def generate_features(master_df: pd.DataFrame, windows: list[int]) -> pd.DataFrame:
    if master_df.empty:
        return master_df

    feature_df = master_df.copy()
    numeric_cols = feature_df.select_dtypes(include=["number"]).columns

    for col in numeric_cols:
        feature_df[f"{col}_pct_change"] = feature_df[col].pct_change()
        for window in windows:
            feature_df[f"{col}_ma_{window}"] = feature_df[col].rolling(window).mean()
            feature_df[f"{col}_std_{window}"] = feature_df[col].rolling(window).std()

    return feature_df


def store_frequency_outputs(
    frequency: str,
    series_data: dict[str, pd.DataFrame],
    master_df: pd.DataFrame,
    feature_df: pd.DataFrame,
    raw_dir: Path,
    processed_dir: Path,
    masters_dir: Path,
    features_dir: Path,
) -> None:
    for series_id, raw_df in series_data.items():
        write_dataframe(raw_df, raw_dir / frequency / f"{series_id}.csv")
        cleaned = transform_series(clean_series(raw_df))
        write_dataframe(cleaned, processed_dir / frequency / f"{series_id}.csv")

    write_dataframe(master_df, masters_dir / f"master_{frequency}.csv")
    write_dataframe(feature_df, features_dir / f"features_{frequency}.csv")
