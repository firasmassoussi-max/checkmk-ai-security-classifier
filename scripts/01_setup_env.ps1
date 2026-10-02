# 01_setup_env.ps1
# Erstellt eine lokale Python-Umgebung und installiert Abhängigkeiten.

Write-Host "[1/3] Python-Version prüfen"
py -3.12 --version

Write-Host "[2/3] Virtuelle Umgebung erstellen"
py -3.12 -m venv .venv

Write-Host "[3/3] requirements installieren"
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r .\requirements.txt

Write-Host "Fertig. Aktivieren mit: .\.venv\Scripts\Activate.ps1"
