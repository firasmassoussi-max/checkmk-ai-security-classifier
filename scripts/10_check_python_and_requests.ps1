# 10_check_python_and_requests.ps1
# Prüft Python-Version und ob requests installiert ist.

Write-Host "Python-Versionen:"
py -0p

Write-Host "requests prüfen:"
py -3.12 -c "import requests; print(requests.__version__)"

Write-Host "Wenn requests fehlt:"
Write-Host "py -3.12 -m pip install -r .\requirements.txt"
