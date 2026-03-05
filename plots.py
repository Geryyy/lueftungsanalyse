"""Visualisierungen für die Lüftungsanalyse."""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import date

import config
from humidity import absolute_humidity, cellar_absolute_humidity

sns.set_theme(style="whitegrid")
HOURS = list(range(24))


def _save_or_show(fig, filename: str | None):
    if filename:
        fig.savefig(filename, dpi=150, bbox_inches="tight")
        print(f"  Gespeichert: {filename}")
    else:
        plt.show()
    plt.close(fig)


def plot_temperature(hourly: pd.DataFrame, filename: str | None = None):
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(hourly.index, hourly["temperature"], marker="o", linewidth=2)
    ax.set_xlabel("Stunde")
    ax.set_ylabel("Temperatur (°C)")
    ax.set_title("Tagesverlauf Temperatur – Sommermonate (Jun–Aug)")
    ax.xaxis.set_major_locator(mticker.MultipleLocator(2))
    ax.set_xlim(0, 23)
    _save_or_show(fig, filename)


def plot_relative_humidity(hourly: pd.DataFrame, filename: str | None = None):
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(hourly.index, hourly["relative_humidity"], marker="o", color="steelblue", linewidth=2)
    ax.set_xlabel("Stunde")
    ax.set_ylabel("Relative Feuchte (%)")
    ax.set_title("Tagesverlauf Relative Feuchte – Sommermonate")
    ax.xaxis.set_major_locator(mticker.MultipleLocator(2))
    ax.set_xlim(0, 23)
    _save_or_show(fig, filename)


def plot_absolute_humidity(hourly: pd.DataFrame, filename: str | None = None):
    cellar_ah = cellar_absolute_humidity()
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(hourly.index, hourly["ah_outside"], marker="o", color="darkorange", linewidth=2,
            label="Außenluft")
    ax.axhline(cellar_ah, color="green", linestyle="--", linewidth=1.5,
               label=f"Keller ({config.CELLAR_TEMP} °C / {config.CELLAR_RH} % RH ≈ {cellar_ah:.1f} g/m³)")
    ax.set_xlabel("Stunde")
    ax.set_ylabel("Absolute Feuchte (g/m³)")
    ax.set_title("Tagesverlauf Absolute Feuchte – Sommermonate")
    ax.xaxis.set_major_locator(mticker.MultipleLocator(2))
    ax.set_xlim(0, 23)
    ax.legend()
    _save_or_show(fig, filename)


def plot_absolute_humidity_variance(df: pd.DataFrame, filename: str | None = None):
    """Absolute Feuchte mit Mittelwert, ±1σ-Band und Perzentilen (10/25/75/90)."""
    cellar_ah = cellar_absolute_humidity()

    stats = df.groupby("hour")["ah_outside"].agg(
        mean="mean",
        std="std",
        p10=lambda x: x.quantile(0.10),
        p25=lambda x: x.quantile(0.25),
        p75=lambda x: x.quantile(0.75),
        p90=lambda x: x.quantile(0.90),
    )
    hours = stats.index

    fig, ax = plt.subplots(figsize=(10, 5))

    # 10–90 % Bereich
    ax.fill_between(hours, stats["p10"], stats["p90"],
                    alpha=0.15, color="darkorange", label="10.–90. Perzentile")
    # 25–75 % Bereich (IQR)
    ax.fill_between(hours, stats["p25"], stats["p75"],
                    alpha=0.30, color="darkorange", label="25.–75. Perzentile (IQR)")
    # Mittelwert ± σ
    ax.fill_between(hours, stats["mean"] - stats["std"], stats["mean"] + stats["std"],
                    alpha=0.20, color="red", label="Mittelwert ± 1σ")
    # Mittelwert
    ax.plot(hours, stats["mean"], color="darkorange", linewidth=2.5, marker="o", label="Mittelwert")

    # Keller-Referenzlinie
    ax.axhline(cellar_ah, color="green", linestyle="--", linewidth=1.8,
               label=f"Keller-AH ({config.CELLAR_TEMP} °C / {config.CELLAR_RH} % RH = {cellar_ah:.1f} g/m³)")

    ax.set_xlabel("Stunde")
    ax.set_ylabel("Absolute Feuchte (g/m³)")
    ax.set_title("Absolute Feuchte Außenluft – Tagesverlauf mit Streuung (Sommermonate)")
    ax.xaxis.set_major_locator(mticker.MultipleLocator(2))
    ax.set_xlim(0, 23)
    ax.legend(loc="upper left", fontsize=8)
    _save_or_show(fig, filename)


def plot_ventilation_probability(hourly: pd.DataFrame, filename: str | None = None):
    fig, ax = plt.subplots(figsize=(9, 4))
    bars = ax.bar(hourly.index, hourly["ventilation_prob"] * 100, color="mediumseagreen", edgecolor="white")
    ax.set_xlabel("Stunde")
    ax.set_ylabel("Wahrscheinlichkeit (%)")
    ax.set_title("Wahrscheinlichkeit für sinnvolles Lüften pro Stunde")
    ax.set_ylim(0, 100)
    ax.xaxis.set_major_locator(mticker.MultipleLocator(2))
    ax.set_xlim(-0.5, 23.5)
    _save_or_show(fig, filename)


