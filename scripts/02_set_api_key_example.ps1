# 02_set_api_key_example.ps1
# Beispiel: API-Key setzen. Niemals den echten Key in GitHub speichern.

$env:OPENAI_API_KEY="****"

Write-Host "OPENAI_API_KEY wurde für diese PowerShell-Session gesetzt (nur Platzhalter)."
Write-Host "Für echte Tests lokal ersetzen, aber NICHT committen."
