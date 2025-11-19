import os
import aiosqlite
import asyncio
from typing import Dict, Any, List
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "./honeypot_events.db")

_init_lock = asyncio.Lock()

async def init_db() -> None:
    async with _init_lock:
        async with aiosqlite.connect(DB_PATH) as db:
            # Original events table
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts TEXT NOT NULL,
                    src_ip TEXT,
                    src_port INTEGER,
                    dest_port INTEGER,
                    protocol TEXT,
                    payload_preview TEXT
                )
                """
            )
            
            # Authentication attempts table
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS auth_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts TEXT NOT NULL,
                    src_ip TEXT NOT NULL,
                    username TEXT,
                    password TEXT,
                    success BOOLEAN DEFAULT 0,
                    service TEXT,
                    session_id TEXT
                )
                """
            )
            
            # Commands executed table
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS commands (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    src_ip TEXT NOT NULL,
                    command TEXT NOT NULL,
                    response TEXT
                )
                """
            )
            
            # Sessions table
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
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
                )
                """
            )
            
            # IP intelligence table
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS ip_intel (
                    ip TEXT PRIMARY KEY,
                    country TEXT,
                    city TEXT,
                    isp TEXT,
                    threat_score INTEGER DEFAULT 0,
                    last_seen TEXT,
                    total_attacks INTEGER DEFAULT 1,
                    is_tor BOOLEAN DEFAULT 0,
                    is_vpn BOOLEAN DEFAULT 0
                )
                """
            )
            
            await db.commit()

async def insert_event(event: Dict[str, Any]) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO events (ts, src_ip, src_port, dest_port, protocol, payload_preview) VALUES (?, ?, ?, ?, ?, ?)",
            (event.get("ts"), event.get("src_ip"), event.get("src_port"), event.get("dest_port"), event.get("protocol"), event.get("payload_preview")),
        )
        await db.commit()
        return cur.lastrowid or 0

async def insert_auth_attempt(auth: Dict[str, Any]) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO auth_attempts (ts, src_ip, username, password, success, service, session_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (auth.get("ts"), auth.get("src_ip"), auth.get("username"), auth.get("password"), auth.get("success", False), auth.get("service"), auth.get("session_id")),
        )
        await db.commit()
        return cur.lastrowid or 0

async def insert_command(cmd: Dict[str, Any]) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO commands (ts, session_id, src_ip, command, response) VALUES (?, ?, ?, ?, ?)",
            (cmd.get("ts"), cmd.get("session_id"), cmd.get("src_ip"), cmd.get("command"), cmd.get("response")),
        )
        await db.commit()
        return cur.lastrowid or 0

async def create_session(session: Dict[str, Any]) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO sessions (session_id, src_ip, src_port, start_time) VALUES (?, ?, ?, ?)",
            (session.get("session_id"), session.get("src_ip"), session.get("src_port"), session.get("start_time")),
        )
        await db.commit()
        return cur.lastrowid or 0

async def update_session(session_id: str, updates: Dict[str, Any]) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [session_id]
        await db.execute(f"UPDATE sessions SET {set_clause} WHERE session_id = ?", values)
        await db.commit()

async def upsert_ip_intel(ip: str, data: Dict[str, Any]) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO ip_intel (ip, country, city, isp, threat_score, last_seen, total_attacks, is_tor, is_vpn)
            VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?)
            ON CONFLICT(ip) DO UPDATE SET
                last_seen = excluded.last_seen,
                total_attacks = total_attacks + 1,
                threat_score = excluded.threat_score
            """,
            (ip, data.get("country"), data.get("city"), data.get("isp"), data.get("threat_score", 0), 
             datetime.utcnow().isoformat() + "Z", data.get("is_tor", False), data.get("is_vpn", False))
        )
        await db.commit()

async def fetch_events(limit: int = 50) -> List[Dict[str, Any]]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM events ORDER BY id DESC LIMIT ?", (limit,))
        rows = await cur.fetchall()
        return [dict(r) for r in rows]

async def fetch_auth_attempts(limit: int = 100) -> List[Dict[str, Any]]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM auth_attempts ORDER BY id DESC LIMIT ?", (limit,))
        rows = await cur.fetchall()
        return [dict(r) for r in rows]

async def fetch_commands(limit: int = 100) -> List[Dict[str, Any]]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM commands ORDER BY id DESC LIMIT ?", (limit,))
        rows = await cur.fetchall()
        return [dict(r) for r in rows]

async def fetch_sessions(limit: int = 50) -> List[Dict[str, Any]]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM sessions ORDER BY id DESC LIMIT ?", (limit,))
        rows = await cur.fetchall()
        return [dict(r) for r in rows]

async def get_statistics() -> Dict[str, Any]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        
        # Total counts
        total_events = (await db.execute("SELECT COUNT(*) as cnt FROM events")).fetchone()
        total_auth = (await db.execute("SELECT COUNT(*) as cnt FROM auth_attempts")).fetchone()
        total_commands = (await db.execute("SELECT COUNT(*) as cnt FROM commands")).fetchone()
        total_sessions = (await db.execute("SELECT COUNT(*) as cnt FROM sessions")).fetchone()
        
        # Top passwords
        top_passwords = await db.execute(
            "SELECT password, COUNT(*) as count FROM auth_attempts WHERE password IS NOT NULL GROUP BY password ORDER BY count DESC LIMIT 10"
        )
        passwords = await top_passwords.fetchall()
        
        # Top usernames
        top_users = await db.execute(
            "SELECT username, COUNT(*) as count FROM auth_attempts WHERE username IS NOT NULL GROUP BY username ORDER BY count DESC LIMIT 10"
        )
        usernames = await top_users.fetchall()
        
        # Top commands
        top_cmds = await db.execute(
            "SELECT command, COUNT(*) as count FROM commands GROUP BY command ORDER BY count DESC LIMIT 10"
        )
        commands = await top_cmds.fetchall()
        
        # Top attacking IPs
        top_ips = await db.execute(
            "SELECT src_ip, COUNT(*) as count FROM events GROUP BY src_ip ORDER BY count DESC LIMIT 10"
        )
        ips = await top_ips.fetchall()
        
        total_events_row = await total_events
        total_auth_row = await total_auth
        total_commands_row = await total_commands
        total_sessions_row = await total_sessions
        
        return {
            "total_events": total_events_row["cnt"] if total_events_row else 0,
            "total_auth_attempts": total_auth_row["cnt"] if total_auth_row else 0,
            "total_commands": total_commands_row["cnt"] if total_commands_row else 0,
            "total_sessions": total_sessions_row["cnt"] if total_sessions_row else 0,
            "top_passwords": [dict(r) for r in passwords],
            "top_usernames": [dict(r) for r in usernames],
            "top_commands": [dict(r) for r in commands],
            "top_attacker_ips": [dict(r) for r in ips]
        }

async def fetch_ip_intel(limit: int = 100) -> List[Dict[str, Any]]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM ip_intel ORDER BY total_attacks DESC LIMIT ?", (limit,))
        rows = await cur.fetchall()
        return [dict(r) for r in rows]
