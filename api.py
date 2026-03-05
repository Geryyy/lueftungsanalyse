"""Geosphere API – klima-v2-1h Datenabruf.

Die API liefert maximal ~1 Jahr pro Request, daher wird der Zeitraum
automatisch in Jahresscheiben aufgeteilt und zusammengeführt.
"""

import time
from datetime import date, timedelta

import pandas as pd
import requests

BASE_URL = "https://dataset.api.hub.geosphere.at/v1/station/historical/klima-v2-1h"


def _fetch_chunk(station: int, start: str, end: str) -> pd.DataFrame:
    """Lädt einen einzelnen Zeitabschnitt und gibt einen DataFrame zurück."""
    params = {
        "station_ids": station,
        "parameters": "TL,RF",
        "start": start,
        "end": end,
    }
    resp = requests.get(BASE_URL, params=params, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    timestamps = data["timestamps"]
    feature = data["features"][0]
    props = feature["properties"]["parameters"]

    tl_values = props["tl"]["data"]
    rf_values = props["rf"]["data"]

    df = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(timestamps, utc=True),
            "temperature": tl_values,
            "relative_humidity": rf_values,
        }
    )
    df["timestamp"] = df["timestamp"].dt.tz_convert("Europe/Vienna")
    return df


def load_weather_data(station: int, start_date: str, end_date: str) -> pd.DataFrame:
    """Lädt stündliche Wetterdaten (TL, RF) für eine Station.

    Der Zeitraum wird automatisch in Jahresscheiben aufgeteilt.

    Parameters
    ----------
    station    : Geosphere Station-ID (int)
    start_date : "YYYY-MM-DD"
    end_date   : "YYYY-MM-DD"

    Returns
    -------
    DataFrame mit Spalten: timestamp, temperature, relative_humidity
    """
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)

    chunks = []
    current = start
    while current <= end:
        chunk_end = min(date(current.year, 12, 31), end)
        print(f"  Lade {current} – {chunk_end} …")
        try:
            chunk = _fetch_chunk(
                station,
                current.isoformat(),
                chunk_end.isoformat(),
            )
            chunks.append(chunk)
        except requests.HTTPError as exc:
            print(f"  Warnung: HTTP-Fehler für {current}–{chunk_end}: {exc}")
        time.sleep(0.5)          # API nicht überlasten
        current = date(chunk_end.year + 1, 1, 1)

    if not chunks:
        raise RuntimeError("Keine Daten empfangen.")

    df = pd.concat(chunks, ignore_index=True)
    df = df.dropna(subset=["temperature", "relative_humidity"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df
