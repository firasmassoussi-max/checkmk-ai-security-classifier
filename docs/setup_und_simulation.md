# Setup und Simulation

Dieses Dokument beschreibt, wie das Projekt lokal gestartet und getestet wird.

## 1. Projekt klonen oder herunterladen

```powershell
git clone https://github.com/firasmassoussi-max/checkmk-ai-security-classifier.git
cd checkmk-ai-security-classifier
```

Alternativ kann das Repository als ZIP heruntergeladen werden.

## 2. Python-Abhaengigkeiten installieren

```powershell
py -3.12 -m pip install -r requirements.txt
```

## 3. API-Key setzen

Der API-Key wird nicht im Code gespeichert. Er wird zur Laufzeit als Umgebungsvariable gesetzt.

```powershell
$env:OPENAI_API_KEY="****"
```

Wenn der Key dauerhaft gesetzt werden soll:

```powershell
setx OPENAI_API_KEY "****"
```

Danach PowerShell neu starten.

## 4. Simulation starten

Malware-/Mining-aehnliches Event testen:

```powershell
py -3.12 .\src\checkmk_ai_classifier.py --input .\examples\event_mining_features.json --output .\result_malware.json
```

Ergebnis anzeigen:

```powershell
Get-Content .\result_malware.json -Raw
```

## 5. Was passiert technisch?

1. Python liest die JSON-Datei.
2. Wenn Messwertlisten vorhanden sind, berechnet Python Kennzahlen wie Mean, Median, Max, P95, Standardabweichung und MAD.
3. Python baut daraus ein kompaktes Feature-Event.
4. Dieses Event wird an die KI-API gesendet.
5. Die KI liefert ein strukturiertes JSON zurueck.
6. Das Ergebnis wird als Datei gespeichert.

## 6. Warum wurde simuliert?

Eigentlich sollte Checkmk die Werte direkt liefern. Da die direkte Einbindung im Projekt nicht umgesetzt werden konnte, wurden die JSON-Events kuenstlich erzeugt bzw. an oeffentliche Beispielstrukturen angelehnt. Dadurch konnte die komplette Pipeline trotzdem nachvollziehbar demonstriert werden.
