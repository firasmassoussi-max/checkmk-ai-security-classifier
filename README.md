# Checkmk AI Security Classifier

Dieses Repository dokumentiert ein Projekt zur **KI-gestützten Klassifikation von Monitoring- und Security-Events**.

Die Grundidee ist:

```text
Checkmk / Monitoring-Werte -> JSON -> Python-Preprocessing -> KI-API -> strukturiertes Ergebnis
```

Da im Projekt keine direkte produktive Checkmk-Anbindung umgesetzt werden konnte, wurden die Eingabedaten als **synthetische JSON-Dateien** erzeugt bzw. an öffentlich verfügbare Beispielstrukturen angelehnt und angepasst. Dadurch konnte die komplette Pipeline trotzdem simuliert und dokumentiert werden.

## Ziel des Projekts

Das Projekt zeigt, wie Monitoring-Daten und Schwellwerte, z. B. CPU-Auslastung, Netzwerkverhalten oder verdächtige Prozessaktivität, in ein einheitliches JSON-Format gebracht werden können. Danach werden diese Daten an eine KI-API gesendet, damit die KI eine mögliche Angriffskategorie erkennt und eine kurze Erklärung liefert.

Die KI gibt ein festes JSON-Ergebnis zurück:

```json
{
  "attack_type": "malware",
  "confidence": 0.85,
  "explanation": "Kurze Begründung der Analyse",
  "recommended_next_steps": [
    "Prozesse prüfen",
    "Netzwerkverbindungen analysieren",
    "Host isolieren, falls Verdacht bestätigt wird"
  ]
}
```

## Warum JSON?

JSON wurde genutzt, weil es einfach lesbar ist, gut von Python verarbeitet werden kann und sich für APIs eignet. In diesem Projekt wird JSON sowohl als Eingabeformat als auch als Ausgabeformat verwendet.

## Datensparsamkeit

Es werden nicht komplette Logs an die KI geschickt. Stattdessen werden Werte zusammengefasst, z. B.:

- Durchschnitt
- Median
- Maximum
- MAD (Median Absolute Deviation)
- Dauer über einem Schwellwert
- Anzahl neuer Prozesse
- Anzahl ausgehender Verbindungen

Dadurch erhält die KI genug Kontext, ohne dass unnötig viele sensible Rohdaten übertragen werden.

## API-Key

Der API-Key wird **nicht im Code gespeichert**. Für die Dokumentation wird er immer zensiert dargestellt:

```text
OPENAI_API_KEY=****
```

In PowerShell wird der Key zur Laufzeit gesetzt:

```powershell
$env:OPENAI_API_KEY="****"
```

## Setup

```powershell
cd $HOME\Downloads\checkmk_ai
py -3.12 -m pip install -r requirements.txt
$env:OPENAI_API_KEY="****"
```

## Simulation starten

Beispiel mit dem Malware-/Mining-ähnlichen Event:

```powershell
py -3.12 .\src\checkmk_ai_classifier.py --input .\examples\event_mining_features.json --output .\result_malware.json
Get-Content .\result_malware.json -Raw
```

## Repository-Struktur

```text
.
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── checkmk_ai_classifier.py
│   └── classify_checkmk_event.py
├── examples/
│   ├── event_mining_features.json
│   ├── internet_cloudwatch_cpu_alarm_adapted.json
│   └── result_example_malware.json
└── docs/
    ├── setup_und_simulation.md
    ├── projektbeschreibung.md
    ├── sicherheit_datensparsamkeit.md
    └── quellen.md
```

## Hinweis

Dieses Projekt ist eine Simulation für Lern- und Demonstrationszwecke. Es ersetzt keine produktive SOC-Lösung und keine vollständige SIEM/SOAR-Integration.
