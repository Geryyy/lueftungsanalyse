# Kellerlüftungsanalyse

Analysiert stündliche Wetterdaten der [Geosphere Austria API](https://dataset.api.hub.geosphere.at/v1/docs/), um zu bestimmen, wann Lüften eines kühlen Kellers im Sommer sinnvoll ist.

## Hintergrund

Lüften ist nur dann sinnvoll, wenn die **absolute Feuchte der Außenluft niedriger** ist als die der Kellerluft. Relative Feuchte allein reicht als Kriterium nicht aus, da sie stark temperaturabhängig ist.

```
AH = 6.112 · exp((17.67 · T) / (T + 243.5)) · RH · 2.1674 / (273.15 + T)   [g/m³]
```

## Datenquelle

- API: `klima-v2-1h` (stündliche Klimadaten)
- Station: **Weyer, OÖ** (ID 104)
- Zeitraum: 2015–2024

## Konfiguration

Alle Parameter in [`config.py`](config.py):

| Parameter | Wert | Bedeutung |
|---|---|---|
| `STATION_ID` | 104 | Geosphere Station Weyer |
| `START_DATE` | 2015-01-01 | Beginn des Analysezeitraums |
| `END_DATE` | 2024-12-31 | Ende des Analysezeitraums |
| `SUMMER_MONTHS` | [6, 7, 8] | Monate für Stunden-Analyse |
| `CELLAR_TEMP` | 15 °C | angenommene Kellertemperatur |
| `CELLAR_RH` | 70 % | angenommene Kellerfeuchte |

## Installation

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Ausführen

```bash
python main.py
```

Beim ersten Aufruf werden die Wetterdaten von der API geladen und in `weather_cache.pkl` gespeichert. Folgeaufrufe verwenden den Cache.

Ergebnisse werden in `output/` gespeichert.

## Projektstruktur

```
config.py       Konfiguration (Station, Zeitraum, Kellerparameter)
api.py          Geosphere API-Abruf (jahresweise, mit Cache)
humidity.py     Berechnung absolute Feuchte
analysis.py     Filterung, Stundenmittel, Lüftungsstatistik
plots.py        Diagramme
main.py         Hauptprogramm
```

## Ausgabe

| Datei | Inhalt |
|---|---|
| `01_temperatur_tagesgang.png` | Mittlerer Tagesverlauf Temperatur (Jun–Aug) |
| `02_relative_feuchte_tagesgang.png` | Mittlerer Tagesverlauf relative Feuchte |
| `03_absolute_feuchte_tagesgang.png` | Mittlerer Tagesverlauf absolute Feuchte mit Kellerreferenz |
| `04_lueftungswahrscheinlichkeit.png` | Wahrscheinlichkeit für sinnvolles Lüften pro Stunde |
| `05_heatmap_stunde_monat.png` | Lüftungswahrscheinlichkeit Stunde × Monat |
| `06_absolute_feuchte_varianz.png` | Absolute Feuchte mit Mittelwert und Streuung (Stunden) |
| `07_absolute_feuchte_tagesverlauf_apr_sep.png` | Absolute Feuchte Tagesmittel Apr–Sep mit Kellerreferenzen (70/80/90 % RH) |

## Ergebnis (Weyer, 2015–2024)

Die mittlere absolute Außenfeuchte liegt im Sommer stets deutlich über der Keller-Referenz (~9 g/m³ bei 70 % RH / 15 °C). Lüften ist nur an einzelnen trockenen Tagen sinnvoll, hauptsächlich im April und September sowie vereinzelt an Tagen nach Kaltfrontdurchgängen.
