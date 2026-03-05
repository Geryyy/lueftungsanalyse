"""Analysemodule für Lüftungswahrscheinlichkeit."""

import pandas as pd

import config
from humidity import absolute_humidity, cellar_absolute_humidity


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    """Fügt berechnete Spalten hinzu und filtert auf Sommermonate."""
    df = df.copy()
    df["month"] = df["timestamp"].dt.month
    df["hour"] = df["timestamp"].dt.hour

    df = df[df["month"].isin(config.SUMMER_MONTHS)].copy()

    df["ah_outside"] = absolute_humidity(df["temperature"], df["relative_humidity"])
    cellar_ah = cellar_absolute_humidity()
    df["ah_cellar"] = cellar_ah
    df["ventilation_possible"] = df["ah_outside"] < cellar_ah

    return df


def hourly_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregiert Stundenmittelwerte und Lüftungswahrscheinlichkeit.

    Returns
    -------
    DataFrame mit Index = Stunde (0–23) und Spalten:
        temperature, relative_humidity, ah_outside, ventilation_prob
    """
    grouped = df.groupby("hour").agg(
        temperature=("temperature", "mean"),
        relative_humidity=("relative_humidity", "mean"),
        ah_outside=("ah_outside", "mean"),
        ventilation_prob=("ventilation_possible", "mean"),
    )
    return grouped


def summary(df: pd.DataFrame) -> dict:
    """Berechnet zusammenfassende Statistiken."""
    cellar_ah = cellar_absolute_humidity()
    avg_hours_per_day = df.groupby(df["timestamp"].dt.date)["ventilation_possible"].sum().mean()

    vent_by_hour = df.groupby("hour")["ventilation_possible"].mean()
    best_hour = int(vent_by_hour.idxmax())
    worst_hour = int(vent_by_hour.idxmin())

    return {
        "cellar_ah_g_m3": round(cellar_ah, 2),
        "avg_ventilation_hours_per_day": round(float(avg_hours_per_day), 1),
        "best_hour": best_hour,
        "best_hour_prob": round(float(vent_by_hour[best_hour]) * 100, 1),
        "worst_hour": worst_hour,
        "worst_hour_prob": round(float(vent_by_hour[worst_hour]) * 100, 1),
    }
