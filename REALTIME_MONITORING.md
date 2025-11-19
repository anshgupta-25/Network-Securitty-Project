# 🔴 REAL-TIME THREAT MONITORING GUIDE

Your honeypot has **3 ways** to monitor threats in real-time!

---

## ⚡ Option 1: Real-Time PowerShell Monitor (Recommended)

**Continuously polls the API and shows new threats instantly**

### How to Run:
```powershell
.\monitor_realtime.ps1
```

### What You'll See:
- New threats appear automatically every 2 seconds
- Color-coded threat information
- Service identification (SSH/RDP)
- Payload preview
- Press CTRL+C to stop

---

## 🔌 Option 2: WebSocket Real-Time Monitor (Instant)

**Connects via WebSocket and receives threats the moment they happen**

### How to Run:
```powershell
& "D:/Network Securitty Project/.venv/Scripts/python.exe" backend/monitor_websocket.py
```

### Advantages:
- **Instant notifications** (no polling delay)
- Lower resource usage
- True real-time streaming
- System beep alerts on each threat

---

## 🌐 Option 3: Browser Real-Time (Manual Refresh)

Open in your browser and manually refresh:
```
http://127.0.0.1:8000/events
```

Or use browser console for auto-refresh:
```javascript
// Run in browser console (F12)
setInterval(() => {
    fetch('http://127.0.0.1:8000/events?limit=10')
        .then(r => r.json())
        .then(data => console.table(data));
}, 3000);
```

---

## 🧪 Test Real-Time Monitoring

### Terminal 1: Start Honeypot
```powershell
.\start_honeypot.ps1
```

### Terminal 2: Start Real-Time Monitor
```powershell
.\monitor_realtime.ps1
```

### Terminal 3: Send Test Attacks
```powershell
# Attack 1
$c = New-Object System.Net.Sockets.TcpClient('127.0.0.1',2222)
$s = $c.GetStream()
$s.Write([System.Text.Encoding]::UTF8.GetBytes('HACK-TEST'),0,9)
$s.Close(); $c.Close()

# Wait 3 seconds, then send another
Start-Sleep -Seconds 3

# Attack 2
$c = New-Object System.Net.Sockets.TcpClient('127.0.0.1',3389)
$s = $c.GetStream()
$s.Write([System.Text.Encoding]::UTF8.GetBytes('RDP-ATTACK'),0,10)
$s.Close(); $c.Close()
```

**You'll see threats appear in Terminal 2 in real-time!** 🔥

---

## 📊 Real-Time Dashboard (Future Enhancement)

Want a visual dashboard? Consider building:
- React/Vue.js frontend
- Chart.js for graphs
- WebSocket connection for live updates
- Geolocation map of attacks

---

## ⚙️ Customize Monitoring

### Change Poll Interval (monitor_realtime.ps1)
Edit line 55:
```powershell
Start-Sleep -Seconds 2  # Change to 1 for faster, 5 for slower
```

### Enable Sound Alerts
Uncomment line 44 in monitor_realtime.ps1:
```powershell
[Console]::Beep(1000, 200)
```

### Filter by Port
Add to monitor_realtime.ps1 after line 17:
```powershell
$newEvents = $newEvents | Where-Object { $_.dest_port -eq 2222 }  # Only SSH
```

---

## 🚀 Production Real-Time Monitoring

For production deployments, consider:

1. **Log Aggregation**: Forward to ELK Stack, Splunk, or Graylog
2. **SIEM Integration**: Send events to SIEM platforms
3. **Alerting**: Email/Slack notifications on suspicious patterns
4. **Metrics**: Prometheus + Grafana for visualization
5. **Machine Learning**: Anomaly detection on attack patterns

---

## ✅ Summary

Your honeypot **ALREADY MONITORS IN REAL-TIME**:

✅ Events captured instantly as connections arrive
✅ WebSocket endpoint streams threats live
✅ REST API for polling-based monitoring
✅ All attacks logged with timestamps
✅ Database persists all events for analysis

**Choose your preferred monitoring method and start watching threats roll in!** 🛡️
