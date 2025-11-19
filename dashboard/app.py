"""
Flask Dashboard for Honeypot Threat Analysis
Provides web UI with charts, statistics, and real-time monitoring
"""
from flask import Flask, render_template, jsonify
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime, timedelta
from collections import Counter

app = Flask(__name__)
CORS(app)

DB_PATH = os.getenv("DB_PATH", "./honeypot_events.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/statistics')
def get_statistics():
    """Get overall statistics"""
    conn = get_db()
    cur = conn.cursor()
    
    # Total counts
    total_events = cur.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    total_auth = cur.execute("SELECT COUNT(*) FROM auth_attempts").fetchone()[0]
    total_commands = cur.execute("SELECT COUNT(*) FROM commands").fetchone()[0]
    total_sessions = cur.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
    
    # Successful logins
    successful_logins = cur.execute("SELECT COUNT(*) FROM sessions WHERE success_login = 1").fetchone()[0]
    
    # Unique IPs
    unique_ips = cur.execute("SELECT COUNT(DISTINCT src_ip) FROM events").fetchone()[0]
    
    conn.close()
    
    return jsonify({
        "total_events": total_events,
        "total_auth_attempts": total_auth,
        "total_commands": total_commands,
        "total_sessions": total_sessions,
        "successful_logins": successful_logins,
        "unique_attacker_ips": unique_ips
    })

@app.route('/api/top_passwords')
def get_top_passwords():
    """Get most common passwords"""
    conn = get_db()
    cur = conn.cursor()
    
    passwords = cur.execute("""
        SELECT password, COUNT(*) as count 
        FROM auth_attempts 
        WHERE password IS NOT NULL AND password != ''
        GROUP BY password 
        ORDER BY count DESC 
        LIMIT 20
    """).fetchall()
    
    conn.close()
    
    return jsonify([{"password": row["password"], "count": row["count"]} for row in passwords])

@app.route('/api/top_usernames')
def get_top_usernames():
    """Get most common usernames"""
    conn = get_db()
    cur = conn.cursor()
    
    usernames = cur.execute("""
        SELECT username, COUNT(*) as count 
        FROM auth_attempts 
        WHERE username IS NOT NULL AND username != ''
        GROUP BY username 
        ORDER BY count DESC 
        LIMIT 20
    """).fetchall()
    
    conn.close()
    
    return jsonify([{"username": row["username"], "count": row["count"]} for row in usernames])

@app.route('/api/top_commands')
def get_top_commands():
    """Get most executed commands"""
    conn = get_db()
    cur = conn.cursor()
    
    commands = cur.execute("""
        SELECT command, COUNT(*) as count 
        FROM commands 
        GROUP BY command 
        ORDER BY count DESC 
        LIMIT 20
    """).fetchall()
    
    conn.close()
    
    return jsonify([{"command": row["command"], "count": row["count"]} for row in commands])

@app.route('/api/top_ips')
def get_top_ips():
    """Get top attacker IPs"""
    conn = get_db()
    cur = conn.cursor()
    
    ips = cur.execute("""
        SELECT src_ip, COUNT(*) as count 
        FROM events 
        GROUP BY src_ip 
        ORDER BY count DESC 
        LIMIT 20
    """).fetchall()
    
    conn.close()
    
    return jsonify([{"ip": row["src_ip"], "count": row["count"]} for row in ips])

@app.route('/api/attack_timeline')
def get_attack_timeline():
    """Get attack timeline (last 24 hours by hour)"""
    conn = get_db()
    cur = conn.cursor()
    
    timeline = cur.execute("""
        SELECT 
            strftime('%Y-%m-%d %H:00:00', ts) as hour,
            COUNT(*) as count
        FROM events
        WHERE ts >= datetime('now', '-24 hours')
        GROUP BY hour
        ORDER BY hour
    """).fetchall()
    
    conn.close()
    
    return jsonify([{"hour": row["hour"], "count": row["count"]} for row in timeline])

@app.route('/api/service_distribution')
def get_service_distribution():
    """Get distribution of attacked services"""
    conn = get_db()
    cur = conn.cursor()
    
    services = cur.execute("""
        SELECT 
            CASE 
                WHEN dest_port = 2222 THEN 'SSH'
                WHEN dest_port = 3389 THEN 'RDP'
                ELSE 'Other'
            END as service,
            COUNT(*) as count
        FROM events
        GROUP BY service
    """).fetchall()
    
    conn.close()
    
    return jsonify([{"service": row["service"], "count": row["count"]} for row in services])

@app.route('/api/recent_sessions')
def get_recent_sessions():
    """Get recent attacker sessions"""
    conn = get_db()
    cur = conn.cursor()
    
    sessions = cur.execute("""
        SELECT * FROM sessions 
        ORDER BY start_time DESC 
        LIMIT 50
    """).fetchall()
    
    conn.close()
    
    return jsonify([dict(row) for row in sessions])

@app.route('/api/recent_commands')
def get_recent_commands():
    """Get recently executed commands"""
    conn = get_db()
    cur = conn.cursor()
    
    commands = cur.execute("""
        SELECT * FROM commands 
        ORDER BY ts DESC 
        LIMIT 100
    """).fetchall()
    
    conn.close()
    
    return jsonify([dict(row) for row in commands])

@app.route('/api/geographic_data')
def get_geographic_data():
    """Get geographic distribution of attacks"""
    conn = get_db()
    cur = conn.cursor()
    
    geo_data = cur.execute("""
        SELECT country, city, COUNT(*) as count, MAX(total_attacks) as total_attacks
        FROM ip_intel
        WHERE country IS NOT NULL
        GROUP BY country, city
        ORDER BY count DESC
        LIMIT 50
    """).fetchall()
    
    conn.close()
    
    return jsonify([dict(row) for row in geo_data])

@app.route('/api/threat_intelligence')
def get_threat_intelligence():
    """Get threat intelligence data"""
    conn = get_db()
    cur = conn.cursor()
    
    intel = cur.execute("""
        SELECT * FROM ip_intel 
        ORDER BY threat_score DESC, total_attacks DESC 
        LIMIT 50
    """).fetchall()
    
    conn.close()
    
    return jsonify([dict(row) for row in intel])

@app.route('/api/reset_all', methods=['POST'])
def reset_all_data():
    """Reset/Clear all data from all tables"""
    try:
        conn = get_db()
        cur = conn.cursor()
        
        # Clear all tables
        cur.execute("DELETE FROM events")
        cur.execute("DELETE FROM auth_attempts")
        cur.execute("DELETE FROM commands")
        cur.execute("DELETE FROM sessions")
        cur.execute("DELETE FROM ip_intel")
        
        # Reset autoincrement counters
        cur.execute("DELETE FROM sqlite_sequence WHERE name='events'")
        cur.execute("DELETE FROM sqlite_sequence WHERE name='auth_attempts'")
        cur.execute("DELETE FROM sqlite_sequence WHERE name='commands'")
        cur.execute("DELETE FROM sqlite_sequence WHERE name='sessions'")
        
        conn.commit()
        conn.close()
        
        return jsonify({"status": "success", "message": "All data cleared successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  HONEYPOT THREAT ANALYSIS DASHBOARD")
    print("="*60)
    print(f"  Dashboard URL: http://127.0.0.1:5000")
    print(f"  Database: {DB_PATH}")
    print("="*60 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
