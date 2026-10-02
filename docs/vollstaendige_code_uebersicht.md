# Vollständige Code-Übersicht

Diese Datei dokumentiert alle Skripte und Code-Bausteine, die für die Simulation und Demonstration des Projekts relevant sind.

Wichtig: Der echte API-Key wird **nicht** im Repository gespeichert. In der Dokumentation wird er nur als Platzhalter gezeigt:

```powershell
$env:OPENAI_API_KEY="****"
```

## Ordnerstruktur

```text
src/
  classify_checkmk_event.py          # Hauptskript: JSON -> OpenAI API -> Ergebnis-JSON
  checkmk_ai_classifier.py           # erweiterte Variante mit Feature-Berechnung
  feature_engineering.py             # Mittelwert, Median, P95, MAD usw.
  build_feature_event.py             # Rohwerte -> datensparsames Feature-JSON
  openai_responses_client.py         # API-Client für OpenAI Responses API
  validate_event_json.py             # einfache JSON-Prüfung
  redact_event.py                    # Entfernen sensibler Felder
  batch_demo_runner.py               # mehrere JSON-Beispiele automatisch ausführen

scripts/
  01_setup_env.ps1                   # Umgebung vorbereiten
  02_set_api_key_example.ps1          # API-Key als Platzhalter setzen
  03_create_malware_json.ps1         # Malware/Crypto-Mining Demo-JSON erzeugen
  04_run_malware_demo.ps1            # Malware-Demo starten
  05_run_credential_stuffing_demo.ps1# Credential-Stuffing-Demo starten
  06_run_cloudwatch_demo.ps1         # CloudWatch-CPU-Demo starten
  07_show_result.ps1                 # Ergebnisdatei anzeigen
  08_clean_results.ps1               # Ergebnisdateien löschen
  09_run_batch_demo.ps1              # mehrere Beispiele ausführen
  10_check_python_and_requests.ps1    # Python/requests prüfen

examples/
  event_mining_features.json
  internet_cloudwatch_cpu_alarm_adapted.json
  result_example_malware.json
```

## Projektidee

Ursprünglich sollte Checkmk direkt Werte liefern. Da die vollständige Ende-zu-Ende-Anbindung im Projektzeitraum nicht zuverlässig umgesetzt wurde, verwenden wir kontrollierte JSON-Beispieldaten. Diese JSON-Dateien repräsentieren typische Monitoring-Features wie CPU, IOwait, Netzwerkmetriken oder fehlgeschlagene Logins.

Der Ablauf ist:

```text
Monitoring/JSON -> Python-Feature-Verarbeitung -> OpenAI API -> strukturierte KI-Klassifikation
```

## Warum mehrere Skripte?

Für GitHub und eine Arbeitgeber-Demo ist es besser, nicht nur ein einzelnes langes Skript zu zeigen, sondern die Arbeit in verständliche Bausteine aufzuteilen:

- Feature Engineering
- Redaction/Datensparsamkeit
- JSON-Validierung
- API-Kommunikation
- Demo-Ausführung
- Batch-Test

Dadurch sieht man klar, welche Teile des Projekts technisch umgesetzt wurden.