# 🛡️ Remote Access Honeypot for Threat Analysis

A comprehensive, real-time honeypot system designed to capture, analyze, and visualize cyber attacks targeting remote access services (SSH/RDP). Features include credential harvesting, command logging, session tracking, and an interactive web dashboard with live threat intelligence.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-red.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [System Components](#-system-components)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Dashboard Features](#-dashboard-features)
- [Database Schema](#-database-schema)
- [Security Considerations](#-security-considerations)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## ✨ Features

### Core Honeypot Capabilities
- 🎯 **SSH & RDP Emulation**: Simulates vulnerable SSH (port 2222) and RDP (port 3389) services
- 🔐 **Credential Harvesting**: Captures all authentication attempts with usernames and passwords
- 💻 **Command Logging**: Records all commands executed by attackers in fake shell sessions
- 📊 **Session Tracking**: Monitors complete attacker sessions from connection to disconnection
- 🌐 **Real-Time Monitoring**: WebSocket-based live event streaming
- 🔄 **Attack Pattern Analysis**: Identifies common attack patterns and techniques

### Web Integration
- 🌍 **Vulnerable Website Demo**: Includes frontend and backend websites for testing
- 🔌 **Event Ingestion API**: `/ingest/web` endpoint accepts events from external sources
- 📡 **Real-Time Forwarding**: Captures attacks on demo websites and forwards to honeypot

### Dashboard & Visualization
- 📈 **Interactive Charts**: Real-time graphs showing attack trends, top passwords, commands
- 🗺️ **Geographic Mapping**: (Optional) IP geolocation for attacker origin tracking
- 🎨 **Modern UI**: Beautiful gradient design with responsive layout
- 🗑️ **Data Management**: Clear all data button to reset statistics
- 🔄 **Auto-Refresh**: Automatic updates every 10 seconds

### Data Analysis
- 🔍 **Top Passwords**: Identifies most commonly used passwords
- 👤 **Top Usernames**: Tracks popular username attempts
- ⚙️ **Command Frequency**: Analyzes most executed commands
- 🌐 **IP Intelligence**: Tracks unique attacker IPs and behavior patterns
- 📅 **Attack Timeline**: 24-hour attack distribution visualization

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    ATTACK SOURCES                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Real Attacks │  │ Demo Website │  │ Test Scripts │         │
│  │  SSH/RDP     │  │ (Port 7000)  │  │   (Manual)   │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
└─────────┼──────────────────┼──────────────────┼────────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────┐
│              HONEYPOT BACKEND (Port 8000)                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  FastAPI Application (main_enhanced.py)                  │  │
│  │  • TCP Honeypots (ports 2222, 3389)                     │  │
│  │  • REST API Endpoints                                    │  │
│  │  • WebSocket Event Streaming                            │  │
│  │  • /ingest/web - External Event Receiver                │  │
│  └──────────────────┬───────────────────────────────────────┘  │
└─────────────────────┼───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                   SQLite DATABASE                               │
│  • events           - Raw connection logs                       │
│  • auth_attempts    - Login credentials                         │
│  • commands         - Executed commands                         │
│  • sessions         - Complete attack sessions                  │
│  • ip_intel         - IP geolocation & threat scores            │
└──────────────────────┬──────────────────────────────────────────┘
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
┌──────────────────────┐  ┌──────────────────────┐
│  DASHBOARD (5000)    │  │  BACKEND SITE (9000) │
│  Flask Web UI        │  │  Vulnerable Demo     │
│  • Charts & Graphs   │  │  • /login endpoint   │
│  • Statistics        │  │  • /submit_cmd       │
│  • Real-time Updates │  │  Forwards to 8000    │
└──────────────────────┘  └──────────────────────┘
```

---

## 📁 Project Structure

```
Network-Securitty-Project/
│
├── backend/                          # Main honeypot backend
│   └── app/
│       ├── main_enhanced.py          # FastAPI app with honeypot logic
│       ├── honeypot_enhanced.py      # SSH/RDP protocol emulation
│       ├── db_enhanced.py            # Database operations (SQLite)
│       ├── schemas.py                # Pydantic data models
│       └── analyzer.py               # Attack pattern analysis
│
├── dashboard/                        # Web dashboard
│   ├── app.py                        # Flask application
│   └── templates/
│       └── dashboard.html            # Dashboard UI with Chart.js
│
├── backend_websites/                 # Demo vulnerable website (backend)
│   ├── app.py                        # Flask app with /login, /submit_cmd
│   └── templates/
│       └── index.html                # Backend UI
│
├── frontend_websites/                # Attacker playground (frontend)
│   └── index.html                    # Static HTML with attack forms
│
├── start_enhanced_honeypot.ps1      # Launch honeypot backend
├── start_dashboard.ps1              # Launch dashboard
├── start_websites.ps1               # Launch demo websites
├── launch_system.ps1                # Launch entire system
│
├── honeypot_events.db               # SQLite database (auto-created)
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

---

## 🚀 Installation

### Prerequisites

- **Python 3.9+** (tested on Python 3.13)
- **Windows PowerShell** (for launcher scripts)
- **Git** (for cloning repository)

### Step 1: Clone Repository

```bash
git clone https://github.com/abhinendra9792/Network-Securitty-Project.git
cd Network-Securitty-Project
```

### Step 2: Create Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

**Main Dependencies:**
- `fastapi` - REST API framework
- `uvicorn` - ASGI server
- `aiosqlite` - Async SQLite database
- `flask` - Dashboard web framework
- `flask-cors` - CORS support
- `websockets` - Real-time event streaming
- `requests` - HTTP client

---

## ⚡ Quick Start

### Option 1: Launch Everything at Once

```powershell
.\launch_system.ps1
```

This starts:
- Honeypot backend (port 8000)
- Dashboard (port 5000)
- Demo websites (ports 7000 & 9000)

### Option 2: Launch Components Individually

**Terminal 1 - Start Honeypot:**
```powershell
.\start_enhanced_honeypot.ps1
```

**Terminal 2 - Start Dashboard:**
```powershell
.\start_dashboard.ps1
```

**Terminal 3 - Start Demo Websites:**
```powershell
.\start_websites.ps1
```

### Verify System is Running

```powershell
# Check ports
Test-NetConnection -ComputerName 127.0.0.1 -Port 8000  # Honeypot
Test-NetConnection -ComputerName 127.0.0.1 -Port 5000  # Dashboard
Test-NetConnection -ComputerName 127.0.0.1 -Port 9000  # Backend website
Test-NetConnection -ComputerName 127.0.0.1 -Port 7000  # Frontend website

# Get statistics
Invoke-RestMethod http://127.0.0.1:8000/statistics
```

---

## 🧩 System Components

### 1. Honeypot Backend (`backend/app/main_enhanced.py`)

The core FastAPI application that handles:

**TCP Honeypots:**
- Listens on port 2222 (SSH) and 3389 (RDP)
- Emulates SSH banners and authentication flows
- Captures credentials, commands, and full sessions

**REST API Endpoints:**
```python
GET  /events              # Get recent connection events
GET  /auth_attempts       # Get authentication attempts
GET  /commands            # Get executed commands
GET  /sessions            # Get attacker sessions
GET  /statistics          # Get overall statistics
GET  /ip_intelligence     # Get IP threat data
POST /ingest/web          # Accept events from external sources
```

**WebSocket:**
```python
WS   /ws/events           # Real-time event streaming
```

### 2. Honeypot Protocol Handler (`backend/app/honeypot_enhanced.py`)

Implements SSH/RDP protocol emulation:

```python
async def handle_ssh_connection(reader, writer, event_queue):
    """
    Emulates SSH authentication flow:
    1. Send SSH banner
    2. Read username
    3. Read password
    4. Log auth attempt
    5. Provide fake shell
    6. Log all commands
    7. Track session metrics
    """
```

**Features:**
- Parses SSH protocol handshakes
- Captures multi-line credentials
- Provides interactive fake shell
- Logs command responses
- Tracks session duration

### 3. Database Layer (`backend/app/db_enhanced.py`)

SQLite database with 5 tables:

```python
async def insert_auth_attempt(auth: Dict[str, Any]) -> int:
    """Insert authentication attempt"""
    
async def insert_command(cmd: Dict[str, Any]) -> int:
    """Insert executed command"""
    
async def create_session(session: Dict[str, Any]) -> int:
    """Create new session"""
    
async def get_statistics() -> Dict[str, Any]:
    """Aggregate statistics across all tables"""
```

### 4. Dashboard (`dashboard/app.py`)

Flask web application with Chart.js visualizations:

**Key Endpoints:**
```python
@app.route('/')
def dashboard():
    """Render main dashboard"""

@app.route('/api/statistics')
def get_statistics():
    """Return statistics JSON"""

@app.route('/api/reset_all', methods=['POST'])
def reset_all_data():
    """Clear all database tables"""
```

**Dashboard Features:**
- 6 statistics cards (events, auth, commands, sessions, logins, IPs)
- 6 charts (passwords, usernames, commands, timeline, services, geo)
- 2 data tables (recent sessions, recent commands)
- Auto-refresh every 10 seconds
- Clear all data button

### 5. Demo Websites

**Backend (`backend_websites/app.py`):**
- Vulnerable Flask app on port 9000
- `/login` - Accepts credentials, forwards to honeypot
- `/submit_cmd` - Accepts commands, forwards to honeypot

**Frontend (`frontend_websites/index.html`):**
- Static HTML on port 7000
- Attack playground with forms
- Posts to backend_websites service

---

## 📖 Usage Guide

### Capturing Real Attacks

**Expose Honeypot to Internet (Advanced Users Only):**

⚠️ **WARNING**: Only do this on isolated networks or VMs!

```powershell
# Forward ports on your router/firewall:
# External:22 → Internal:2222 (SSH honeypot)
# External:3389 → Internal:3389 (RDP honeypot)

# Or use ngrok for testing:
ngrok tcp 2222
```

Attacks will be automatically captured and logged.

### Testing with Demo Websites

**Browser Method:**
1. Open http://127.0.0.1:7000
2. Enter any username/password
3. Click "Send"
4. View results at http://127.0.0.1:5000

**PowerShell Method:**
```powershell
# Send login attempt
Invoke-RestMethod -Uri http://127.0.0.1:9000/login -Method Post `
  -Body (@{username='hacker';password='test123'} | ConvertTo-Json) `
  -ContentType 'application/json'

# Send command
Invoke-RestMethod -Uri http://127.0.0.1:9000/submit_cmd -Method Post `
  -Body (@{session_id='test-1';command='whoami'} | ConvertTo-Json) `
  -ContentType 'application/json'
```

### Direct Honeypot Testing

**SSH Test (Port 2222):**
```powershell
# Using PowerShell
$c = New-Object System.Net.Sockets.TcpClient('127.0.0.1', 2222)
$s = $c.GetStream()
$w = New-Object System.IO.StreamWriter($s)

# Send username
$w.WriteLine('root')
$w.Flush()
Start-Sleep -Milliseconds 300

# Send password
$w.WriteLine('password123')
$w.Flush()
Start-Sleep -Milliseconds 300

# Send commands
$w.WriteLine('ls -la')
$w.Flush()
$w.WriteLine('cat /etc/passwd')
$w.Flush()

$w.Close()
$s.Close()
$c.Close()
```

**Using External Tools:**
```bash
# Using netcat (Linux/Mac)
nc 127.0.0.1 2222

# Using PuTTY (Windows)
# Connect to: 127.0.0.1:2222
```

### WebSocket Monitoring

**Python WebSocket Client:**
```python
import asyncio
import websockets

async def monitor():
    uri = "ws://127.0.0.1:8000/ws/events"
    async with websockets.connect(uri) as ws:
        print("Connected to honeypot websocket")
        async for message in ws:
            print(f"Event: {message}")

asyncio.run(monitor())
```

---

## 📡 API Documentation

### GET /statistics

Returns comprehensive attack statistics.

**Response:**
```json
{
  "total_events": 150,
  "total_auth_attempts": 45,
  "total_commands": 30,
  "total_sessions": 12,
  "top_passwords": [
    {"password": "admin123", "count": 8},
    {"password": "root", "count": 6}
  ],
  "top_usernames": [
    {"username": "admin", "count": 15},
    {"username": "root", "count": 12}
  ],
  "top_commands": [
    {"command": "whoami", "count": 10},
    {"command": "ls -la", "count": 8}
  ],
  "top_attacker_ips": [
    {"src_ip": "192.168.1.100", "count": 25}
  ]
}
```

### POST /ingest/web

Accept events from external sources (websites, scripts, etc).

**Request Body:**
```json
{
  "type": "auth",
  "payload": {
    "src_ip": "10.0.0.5",
    "username": "admin",
    "password": "password123",
    "service": "web",
    "success": false
  }
}
```

**Event Types:**
- `auth` - Authentication attempt
- `command` - Command execution
- `session` - Session creation
- `event` - Generic event

**Response:**
```json
{
  "status": "ok"
}
```

### GET /auth_attempts?limit=100

Returns recent authentication attempts.

**Response:**
```json
[
  {
    "id": 1,
    "ts": "2025-11-19T10:30:00Z",
    "src_ip": "192.168.1.100",
    "username": "admin",
    "password": "admin123",
    "success": false,
    "service": "ssh",
    "session_id": "abc123"
  }
]
```

### GET /commands?limit=100

Returns recently executed commands.

### GET /sessions?limit=50

Returns attacker session data.

### WS /ws/events

WebSocket endpoint for real-time event streaming. Pushes JSON events as they occur.

---

## 📊 Dashboard Features

### Statistics Cards

1. **Total Events** - All captured connections
2. **Auth Attempts** - Login attempts (successful + failed)
3. **Commands Executed** - Total commands run
4. **Attacker Sessions** - Unique sessions tracked
5. **Successful Logins** - Successful auth count
6. **Unique IPs** - Distinct attacker IP addresses

### Charts

1. **Top 10 Passwords** - Most common passwords attempted
2. **Top 10 Usernames** - Most targeted usernames
3. **Top Commands** - Most executed commands
4. **Attack Timeline** - 24-hour attack distribution
5. **Service Distribution** - SSH vs RDP traffic
6. **Geographic Map** - (Optional) Attacker origins

### Data Tables

1. **Recent Attacker Sessions** - Session details with duration, commands
2. **Recent Commands Executed** - Command log with timestamps

### Controls

- **🔄 Refresh Data** - Manually refresh dashboard
- **🗑️ Clear All Data** - Reset database (with confirmation)
- **Auto-refresh** - Updates every 10 seconds

---

## 🗄️ Database Schema

### Table: `events`

Raw connection logs.

```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,              -- ISO timestamp
    src_ip TEXT,                   -- Attacker IP
    src_port INTEGER,              -- Attacker port
    dest_port INTEGER,             -- Honeypot port (2222/3389)
    protocol TEXT,                 -- SSH/RDP
    payload_preview TEXT           -- Raw data preview
);
```

### Table: `auth_attempts`

Authentication attempts with credentials.

```sql
CREATE TABLE auth_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    src_ip TEXT NOT NULL,
    username TEXT,                 -- Captured username
    password TEXT,                 -- Captured password
    success BOOLEAN DEFAULT 0,     -- Auth result
    service TEXT,                  -- ssh/rdp/web
    session_id TEXT                -- Associated session
);
```

### Table: `commands`

Commands executed in fake shells.

```sql
CREATE TABLE commands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    session_id TEXT NOT NULL,
    src_ip TEXT NOT NULL,
    command TEXT NOT NULL,         -- Command text
    response TEXT                  -- Fake response
);
```

### Table: `sessions`

Complete attacker sessions.

```sql
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT UNIQUE NOT NULL,
    src_ip TEXT NOT NULL,
    src_port INTEGER,
    start_time TEXT NOT NULL,
    end_time TEXT,
    duration_seconds INTEGER,
    auth_attempts INTEGER DEFAULT 0,
    commands_count INTEGER DEFAULT 0,
    success_login BOOLEAN DEFAULT 0
);
```

### Table: `ip_intel`

IP geolocation and threat intelligence.

```sql
CREATE TABLE ip_intel (
    ip TEXT PRIMARY KEY,
    country TEXT,
    city TEXT,
    isp TEXT,
    threat_score INTEGER DEFAULT 0,
    last_seen TEXT,
    total_attacks INTEGER DEFAULT 1,
    is_tor BOOLEAN DEFAULT 0,
    is_vpn BOOLEAN DEFAULT 0
);
```

---

## 🔒 Security Considerations

### ⚠️ Important Warnings

1. **Isolated Environment**: Run honeypot on isolated networks or VMs
2. **No Sensitive Data**: Never run on production systems with real data
3. **Firewall Rules**: Properly configure firewalls to prevent lateral movement
4. **Log Monitoring**: Regularly review logs for suspicious patterns
5. **Legal Compliance**: Ensure compliance with local laws regarding honeypots

### Recommended Setup

```
Internet
    ↓
Firewall (Port forwarding: 22→2222, 3389→3389)
    ↓
DMZ / Isolated VLAN
    ↓
Honeypot VM (No sensitive data, no network access to internal systems)
```

### Best Practices

- Use dedicated VM or container
- Disable outbound internet on honeypot
- Monitor honeypot system for compromise
- Regularly backup and analyze captured data
- Don't expose real credentials or systems
- Consider using Docker for additional isolation

---

## 🐛 Troubleshooting

### Port Already in Use

```powershell
# Find process using port
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess

# Kill process
Stop-Process -Id <PID> -Force
```

### Database Locked

```powershell
# Stop all services
Get-Process python | Stop-Process -Force

# Delete database (will be recreated)
Remove-Item honeypot_events.db
```

### Dashboard Shows No Data

1. Ensure honeypot backend is running (port 8000)
2. Click "Refresh Data" button
3. Check that database has data:
```powershell
sqlite3 honeypot_events.db "SELECT COUNT(*) FROM auth_attempts;"
```

### WebSocket Connection Failed

- Check firewall allows port 8000
- Ensure honeypot backend is running
- Try different WebSocket client

### Import Errors

```powershell
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Development Setup

```powershell
# Install dev dependencies
pip install -r requirements.txt

# Run tests (if available)
pytest

# Format code
black backend/ dashboard/
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python API framework
- [Flask](https://flask.palletsprojects.com/) - Lightweight web framework
- [Chart.js](https://www.chartjs.org/) - Beautiful JavaScript charts
- [Cowrie](https://github.com/cowrie/cowrie) - SSH/Telnet honeypot inspiration

---

## 📬 Contact

**Author**: Abhinendra  
**GitHub**: [@abhinendra9792](https://github.com/abhinendra9792)  
**Repository**: [Network-Securitty-Project](https://github.com/abhinendra9792/Network-Securitty-Project)

---

## 🎯 Project Goals

This honeypot system was designed to:

1. **Learn**: Understand real-world cyber attack patterns
2. **Research**: Collect data on attacker behavior and techniques
3. **Detect**: Identify common credentials and exploit attempts
4. **Analyze**: Study attack timelines and geographic distributions
5. **Educate**: Demonstrate security concepts in action

---

## 🚀 Future Enhancements

- [ ] Add email/Slack alerts for new attacks
- [ ] Implement machine learning for attack classification
- [ ] Add more protocol emulations (FTP, SMTP, HTTP)
- [ ] Integrate with threat intelligence feeds (AbuseIPDB, VirusTotal)
- [ ] Add session replay functionality
- [ ] Export data to CSV/JSON
- [ ] Docker containerization
- [ ] Kubernetes deployment manifests
- [ ] Advanced geolocation with maps
- [ ] MITRE ATT&CK framework mapping

---

## ⭐ Star History

If you find this project useful, please consider giving it a star on GitHub!

---

**Built with ❤️ for cybersecurity research and education**
