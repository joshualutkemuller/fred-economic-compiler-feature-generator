from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import requests


@dataclass
class FredClient:
    api_key: str
    base_url: str = "https://api.stlouisfed.org/fred/series/observations"

    def fetch_series(
        self,
        series_id: str,
        start_date: str,
        end_date: str | None = None,
    ) -> pd.DataFrame:
        params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json",
            "observation_start": start_date,
        }
        if end_date:
            params["observation_end"] = end_date

        response = requests.get(self.base_url, params=params, timeout=60)
        response.raise_for_status()
        payload = response.json()

        observations = payload.get("observations", [])
        frame = pd.DataFrame(observations)
        if frame.empty:
            return pd.DataFrame(columns=[series_id], dtype="float64")

        frame = frame[["date", "value"]].copy()
        frame["date"] = pd.to_datetime(frame["date"], utc=False)
        frame[series_id] = pd.to_numeric(frame["value"], errors="coerce")
        frame = frame.drop(columns=["value"]).set_index("date").sort_index()
        return frame
