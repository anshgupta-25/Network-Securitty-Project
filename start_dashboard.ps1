# Start Flask Dashboard
Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "  Honeypot Threat Analysis Dashboard" -ForegroundColor Cyan  
Write-Host "================================================`n" -ForegroundColor Cyan

# Activate virtual environment
& ".\.venv\Scripts\Activate.ps1"

Write-Host "[*] Starting Flask dashboard..." -ForegroundColor Yellow
Write-Host "[*] Dashboard URL: http://127.0.0.1:5000" -ForegroundColor Green
Write-Host "[*] Features:" -ForegroundColor Yellow
Write-Host "    - Real-time statistics" -ForegroundColor Cyan
Write-Host "    - Attack timeline visualization" -ForegroundColor Cyan
Write-Host "    - Top passwords & usernames charts" -ForegroundColor Cyan
Write-Host "    - Command execution analysis" -ForegroundColor Cyan
Write-Host "    - Geographic distribution" -ForegroundColor Cyan
Write-Host "    - Session replay & forensics`n" -ForegroundColor Cyan

Write-Host "[!] Press CTRL+C to stop the dashboard`n" -ForegroundColor Red

# Install Flask dependencies if not present
Write-Host "[*] Installing dashboard dependencies..." -ForegroundColor Yellow
& "D:/Network Securitty Project/.venv/Scripts/python.exe" -m pip install -q Flask Flask-CORS

# Run Flask dashboard
& "D:/Network Securitty Project/.venv/Scripts/python.exe" dashboard/app.py
