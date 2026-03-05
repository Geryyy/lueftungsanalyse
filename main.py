"""Kellerlüftungsanalyse – Hauptprogramm.

Workflow:
1. Wetterdaten über Geosphere API laden (oder Cache verwenden)
2. Absolute Feuchte berechnen, Sommermonate filtern
3. Kellerreferenz berechnen
4. Stündliche Statistiken und Zusammenfassung ausgeben
5. Plots erzeugen
"""

import os
import pickle

import config
import analysis
import plots
from api import load_weather_data

CACHE_FILE = "weather_cache.pkl"
OUTPUT_DIR = "output"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # --- Daten laden (mit Cache) ---
    if os.path.exists(CACHE_FILE):
        print("Verwende gecachte Wetterdaten …")
        with open(CACHE_FILE, "rb") as f:
            raw_df = pickle.load(f)
    else:
        print(f"Lade Wetterdaten für Station {config.STATION_ID} "
              f"({config.START_DATE} – {config.END_DATE}) …")
        raw_df = load_weather_data(config.STATION_ID, config.START_DATE, config.END_DATE)
        with open(CACHE_FILE, "wb") as f:
            pickle.dump(raw_df, f)
        print(f"  {len(raw_df):,} Datenpunkte geladen und gecacht.")

    # --- Analyse ---
    df = analysis.prepare(raw_df)
    hourly = analysis.hourly_stats(df)
    stats = analysis.summary(df)

    # --- Ausgabe ---
    print("\n=== Zusammenfassung ===")
    print(f"Keller-Absolute-Feuchte:          {stats['cellar_ah_g_m3']} g/m³")
    print(f"Ø Lüftungsstunden pro Tag:         {stats['avg_ventilation_hours_per_day']} h")
    print(f"Beste Stunde zum Lüften:           {stats['best_hour']:02d}:00 "
          f"({stats['best_hour_prob']} % der Sommertage)")
    print(f"Schlechteste Stunde zum Lüften:    {stats['worst_hour']:02d}:00 "
          f"({stats['worst_hour_prob']} % der Sommertage)")

    # --- Plots ---
    print("\nErzeuge Diagramme …")
    plots.plot_temperature(hourly, f"{OUTPUT_DIR}/01_temperatur_tagesgang.png")
    plots.plot_relative_humidity(hourly, f"{OUTPUT_DIR}/02_relative_feuchte_tagesgang.png")
    plots.plot_absolute_humidity(hourly, f"{OUTPUT_DIR}/03_absolute_feuchte_tagesgang.png")
    plots.plot_ventilation_probability(hourly, f"{OUTPUT_DIR}/04_lueftungswahrscheinlichkeit.png")
    plots.plot_heatmap(df, f"{OUTPUT_DIR}/05_heatmap_stunde_monat.png")
    plots.plot_absolute_humidity_variance(df, f"{OUTPUT_DIR}/06_absolute_feuchte_varianz.png")
    plots.plot_daily_absolute_humidity(raw_df, f"{OUTPUT_DIR}/07_absolute_feuchte_tagesverlauf_apr_sep.png")

    print(f"\nFertig. Diagramme in '{OUTPUT_DIR}/'.")


if __name__ == "__main__":
    main()
