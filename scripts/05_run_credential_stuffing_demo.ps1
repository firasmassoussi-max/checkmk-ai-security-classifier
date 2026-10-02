# 05_run_credential_stuffing_demo.ps1
# Startet ein Login-/Credential-Stuffing Beispiel.

if (-not $env:OPENAI_API_KEY) {
  Write-Error "OPENAI_API_KEY fehlt. Beispiel: `$env:OPENAI_API_KEY='****'"
  exit 1
}

py -3.12 .\src\classify_checkmk_event.py `
  --model gpt-4o-mini `
  --input .\examples\internet_elastic_audit_realm_authentication_failed_adapted.json `
  --output .\examples\result_credential_stuffing.json

Get-Content .\examples\result_credential_stuffing.json -Raw
