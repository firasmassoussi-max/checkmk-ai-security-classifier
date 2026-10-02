# Projektbeschreibung

## Ausgangssituation

Checkmk ist ein Monitoring-System, das Zustände und Schwellwerte von Systemen überwachen kann. Typische Beispiele sind CPU-Auslastung, Speicher, Netzwerk-Traffic, Prozesse oder fehlgeschlagene Logins.

Im Projekt sollte untersucht werden, wie solche Monitoring-Werte in ein JSON-Format gebracht und anschließend an eine KI-API weitergeleitet werden können. Die KI soll daraus eine mögliche Angriffskategorie erkennen und eine Erklärung liefern.

## Umgesetzter Ansatz

Die produktive Checkmk-Anbindung konnte im Projekt nicht vollständig umgesetzt werden. Deshalb wurden JSON-Dateien für die Simulation verwendet. Diese JSON-Dateien wurden entweder synthetisch erstellt oder an öffentliche Beispielstrukturen angelehnt und angepasst.

Die Simulation bildet trotzdem den geplanten Ablauf ab:

```text
Checkmk-Werte / Schwellwerte -> JSON -> Python -> KI-API -> Ergebnis-JSON
```

## Rolle von Python

Python übernimmt in der Pipeline mehrere Aufgaben:

1. JSON-Datei einlesen
2. Messwerte formatieren
3. Kennzahlen berechnen, z. B. Mittelwert, Median, Maximum, P95 und MAD
4. API-Request an die KI vorbereiten
5. Antwort der KI verarbeiten
6. Ergebnis als JSON speichern

Je mehr sinnvolle Informationen die KI bekommt, desto genauer kann die Analyse sein. Einzelne Werte wie nur CPU 95 Prozent reichen oft nicht aus. Mehr Kontext, z. B. Dauer, Median, Prozessaktivität und Netzwerkverhalten, verbessert die Einschätzung.

## Output der KI

Die KI antwortet in einem festen Format:

- `attack_type`: vermutete Angriffskategorie
- `confidence`: Sicherheit der Einschätzung
- `explanation`: kurze Begründung
- `recommended_next_steps`: empfohlene nächste Schritte

Dadurch ist die Ausgabe nicht nur ein freier Text, sondern strukturiert und vergleichbar.

## Zielgruppe

Das Projekt eignet sich als Demonstration für Arbeitgeber, Ausbildung, Studium oder Portfolio. Es zeigt Grundlagen in Monitoring, JSON, Python, API-Kommunikation, Security-Analyse und datensparsamer Verarbeitung.