def plot_daily_absolute_humidity(raw_df: pd.DataFrame, filename: str | None = None):
    """Mittlere absolute Feuchte pro Kalendertag (Apr–Sep), gemittelt über alle Jahre.

    raw_df : ungefilteter DataFrame aus load_weather_data (alle Monate/Jahre)
    """
    cellar_ah = cellar_absolute_humidity()
    months = [4, 5, 6, 7, 8, 9]
    month_labels = {4: "Apr", 5: "Mai", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep"}

    df = raw_df.copy()
    df["month"] = df["timestamp"].dt.month
    df["day"] = df["timestamp"].dt.day
    df = df[df["month"].isin(months)].copy()
    df["ah"] = absolute_humidity(df["temperature"], df["relative_humidity"])

    # Tagesmittel pro Jahr und Kalendertag
    df["year"] = df["timestamp"].dt.year
    daily = df.groupby(["year", "month", "day"])["ah"].mean().reset_index()

    # Statistik über alle Jahre für jeden Kalendertag
    stats = daily.groupby(["month", "day"])["ah"].agg(
        mean="mean",
        std="std",
        p10=lambda x: x.quantile(0.10),
        p25=lambda x: x.quantile(0.25),
        p75=lambda x: x.quantile(0.75),
        p90=lambda x: x.quantile(0.90),
    ).reset_index()

    # x-Achse: fortlaufender Index (Kalendertag Apr–Sep eines Nicht-Schaltjahres)
    ref_year = 2001
    stats["date"] = pd.to_datetime(
        stats[["day", "month"]].assign(year=ref_year).rename(
            columns={"day": "day", "month": "month"}
        )[["year", "month", "day"]]
    )
    stats = stats.sort_values("date").reset_index(drop=True)
    x = stats["date"]

    fig, ax = plt.subplots(figsize=(13, 5))

    ax.fill_between(x, stats["p10"], stats["p90"],
                    alpha=0.15, color="darkorange", label="10.–90. Perzentile")
    ax.fill_between(x, stats["p25"], stats["p75"],
                    alpha=0.30, color="darkorange", label="25.–75. Perzentile (IQR)")
    ax.fill_between(x, stats["mean"] - stats["std"], stats["mean"] + stats["std"],
                    alpha=0.20, color="red", label="Mittelwert ± 1σ")
    ax.plot(x, stats["mean"], color="darkorange", linewidth=2, label="Mittelwert")

    cellar_rh_levels = [70, 80, 90]
    cellar_colors = ["green", "goldenrod", "red"]
    for rh, color in zip(cellar_rh_levels, cellar_colors):
        ah = absolute_humidity(config.CELLAR_TEMP, rh)
        ax.axhline(ah, color=color, linestyle="--", linewidth=1.5,
                   label=f"Keller {config.CELLAR_TEMP} °C / {rh} % RH = {ah:.1f} g/m³")

    # Monatsmarkierungen
    for month in months:
        boundary = pd.Timestamp(year=ref_year, month=month, day=1)
        ax.axvline(boundary, color="gray", linewidth=0.7, linestyle=":")
        ax.text(boundary, ax.get_ylim()[1] if ax.get_ylim()[1] > 0 else 20,
                month_labels[month], fontsize=8, color="gray", ha="left", va="top")

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.set_xlabel("Kalendertag")
    ax.set_ylabel("Absolute Feuchte (g/m³)")
    ax.set_title(f"Absolute Feuchte – Tagesverlauf Apr–Sep "
                 f"(Tagesmittel, gemittelt {raw_df['timestamp'].dt.year.min()}–"
                 f"{raw_df['timestamp'].dt.year.max()})")
    ax.legend(loc="upper left", fontsize=8)
    ax.set_xlim(x.iloc[0], x.iloc[-1])
    _save_or_show(fig, filename)


def plot_heatmap(df: pd.DataFrame, filename: str | None = None):
    """Heatmap: Lüftungswahrscheinlichkeit nach Stunde × Monat."""
    pivot = df.groupby(["month", "hour"])["ventilation_possible"].mean().unstack("hour") * 100
    pivot.index = pivot.index.map({6: "Jun", 7: "Jul", 8: "Aug"})

    fig, ax = plt.subplots(figsize=(12, 4))
    sns.heatmap(pivot, ax=ax, cmap="RdYlGn", vmin=0, vmax=100,
                linewidths=0.3, annot=True, fmt=".0f",
                cbar_kws={"label": "Wahrscheinlichkeit (%)"})
    ax.set_xlabel("Stunde")
    ax.set_ylabel("Monat")
    ax.set_title("Lüftungswahrscheinlichkeit (%) – Stunde × Monat")
    _save_or_show(fig, filename)
