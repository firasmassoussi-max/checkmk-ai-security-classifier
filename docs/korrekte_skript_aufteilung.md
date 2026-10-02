# Korrekte Skript-Aufteilung der Demo-Pipeline

Diese Datei erklärt die eigentlichen Projekt-Skripte. Gemeint sind hier nicht nur PowerShell-Befehle zum Starten, sondern die fachlichen Bausteine der Pipeline.

## 1. Daten-Sammel-Skript

Datei:

```text
src/pipeline/01_data_collector_simulated.py
```

Aufgabe:
Dieses Skript steht für den Teil, der ursprünglich von Checkmk kommen sollte. In der echten Projektidee hätte Checkmk Werte wie CPU-Auslastung, IOwait, Netzwerktraffic oder fehlgeschlagene Logins geliefert.

Da die direkte Checkmk-Anbindung im Projektzeitraum nicht stabil umgesetzt wurde, simuliert dieses Skript solche Werte. Dadurch bleibt die Demo reproduzierbar.

## 2. Event-Skript / JSON-Formatter

Datei:

```text
src/pipeline/02_event_builder.py
```

Aufgabe:
Dieses Skript nimmt die gesammelten Werte und baut daraus ein datensparsames Event-JSON. Dabei werden aus Rohwerten Kennzahlen berechnet, zum Beispiel:

- Mittelwert
- Median
- Minimum
- Maximum
- MAD

Dadurch werden nicht alle Einzelwerte oder Logs an die KI gesendet, sondern nur verdichtete Features.

## 3. API-Skript

Datei:

```text
src/pipeline/03_ai_api_client.py
```

Aufgabe:
Dieses Skript übernimmt die Kommunikation mit der KI-API. Es liest das Event-JSON ein, erstellt daraus eine Anfrage und sendet sie an die OpenAI Responses API.

Der API-Key steht nicht im Code. Er wird über eine Umgebungsvariable gesetzt:

```powershell
$env:OPENAI_API_KEY="****"
```

## 4. Pipeline-Skript

Datei:

```text
src/pipeline/04_run_full_pipeline.py
```

Aufgabe:
Dieses Skript verbindet alle Schritte:

```text
Daten sammeln/simulieren -> Event-JSON bauen -> API senden -> Ergebnis speichern
```

Damit kann die komplette Demo mit einem Befehl gestartet werden.

## Beispielausführung

```powershell
cd checkmk-ai-security-classifier
python -m pip install -r requirements.txt
$env:OPENAI_API_KEY="****"
python src/pipeline/04_run_full_pipeline.py --scenario malware --model gpt-4o-mini
```

## Warum diese Aufteilung wichtig ist

Die Aufteilung zeigt klar, wie das Projekt gedacht ist:

- Checkmk beziehungsweise simulierte Checkmk-Werte liefern technische Daten.
- Python berechnet daraus Features.
- Das Event-Skript baut ein sauberes JSON.
- Das API-Skript sendet das JSON an die KI.
- Das Ergebnis wird wieder als JSON gespeichert.

So kann ein Arbeitgeber sehen, dass das Projekt nicht nur aus einer einzelnen Datei besteht, sondern aus mehreren nachvollziehbaren Komponenten.
