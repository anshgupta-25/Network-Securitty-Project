Write-Host "Starting demo web services..." -ForegroundColor Cyan

# Start backend website (Flask) in new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location 'D:\Network Securitty Project\backend_websites'; & 'D:/Network Securitty Project/.venv/Scripts/python.exe' app.py"
Write-Host "Started backend demo on http://127.0.0.1:9000" -ForegroundColor Green

# Start simple static server for frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location 'D:\Network Securitty Project\frontend_websites'; & 'D:/Network Securitty Project/.venv/Scripts/python.exe' -m http.server 7000"
Write-Host "Started frontend static server on http://127.0.0.1:7000" -ForegroundColor Green

Write-Host "Open the attacker playground at http://127.0.0.1:7000" -ForegroundColor Cyan
