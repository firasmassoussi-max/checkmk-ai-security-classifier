# Sicherheit und Datensparsamkeit

## Grundidee

Bei der Übergabe an eine externe KI-API sollen keine sensiblen Rohdaten übertragen werden. Deshalb nutzt das Projekt Datensparsamkeit: Es werden nur die Informationen gesendet, die für eine Einschätzung wirklich notwendig sind.

## Keine Rohdaten

Es werden keine vollständigen Logs, keine kompletten Prozesslisten, keine echten Benutzernamen und keine echten IP-Listen an die KI gesendet.

Stattdessen werden Kennzahlen verwendet, z. B.:

- CPU-Durchschnitt
- CPU-Maximum
- Median
- MAD
- Dauer über einem Schwellwert
- Anzahl neuer Prozesse
- Anzahl ausgehender Verbindungen

## Beispiel CPU

Statt zu senden, welche Prozesse genau laufen, wird nur eine Zusammenfassung übertragen:

```text
Average CPU: 82%
Peak CPU: 99%
Median CPU: 80%
Dauer ueber 90%: 3 Minuten
```

Damit bekommt die KI genug Kontext, ohne sensible Details zu sehen.

## API-Sicherheit

Der API-Key wird nicht im Code gespeichert. In der Dokumentation wird er nur so dargestellt:

```text
OPENAI_API_KEY=****
```

Die Verbindung zur API erfolgt über HTTPS/TLS.

## Kontrollierter Output

Die KI darf nicht beliebig antworten, sondern muss ein festes JSON-Schema erfüllen. Dadurch sind die Ergebnisse nachvollziehbar und vergleichbar.

Das Ausgabeformat enthält:

- Angriffstyp
- Confidence
- Erklärung
- Next Steps

## Warum das wichtig ist

Datensparsamkeit reduziert das Risiko, sensible Informationen an externe Systeme weiterzugeben. Gleichzeitig bleibt die Analyse trotzdem aussagekräftig, weil die wichtigsten Kennzahlen erhalten bleiben.
