import os
import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from typing import List
from fastapi import Request
from datetime import datetime

from . import db_enhanced as db
from .honeypot_enhanced import start_enhanced_honeypot

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# in-memory queue for real-time events
event_queue: asyncio.Queue = asyncio.Queue()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("="*60)
    logger.info("Starting Enhanced Remote Access Honeypot Backend...")
    logger.info("="*60)
    await db.init_db()
    logger.info("✓ Database initialized with enhanced schema")
    
    # Start enhanced honeypot background task
    honeypot_task = asyncio.create_task(start_enhanced_honeypot(event_queue))
    logger.info("✓ Enhanced honeypot started (SSH & RDP emulation)")
    logger.info("="*60)
    
    yield
    
    # Shutdown
    honeypot_task.cancel()
    logger.info("Honeypot stopped")

app = FastAPI(title="Enhanced Remote Access Honeypot Backend", lifespan=lifespan)

@app.get("/events")
async def get_events(limit: int = 50):
    rows = await db.fetch_events(limit=limit)
    return JSONResponse(rows)

@app.get("/auth_attempts")
async def get_auth_attempts(limit: int = 100):
    rows = await db.fetch_auth_attempts(limit=limit)
    return JSONResponse(rows)

@app.get("/commands")
async def get_commands(limit: int = 100):
    rows = await db.fetch_commands(limit=limit)
    return JSONResponse(rows)

@app.get("/sessions")
async def get_sessions(limit: int = 50):
    rows = await db.fetch_sessions(limit=limit)
    return JSONResponse(rows)

@app.get("/statistics")
async def get_statistics():
    stats = await db.get_statistics()
    return JSONResponse(stats)

@app.get("/ip_intelligence")
async def get_ip_intelligence(limit: int = 100):
    rows = await db.fetch_ip_intel(limit=limit)
    return JSONResponse(rows)

class WebSocketManager:
    def __init__(self):
        self.active: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        try:
            self.active.remove(ws)
        except ValueError:
            pass

    async def broadcast(self, message: dict):
        living = []
        for ws in list(self.active):
            try:
                await ws.send_json(message)
                living.append(ws)
            except Exception:
                pass
        self.active = living

ws_manager = WebSocketManager()

@app.websocket("/ws/events")
async def websocket_events(ws: WebSocket):
    await ws_manager.connect(ws)
    try:
        while True:
            event = await event_queue.get()
            await ws.send_json(event)
    except WebSocketDisconnect:
        ws_manager.disconnect(ws)
    except Exception:
        ws_manager.disconnect(ws)


@app.post("/ingest/web")
async def ingest_web(request: Request):
    """Accept events from external websites (backend_websites) and insert into DB,
    then broadcast to WebSocket subscribers in real-time.
    Expected JSON: { "type": "auth|command|session|event", "payload": { ... } }
    """
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"error": "invalid json"}, status_code=400)

    etype = data.get("type")
    payload = data.get("payload", {})
    # normalize timestamp
    payload.setdefault("ts", datetime.utcnow().isoformat() + "Z")

    # Insert into appropriate table and broadcast
    try:
        if etype == "auth":
            await db.insert_auth_attempt(payload)
        elif etype == "command":
            await db.insert_command(payload)
        elif etype == "session":
            await db.create_session(payload)
        else:
            # generic event
            await db.insert_event(payload)

        # push to in-memory queue and broadcast
        await event_queue.put({"type": etype, "payload": payload})
        # best-effort broadcast
        try:
            await ws_manager.broadcast({"type": etype, "payload": payload})
        except Exception:
            pass

        return JSONResponse({"status": "ok"})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
