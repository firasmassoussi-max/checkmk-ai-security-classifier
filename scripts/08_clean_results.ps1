# 08_clean_results.ps1
# Löscht lokal erzeugte Ergebnisdateien.
# Dient dazu, die Demo sauber neu zu starten.

Get-ChildItem .\examples\result*.json -ErrorAction SilentlyContinue | Remove-Item -Force
Get-ChildItem .\results\*.json -ErrorAction SilentlyContinue | Remove-Item -Force

Write-Host "Ergebnisdateien wurden gelöscht."
