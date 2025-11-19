# 🛡️ Enhanced Remote Access Honeypot for Threat Analysis

## Complete Cybersecurity Research Platform

This project implements a **fully-featured honeypot system** inspired by Cowrie, designed to capture and analyze unauthorized remote access attempts. It emulates SSH/Telnet and RDP services to study attacker behavior, common attack patterns, and credential stuffing attempts.

---

## 🎯 Project Features

### Core Honeypot Capabilities
- ✅ **SSH Protocol Emulation** - Mimics OpenSSH 8.2 server behavior
- ✅ **RDP Protocol Emulation** - Captures Windows Remote Desktop attacks
- ✅ **Credential Capture** - Records all username/password attempts
- ✅ **Command Logging** - Tracks every command attackers try to execute
- ✅ **Session Tracking** - Full session replay and forensics
- ✅ **Fake Shell Environment** - Responds to common Linux commands
- ✅ **Real-Time Event Streaming** - WebSocket-based live updates

### Analysis & Intelligence
- ✅ **Attack Pattern Analysis** - Identifies brute force, scanning, exploitation
- ✅ **Credential Analysis** - Top passwords, usernames, combos
- ✅ **Command Analysis** - Most executed commands, malware downloads
- ✅ **IP Intelligence** - Geolocation, ISP, threat scoring
- ✅ **Behavioral Analytics** - Session duration, persistence, tactics

### Visualization & Dashboard
- ✅ **Flask-Based Web Dashboard** - Beautiful, interactive UI
- ✅ **Real-Time Charts** - Attack timeline, service distribution
- ✅ **Statistical Analysis** - Comprehensive threat metrics
- ✅ **Top 10 Lists** - Passwords, usernames, commands, IPs
- ✅ **Session Browser** - Review attacker sessions
- ✅ **Export Functionality** - CSV/JSON data export

---

## 🏗️ Project Structure

```
Network-Securitty-Project/
├── backend/
│   ├── app/
│   │   ├── main_enhanced.py         # Enhanced FastAPI application
│   │   ├── honeypot_enhanced.py     # SSH/RDP emulation engine
│   │   ├── db_enhanced.py           # Enhanced database layer
│   │   └── schemas.py               # Pydantic models
│   ├── monitor_websocket.py         # Real-time WebSocket monitor
│   └── requirements.txt             # Python dependencies
│
├── dashboard/
│   ├── app.py                       # Flask dashboard application
│   ├── templates/
│   │   └── dashboard.html           # Interactive web dashboard
│   └── requirements.txt             # Flask dependencies
│
├── honeypot_events.db               # SQLite database (auto-created)
│
├── start_enhanced_honeypot.ps1      # Start honeypot backend
├── start_dashboard.ps1              # Start Flask dashboard
├── test_advanced_attacks.ps1        # Comprehensive attack simulator
│
└── Documentation/
    ├── HONEYPOT_GUIDE.md
    ├── REALTIME_MONITORING.md
    └── REALTIME_CONFIRMED.md
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+ installed
- Windows PowerShell
- Network access for testing

### Step 1: Install Dependencies

```powershell
# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install backend dependencies
pip install -r backend/requirements.txt

# Install dashboard dependencies
pip install -r dashboard/requirements.txt
```

### Step 2: Start the Honeypot Backend

Open **PowerShell Terminal 1**:
```powershell
.\start_enhanced_honeypot.ps1
```

This starts:
- SSH honeypot on port **2222**
- RDP honeypot on port **3389**
- FastAPI backend on port **8000**

### Step 3: Start the Dashboard

Open **PowerShell Terminal 2**:
```powershell
.\start_dashboard.ps1
```

This starts the Flask dashboard on **http://127.0.0.1:5000**

### Step 4: Simulate Attacks

Open **PowerShell Terminal 3**:
```powershell
.\test_advanced_attacks.ps1
```

This simulates:
- SSH brute force attacks
- RDP login attempts
- Command execution
- Multi-stage attacks

### Step 5: View Results

Open your browser:
- **Dashboard**: http://127.0.0.1:5000
- **API**: http://127.0.0.1:8000/statistics

---

## 📊 Dashboard Features

### Real-Time Statistics
- Total events captured
- Authentication attempts
- Commands executed
- Unique attacker IPs
- Session count
- Success rate

### Interactive Charts
1. **Attack Timeline** - 24-hour attack frequency
2. **Service Distribution** - SSH vs RDP vs Other
3. **Top 10 Passwords** - Most common password attempts
4. **Top 10 Usernames** - Most targeted usernames
5. **Top 10 Commands** - Most executed commands
6. **Top Attacker IPs** - Most active attackers

### Data Tables
- **Recent Sessions** - Live attacker session history
- **Recent Commands** - Real-time command execution log
- **Geo Intelligence** - Geographic attack origins
- **Threat Scores** - Risk assessment per IP

---

## 🔌 API Endpoints

### Authentication & Credentials
```
GET /auth_attempts?limit=100
```
Returns all captured username/password attempts

### Commands
```
GET /commands?limit=100
```
Returns all executed commands with responses

### Sessions
```
GET /sessions?limit=50
```
Returns attacker session metadata

### Statistics
```
GET /statistics
```
Returns comprehensive attack statistics

### WebSocket (Real-Time)
```
ws://127.0.0.1:8000/ws/events
```
Live event stream for real-time monitoring

---

## 🧪 Testing Attack Scenarios

### Manual SSH Test
```powershell
# Connect to SSH honeypot
$client = New-Object System.Net.Sockets.TcpClient('127.0.0.1',2222)
$stream = $client.GetStream()

