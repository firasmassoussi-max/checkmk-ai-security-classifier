# 09_run_batch_demo.ps1
# Führt mehrere Demo-Dateien nacheinander aus.

if (-not $env:OPENAI_API_KEY) {
  Write-Error "OPENAI_API_KEY fehlt. Beispiel: `$env:OPENAI_API_KEY='****'"
  exit 1
}

py -3.12 .\src\batch_demo_runner.py `
  --inputs `
  .\examples\event_mining_features.json `
  .\examples\internet_cloudwatch_cpu_alarm_adapted.json `
  --outdir .\results `
  --model gpt-4o-mini

Get-Content .\results\summary.json -Raw
