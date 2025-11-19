# Real-Time Attack Websites Integration

All test/attack/demo .ps1 scripts have been **removed** from the project per your request.

## New Architecture

```
┌────────────────────────────────┐
│  Frontend (Port 7000)          │  ← Attacker's browser UI
│  frontend_websites/index.html  │
└────────────────┬───────────────┘
                 │ POST /login, /submit_cmd
                 ↓
┌────────────────────────────────┐
│  Backend (Port 9000)           │  ← Vulnerable demo site
│  backend_websites/app.py       │
└────────────────┬───────────────┘
                 │ POST /ingest/web (JSON)
                 ↓
┌────────────────────────────────┐
│  Honeypot (Port 8000)          │  ← Main honeypot backend
│  backend/app/main_enhanced.py  │
│  + TCP honeypots (2222, 3389)  │
└────────────────┬───────────────┘
                 │ Real-time storage & broadcast
                 ↓
┌────────────────────────────────┐
│  Dashboard (Port 5000)         │  ← Monitoring UI
│  dashboard/app.py              │
└────────────────────────────────┘
```

## Starting the System

### 1. Start Enhanced Honeypot
```powershell
.\start_enhanced_honeypot.ps1
```
- Listens on port 8000 (API + WebSocket)
- Listens on ports 2222 (SSH), 3389 (RDP) for TCP attacks
- Provides `/ingest/web` endpoint to receive events from backend_websites

### 2. Start Demo Websites
```powershell
.\start_websites.ps1
```
- Starts **backend_websites** on port 9000 (Flask app with /login, /submit_cmd)
- Starts **frontend_websites** on port 7000 (static HTML served via Python http.server)

### 3. Start Dashboard (Optional)
```powershell
.\start_dashboard.ps1
```
- Dashboard UI on port 5000
- Shows real-time stats from honeypot DB

## Testing Real-Time Attacks

### Option 1: Use the Attacker Playground (Browser)
1. Open: http://127.0.0.1:7000
2. Fill in username/password and click "Send"
3. The login attempt is forwarded to `backend_websites` → `honeypot ingest` → stored in DB
4. Check dashboard at http://127.0.0.1:5000 (click Refresh Data)

### Option 2: Use PowerShell/curl
```powershell
# Send login attempt
Invoke-RestMethod -Uri http://127.0.0.1:9000/login -Method Post `
  -Body (@{username='hacker';password='pass123'} | ConvertTo-Json) `
  -ContentType 'application/json'

# Send command
Invoke-RestMethod -Uri http://127.0.0.1:9000/submit_cmd -Method Post `
  -Body (@{session_id='web-1';command='whoami'} | ConvertTo-Json) `
  -ContentType 'application/json'

# Check honeypot stats
Invoke-RestMethod http://127.0.0.1:8000/statistics | ConvertTo-Json -Depth 3
```

### Option 3: Direct ingest API
```powershell
# Post auth attempt directly to honeypot
Invoke-RestMethod -Uri http://127.0.0.1:8000/ingest/web -Method Post `
  -Body (@{type='auth';payload=@{src_ip='1.2.3.4';username='root';password='toor';service='web'}} | ConvertTo-Json -Depth 3) `
  -ContentType 'application/json'
```

## URLs

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://127.0.0.1:7000 | Attacker playground (static HTML) |
| **Backend** | http://127.0.0.1:9000 | Vulnerable demo site (Flask) |
| **Honeypot API** | http://127.0.0.1:8000/statistics | Stats endpoint |
| **Honeypot Ingest** | http://127.0.0.1:8000/ingest/web | Receives forwarded events |
| **WebSocket** | ws://127.0.0.1:8000/ws/events | Real-time event stream |
| **Dashboard** | http://127.0.0.1:5000 | Monitoring UI |

## How It Works

1. **Frontend** (port 7000) sends login/command to **backend** (port 9000)
2. **Backend** forwards the event as JSON to **honeypot ingest** (port 8000)
3. **Honeypot** stores in SQLite DB and broadcasts via WebSocket
4. **Dashboard** (port 5000) fetches stats from honeypot API

## Real-Time Flow

```
User types "admin/pass123" in browser
  ↓
Frontend POST → http://127.0.0.1:9000/login
  ↓
Backend Flask forwards → http://127.0.0.1:8000/ingest/web
  ↓
Honeypot inserts into `auth_attempts` table + broadcasts to WebSocket clients
  ↓
Dashboard queries /statistics and displays updated charts
```

## No Test Scripts

All `.ps1` test/attack/demo scripts have been removed:
- ✅ Removed: test_system.ps1
- ✅ Removed: test_attacks.ps1
- ✅ Removed: test_advanced_attacks.ps1
- ✅ Removed: start_and_test.ps1
- ✅ Removed: run_attack_test.ps1
- ✅ Removed: comprehensive_attack_test.ps1
- ✅ Removed: quick_fix.ps1
- ✅ Removed: demo_realtime.ps1
- ✅ Removed: monitor_realtime.ps1

**Only production launchers remain:**
- start_enhanced_honeypot.ps1
- start_dashboard.ps1
- start_websites.ps1
- launch_system.ps1

## Verification Commands

```powershell
# Check all services are running
Test-NetConnection -ComputerName 127.0.0.1 -Port 7000  # Frontend
Test-NetConnection -ComputerName 127.0.0.1 -Port 9000  # Backend
Test-NetConnection -ComputerName 127.0.0.1 -Port 8000  # Honeypot
Test-NetConnection -ComputerName 127.0.0.1 -Port 5000  # Dashboard

# Get honeypot statistics
Invoke-RestMethod http://127.0.0.1:8000/statistics

# Get auth attempts
Invoke-RestMethod http://127.0.0.1:8000/auth_attempts
```

## Next Steps

1. Open http://127.0.0.1:7000 in your browser
2. Send login attempts and commands
3. Watch the dashboard update in real-time at http://127.0.0.1:5000
4. (Optional) Open DevTools and monitor WebSocket at ws://127.0.0.1:8000/ws/events

🎯 **All attacks are now real-time with NO test files!**
