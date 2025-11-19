# Start Enhanced Honeypot with Full Features
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Enhanced Honeypot for Threat Analysis" -ForegroundColor Cyan  
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
& ".\.venv\Scripts\Activate.ps1"

Write-Host "[*] Starting enhanced honeypot backend..." -ForegroundColor Yellow
Write-Host "[*] Features:" -ForegroundColor Yellow
Write-Host "    - SSH Protocol Emulation (Port 2222)" -ForegroundColor Green
Write-Host "    - RDP Protocol Emulation (Port 3389)" -ForegroundColor Green
Write-Host "    - Credential Capture" -ForegroundColor Green
Write-Host "    - Command Logging" -ForegroundColor Green
Write-Host "    - Session Tracking" -ForegroundColor Green
Write-Host "    - Attack Pattern Analysis" -ForegroundColor Green
Write-Host ""
Write-Host "[*] API Endpoints:" -ForegroundColor Yellow
Write-Host "    - http://127.0.0.1:8000/events" -ForegroundColor Cyan
Write-Host "    - http://127.0.0.1:8000/auth_attempts" -ForegroundColor Cyan
Write-Host "    - http://127.0.0.1:8000/commands" -ForegroundColor Cyan
Write-Host "    - http://127.0.0.1:8000/sessions" -ForegroundColor Cyan
Write-Host "    - http://127.0.0.1:8000/statistics" -ForegroundColor Cyan
Write-Host "    - ws://127.0.0.1:8000/ws/events" -ForegroundColor Cyan
Write-Host ""
Write-Host "[!] Press CTRL+C to stop the honeypot" -ForegroundColor Red
Write-Host ""

# Run the enhanced server
& "D:/Network Securitty Project/.venv/Scripts/python.exe" -m uvicorn backend.app.main_enhanced:app --host 0.0.0.0 --port 8000
