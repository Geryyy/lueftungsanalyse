# Context: Kellerlüftungsanalyse mit Geosphere Wetterdaten

## Ziel

Dieses Projekt analysiert Wetterdaten aus Österreich, um zu bestimmen, **wann Lüften eines kühlen Kellers sinnvoll ist**.

Der Keller hat im Sommer typischerweise eine **Temperatur von ca. 15 °C**.

Lüften ist nur sinnvoll, wenn die **absolute Feuchte der Außenluft niedriger ist als die absolute Feuchte der Kellerluft**, da sonst Feuchtigkeit in den Keller eingebracht wird und Kondensation auftreten kann.

Ziel der Analyse:

1. Wetterdaten über die Geosphere API abrufen
2. Temperatur und relative Luftfeuchte auswerten
3. absolute Luftfeuchte berechnen
4. typische **Tagesverläufe in Sommermonaten** analysieren
5. Zeitfenster bestimmen, in denen Lüften sinnvoll wäre

---

# Datenquelle

Geosphere Austria Climate Data API

Dokumentation:

https://dataset.api.hub.geosphere.at/v1/docs/

Datensatz:

klima-v2-1h (stündliche Wetterdaten)

Parameter von Interesse:

* `TL` → Lufttemperatur (°C)
* `RF` → relative Luftfeuchte (%)

Zeitauflösung:

* 1 Stunde

---

# Geografischer Fokus

Region:

Oberösterreich / Österreich

Geeignete Messstationen:

* Weyer (PLZ 3335)

---

# Zeitraum der Analyse

Sommermonate:

* Juni
* Juli
* August

Empfohlen:

mehrjährige Daten (z. B. 2015–2024), um statistisch stabile Aussagen zu erhalten.

---

# Physikalisches Modell

Für die Lüftungsentscheidung wird **absolute Feuchte (g/m³)** verwendet.

Relative Luftfeuchte ist nicht geeignet, da sie stark temperaturabhängig ist.

## Berechnung der absoluten Feuchte

Formel:

AH = 6.112 * exp((17.67 * T) / (T + 243.5)) * RH * 2.1674 / (273.15 + T)

Parameter:

T  = Temperatur in °C
RH = relative Feuchte in %

Ergebnis:

absolute Feuchte in g/m³

---

# Kellerreferenz

Sommer-Kellertemperatur:

15 °C

Maximale absolute Feuchte bei 15 °C (100 % RH):

≈ 12.8 g/m³

Wenn Außenluft mehr absolute Feuchte enthält, führt Lüften zu Kondensation im Keller.

---

# Lüftungsbedingung

Lüften ist sinnvoll wenn:

AH_outside < AH_cellar

Da die Kellerfeuchte typischerweise bei 60–80 % RH liegt, kann optional eine Referenz angenommen werden:

Keller:

T = 15 °C
RH = 70 %

Daraus ergibt sich:

AH_cellar ≈ 9 g/m³

Diese Annahme kann im Modell variiert werden.

---

# Analyseziele

Die Analyse soll folgende Fragen beantworten:

## 1. Typischer Tagesverlauf

Für Sommermonate:

Berechne den durchschnittlichen Tagesverlauf von:

* Temperatur
* relativer Feuchte
* absoluter Feuchte

Aggregiert über:

Stunden des Tages (0–23)

---

## 2. Lüftungsfenster

Bestimme für jede Stunde:

Wahrscheinlichkeit, dass

AH_outside < AH_cellar

Ergebnis:

Statistik über Lüftungsmöglichkeiten pro Tageszeit.

---

## 3. Lüftungsdauer

Berechne:

durchschnittliche Anzahl Stunden pro Tag im Sommer, in denen Lüften sinnvoll wäre.

---

## 4. Wetterlagen

Optional:

analysiere Unterschiede zwischen

* trockenen Tagen
* schwülen Tagen
* Gewitterlagen

---

# Erwartete Outputs

Das Programm soll erzeugen:

## Diagramme

1. Tagesverlauf Temperatur
2. Tagesverlauf relative Feuchte
3. Tagesverlauf absolute Feuchte
4. Wahrscheinlichkeit für sinnvolle Lüftung pro Stunde

---

## Statistische Ergebnisse

Beispiele:

* durchschnittliche Lüftungsstunden pro Tag
* beste Tageszeit zum Lüften
* schlechteste Tageszeit

---

# Implementierung

Sprache:

Python

Empfohlene Libraries:

* requests
* pandas
* numpy
* matplotlib
* seaborn

---

# Verarbeitungsschritte

1. API Daten abrufen
2. relevante Parameter extrahieren
3. absolute Feuchte berechnen
4. Daten nach Stunde gruppieren
5. Mittelwerte und Verteilungen berechnen
6. Visualisierungen erstellen

---

# Erweiterungen

Optional können später ergänzt werden:

* Taupunktanalyse
* unterschiedliche Kellerfeuchten
* Jahresanalyse
* automatische Lüftungsstrategie

---

# Ziel der Analyse

Die Analyse soll zeigen:

* ob Lüften im Sommer überhaupt sinnvoll ist
* wann Lüften am ehesten funktioniert
* wie groß die nutzbaren Zeitfenster sind

Diese Ergebnisse können anschließend verwendet werden, um:

* eine Kellerlüftungssteuerung zu optimieren
* Ventilatorsteuerungen zu dimensionieren
* Bauphysikalische Entscheidungen zu treffen.
