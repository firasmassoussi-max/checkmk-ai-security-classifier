# 06_run_cloudwatch_demo.ps1
# Startet das CloudWatch-CPU-Alarm Beispiel.
# Erwartung: häufig unknown/misconfiguration, weil CPU allein keinen Angriff beweist.

if (-not $env:OPENAI_API_KEY) {
  Write-Error "OPENAI_API_KEY fehlt. Beispiel: `$env:OPENAI_API_KEY='****'"
  exit 1
}

py -3.12 .\src\classify_checkmk_event.py `
  --model gpt-4o-mini `
  --input .\examples\internet_cloudwatch_cpu_alarm_adapted.json `
  --output .\examples\result_cloudwatch.json

Get-Content .\examples\result_cloudwatch.json -Raw
