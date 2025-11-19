# Master Launch Script - Starts entire honeypot system
Write-Host "`n" + ("="*70) -ForegroundColor Cyan
Write-Host "  COMPLETE HONEYPOT THREAT ANALYSIS SYSTEM" -ForegroundColor Cyan
Write-Host ("="*70) + "`n" -ForegroundColor Cyan

Write-Host "This will launch:" -ForegroundColor Yellow
Write-Host "  1. Enhanced Honeypot Backend (SSH + RDP)" -ForegroundColor Green
Write-Host "  2. Flask Dashboard (Web UI)" -ForegroundColor Green
Write-Host "  3. Attack Simulator (Test Suite)`n" -ForegroundColor Green

# Check if honeypot is already running
try {
    $test = Invoke-RestMethod -Uri "http://127.0.0.1:8000/statistics" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "✓ Honeypot backend is already running!" -ForegroundColor Green
    $honeypotRunning = $true
} catch {
    Write-Host "⚠ Honeypot not running, will start it..." -ForegroundColor Yellow
    $honeypotRunning = $false
}

# Start honeypot in new window if not running
if (-not $honeypotRunning) {
    Write-Host "`n[Step 1] Launching Enhanced Honeypot Backend..." -ForegroundColor Cyan
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\start_enhanced_honeypot.ps1"
    Write-Host "  ✓ Honeypot starting in new window..." -ForegroundColor Green
    Write-Host "  ⏳ Waiting 8 seconds for initialization..." -ForegroundColor Yellow
    Start-Sleep -Seconds 8
}

# Start dashboard in new window
Write-Host "`n[Step 2] Launching Flask Dashboard..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\start_dashboard.ps1"
Write-Host "  ✓ Dashboard starting in new window..." -ForegroundColor Green
Write-Host "  ⏳ Waiting 5 seconds for Flask to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Verify services
Write-Host "`n[Step 3] Verifying Services..." -ForegroundColor Cyan

try {
    $stats = Invoke-RestMethod -Uri "http://127.0.0.1:8000/statistics" -TimeoutSec 3
    Write-Host "  ✓ Backend API is responding" -ForegroundColor Green
    Write-Host "    → Events: $($stats.total_events)" -ForegroundColor White
    Write-Host "    → Auth Attempts: $($stats.total_auth_attempts)" -ForegroundColor White
} catch {
    Write-Host "  ✗ Backend API not responding" -ForegroundColor Red
}

try {
    $dashboard = Invoke-WebRequest -Uri "http://127.0.0.1:5000" -TimeoutSec 3 -UseBasicParsing
    Write-Host "  ✓ Dashboard is responding" -ForegroundColor Green
} catch {
    Write-Host "  ⏳ Dashboard still starting..." -ForegroundColor Yellow
}

# Run attack simulator
Write-Host "`n[Step 4] Running Attack Simulator..." -ForegroundColor Cyan
Write-Host "  This will generate test data for the dashboard`n" -ForegroundColor White

Start-Sleep -Seconds 2
.\test_advanced_attacks.ps1

# Display access information
Write-Host "`n" + ("="*70) -ForegroundColor Cyan
Write-Host "  SYSTEM READY!" -ForegroundColor Green
Write-Host ("="*70) + "`n" -ForegroundColor Cyan

Write-Host "🌐 WEB INTERFACES:" -ForegroundColor Yellow
Write-Host "   Dashboard:  http://127.0.0.1:5000" -ForegroundColor Cyan
Write-Host "   API Docs:   http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host ""

Write-Host "📡 API ENDPOINTS:" -ForegroundColor Yellow
Write-Host "   Statistics:      http://127.0.0.1:8000/statistics" -ForegroundColor White
Write-Host "   Auth Attempts:   http://127.0.0.1:8000/auth_attempts" -ForegroundColor White
Write-Host "   Commands:        http://127.0.0.1:8000/commands" -ForegroundColor White
Write-Host "   Sessions:        http://127.0.0.1:8000/sessions" -ForegroundColor White
Write-Host "   WebSocket:       ws://127.0.0.1:8000/ws/events" -ForegroundColor White
Write-Host ""

Write-Host "🎯 HONEYPOT PORTS:" -ForegroundColor Yellow
Write-Host "   SSH:  2222" -ForegroundColor White
Write-Host "   RDP:  3389" -ForegroundColor White
Write-Host ""

Write-Host "📊 NEXT STEPS:" -ForegroundColor Yellow
Write-Host "   1. Open dashboard in browser: http://127.0.0.1:5000" -ForegroundColor White
Write-Host "   2. Run more attacks: .\test_advanced_attacks.ps1" -ForegroundColor White
Write-Host "   3. Monitor real-time: .\monitor_realtime.ps1" -ForegroundColor White
Write-Host ""

Write-Host ("="*70) -ForegroundColor Cyan
Write-Host "  Press any key to open dashboard in browser..." -ForegroundColor Yellow
Write-Host ("="*70) + "`n" -ForegroundColor Cyan

$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
Start-Process "http://127.0.0.1:5000"
