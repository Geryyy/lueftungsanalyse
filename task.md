# Task: Analyse von Lüftungsmöglichkeiten anhand von Geosphere Wetterdaten

Dieses Projekt verwendet die Geosphere Climate Data API, um Wetterdaten auszuwerten und statistisch zu bestimmen, **wann Kellerlüftung im Sommer sinnvoll ist**.

Die physikalischen Grundlagen und Ziele sind im `context.md` beschrieben.

---

# Ziel der Implementierung

Implementiere ein Python-Programm, das:

1. Wetterdaten über die **Geosphere API** lädt
2. Temperatur und relative Feuchte verarbeitet
3. **absolute Luftfeuchte berechnet**
4. den **typischen Tagesverlauf in Sommermonaten** bestimmt
5. statistisch analysiert, wann Lüften sinnvoll wäre
6. Diagramme erzeugt

---

# Projektstruktur

Das Programm soll folgende Struktur haben:

project/

```
context.md
task.md
main.py
api.py
humidity.py
analysis.py
plots.py
config.py
```

---

# Konfigurationsdatei

Datei: `config.py`

Definiere dort:

* Messstation
* Zeitraum
* Sommermonate
* Kellerparameter

Beispiel:

```python
STATION_ID = "LINZ"

START_DATE = "2015-01-01"
END_DATE = "2024-12-31"

SUMMER_MONTHS = [6, 7, 8]

CELLAR_TEMP = 15
CELLAR_RH = 70
```

---

# API Zugriff

Datei: `api.py`

Verwende die Geosphere API:

https://dataset.api.hub.geosphere.at/v1/docs/

Datensatz:

klima-v2-1h

Zu ladende Parameter:

* TL (Temperatur)
* RF (relative Luftfeuchte)

Funktion:

```python
def load_weather_data(station, start_date, end_date):
```

Die Funktion soll:

1. API Request ausführen
2. Daten in `pandas.DataFrame` konvertieren
3. Timestamp parsen
4. DataFrame zurückgeben

Spalten:

```
timestamp
temperature
relative_humidity
```

---

# Berechnung absolute Feuchte

Datei: `humidity.py`

Implementiere Funktion:

```python
def absolute_humidity(temp_c, rel_humidity):
```

Formel:

```
AH = 6.112 * exp((17.67 * T)/(T + 243.5)) * RH * 2.1674 / (273.15 + T)
```

Einheiten:

* Temperatur in °C
* relative Feuchte in %

Output:

g/m³

---

# Kellerreferenz

Implementiere Funktion:

```python
def cellar_absolute_humidity(temp, rh):
```

Verwende Werte aus `config.py`.

---

# Analyse

Datei: `analysis.py`

Schritte:

1. Filter auf Sommermonate
2. absolute Feuchte berechnen
3. Stunden des Tages extrahieren
4. nach Stunde gruppieren

Berechne:

* durchschnittliche Temperatur
* durchschnittliche relative Feuchte
* durchschnittliche absolute Feuchte

---

# Lüftungsanalyse

Implementiere zusätzlich:

```
df["ventilation_possible"] = df["ah_outside"] < cellar_ah
```

Berechne:

* Wahrscheinlichkeit pro Stunde
* durchschnittliche Lüftungsstunden pro Tag

---

# Visualisierung

Datei: `plots.py`

Erzeuge folgende Plots:

## 1 Temperatur Tagesgang

x: Stunde
y: Temperatur

---

## 2 Relative Feuchte Tagesgang

x: Stunde
y: %

---

## 3 Absolute Feuchte Tagesgang

x: Stunde
y: g/m³

---

## 4 Lüftungswahrscheinlichkeit

x: Stunde
y: Wahrscheinlichkeit

---

# Hauptprogramm

Datei: `main.py`

Workflow:

1. Daten laden
2. absolute Feuchte berechnen
3. Kellerreferenz berechnen
4. Analyse durchführen
5. Plots erzeugen

---

# Erweiterungen (optional)

Wenn Zeit vorhanden ist, implementiere zusätzlich:

## Mehrere Kellerbedingungen

Untersuche verschiedene Kellerfeuchten:

```
60 %
70 %
80 %
```

---

## Unterschiedliche Kellertemperaturen

z. B.

```
12 °C
15 °C
18 °C
```

---

## Heatmap

Stunde vs Monat:

Wahrscheinlichkeit für Lüften.

---

# Erwartetes Ergebnis

Das Programm soll folgende Fragen beantworten:

* Wann ist Lüften im Sommer sinnvoll?
* Gibt es typische Tageszeiten?
* Wie viele Stunden pro Tag sind nutzbar?

---

# Ziel

Die Analyse soll eine **praktische Grundlage für die Steuerung einer Kellerlüftung** liefern.

Die Ergebnisse können später genutzt werden für:

* Taupunktsteuerung
* Ventilatorsteuerung
* Bauphysikalische Bewertung.