# Send credentials
$bytes = [System.Text.Encoding]::UTF8.GetBytes('root:password123')
$stream.Write($bytes,0,$bytes.Length)

# Send command
Start-Sleep -Seconds 1
$cmd = [System.Text.Encoding]::UTF8.GetBytes('whoami')
$stream.Write($cmd,0,$cmd.Length)

$stream.Close()
$client.Close()
```

### Manual RDP Test
```powershell
$client = New-Object System.Net.Sockets.TcpClient('127.0.0.1',3389)
$stream = $client.GetStream()
$bytes = [System.Text.Encoding]::UTF8.GetBytes('Administrator:Passw0rd!')
$stream.Write($bytes,0,$bytes.Length)
$stream.Close()
$client.Close()
```

---

## 📈 Research & Analysis Use Cases

### 1. Password Analysis
- Identify most common passwords used in attacks
- Analyze password patterns and complexity
- Create custom wordlists for security testing

### 2. Attack Pattern Recognition
- Detect brute force patterns
- Identify automated tools (Metasploit, Hydra, etc.)
- Classify attack types (recon, exploitation, persistence)

### 3. Attacker Behavior Study
- Session duration analysis
- Command sequence patterns
- Post-exploitation activities
- Malware download attempts

### 4. Threat Intelligence
- Identify malicious IP ranges
- Track persistent threat actors
- Correlate attacks across time periods
- Geographic attack distribution

### 5. Network Defense
- Early warning system for attacks
- Signature development for IDS/IPS
- Security awareness training material
- Vulnerability assessment insights

---

## 🗄️ Database Schema

### Events Table
```sql
- id, ts, src_ip, src_port, dest_port, protocol, payload_preview
```

### Auth_Attempts Table
```sql
- id, ts, src_ip, username, password, success, service, session_id
```

### Commands Table
```sql
- id, ts, session_id, src_ip, command, response
```

### Sessions Table
```sql
- id, session_id, src_ip, src_port, start_time, end_time,
  duration_seconds, auth_attempts, commands_count, success_login
```

### IP_Intel Table
```sql
- ip, country, city, isp, threat_score, last_seen,
  total_attacks, is_tor, is_vpn
```

---

## 🔒 Security Best Practices

⚠️ **WARNING**: Only deploy honeypots in isolated environments!

### Deployment Guidelines
1. **Isolation**: Use separate VM/container
2. **Network Segmentation**: Isolated VLAN
3. **No Sensitive Data**: Never use real credentials
4. **Monitor Resource Usage**: Prevent DoS
5. **Legal Compliance**: Check local laws
6. **Rate Limiting**: Implement on API endpoints
7. **Log Rotation**: Manage disk space

### Production Checklist
- [ ] Deploy in DMZ or isolated network
- [ ] Implement firewall rules
- [ ] Enable log aggregation (SIEM)
- [ ] Set up alerting (email/Slack)
- [ ] Regular backup of database
- [ ] Monitor system resources
- [ ] Review captured data regularly

---

## 🚀 Advanced Features (Roadmap)

### Phase 1 (Current) ✅
- SSH/RDP emulation
- Credential capture
- Command logging
- Flask dashboard
- Real-time monitoring

### Phase 2 (Next)
- [ ] IP Geolocation API integration (ipapi.co)
- [ ] Machine Learning attack classification
- [ ] Advanced protocol emulation (HTTP, FTP, Telnet)
- [ ] Session replay video generation
- [ ] Automated threat reports (PDF export)

### Phase 3 (Future)
- [ ] Multi-honeypot orchestration
- [ ] Threat intelligence feed integration
- [ ] Advanced behavioral analysis
- [ ] Honeypot network (distributed)
- [ ] AI-powered attack prediction

---

## 📚 Educational Value

This project demonstrates:
- **Network Security**: Understanding attack vectors
- **Protocol Analysis**: SSH/RDP internals
- **Python Programming**: Async I/O, web frameworks
- **Database Design**: Schema optimization
- **Data Visualization**: Chart.js, interactive dashboards
- **Threat Intelligence**: IOC collection and analysis
- **Defensive Security**: Attack surface understanding

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional protocol emulation
- Enhanced fake shell responses
- Machine learning models
- Geographic visualization maps
- Advanced forensics tools

---

## 📜 License

MIT License - Educational and research purposes only

---

## 📞 Support & Documentation

- **Dashboard**: http://127.0.0.1:5000
- **API Docs**: http://127.0.0.1:8000/docs
- **GitHub**: Network-Securitty-Project
- **Issues**: Report bugs via GitHub Issues

---

## 🎓 Academic Citations

If using for research, please cite:
```
Enhanced Remote Access Honeypot for Threat Analysis
Network-Securitty-Project
2025
```

---

**Built with ❤️ for Cybersecurity Research and Education**

**⚡ Real-Time | 📊 Data-Driven | 🛡️ Security-Focused**
