# 07_show_result.ps1
# Zeigt eine Ergebnisdatei im Terminal an.

param(
  [string]$Path = ".\examples\result_malware.json"
)

if (-not (Test-Path $Path)) {
  Write-Error "Datei nicht gefunden: $Path"
  exit 1
}

Get-Content $Path -Raw
