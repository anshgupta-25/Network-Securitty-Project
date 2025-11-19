import asyncio
import os
import logging
import uuid
from datetime import datetime
from typing import Dict

from . import db_enhanced as db

logger = logging.getLogger(__name__)
PAYLOAD_PREVIEW_BYTES = int(os.getenv("PAYLOAD_PREVIEW_BYTES", "1024"))

# Fake shell responses
FAKE_SHELL_RESPONSES = {
    "ls": "bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var",
    "pwd": "/home/user",
    "whoami": "root",
    "id": "uid=0(root) gid=0(root) groups=0(root)",
    "uname -a": "Linux honeypot 5.10.0-23-amd64 #1 SMP Debian 5.10.179-1 (2023-05-12) x86_64 GNU/Linux",
    "cat /etc/passwd": "root:x:0:0:root:/root:/bin/bash\nuser:x:1000:1000:User:/home/user:/bin/bash",
    "ps aux": "USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND\nroot         1  0.0  0.0 169640  11972 ?        Ss   10:00   0:01 /sbin/init",
    "ifconfig": "eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500\n        inet 192.168.1.100  netmask 255.255.255.0",
    "wget": "-bash: wget: command not found",
    "curl": "-bash: curl: command not found",
}

async def handle_ssh_session(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, event_queue: asyncio.Queue):
    """Enhanced SSH session handler with authentication and command logging"""
    peer = writer.get_extra_info("peername") or ("unknown", 0)
    src_ip, src_port = peer[0], peer[1]
    dest_port = writer.get_extra_info("sockname")[1]
    
    session_id = str(uuid.uuid4())
    session_start = datetime.utcnow().isoformat() + "Z"
    
    logger.info(f"[SSH SESSION] New connection from {src_ip}:{src_port} | Session: {session_id}")
    
    # Create session record
    try:
        await db.create_session({
            "session_id": session_id,
            "src_ip": src_ip,
            "src_port": src_port,
            "start_time": session_start
        })
    except Exception as e:
        logger.error(f"Failed to create session: {e}")
    
    # Send SSH banner
    try:
        banner = b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\r\n"
        writer.write(banner)
        await writer.drain()
        await asyncio.sleep(0.5)
    except Exception:
        pass
    
    auth_attempts = 0
    authenticated = False
    
    # Authentication phase
    try:
        # Read client banner/authentication attempts
        data = await asyncio.wait_for(reader.read(PAYLOAD_PREVIEW_BYTES), timeout=10.0)
        
        # Try to extract credentials (simple pattern matching)
        payload_str = data.decode("utf-8", errors="replace")
        
        # Simulate SSH auth attempts
        lines = payload_str.split("\n")
        for line in lines:
            if ":" in line or "user" in line.lower() or "pass" in line.lower():
                parts = line.split(":")
                if len(parts) >= 2:
                    username = parts[0].strip()[:50]
                    password = parts[1].strip()[:100]
                    
                    auth_attempts += 1
                    
                    # Log authentication attempt
                    await db.insert_auth_attempt({
                        "ts": datetime.utcnow().isoformat() + "Z",
                        "src_ip": src_ip,
                        "username": username,
                        "password": password,
                        "success": False,
                        "service": "SSH",
                        "session_id": session_id
                    })
                    
                    logger.warning(f"[AUTH ATTEMPT] {src_ip} tried: {username}:{password}")
        
        # Always accept after attempts (to capture commands)
        if auth_attempts == 0 and data:
            # Generic credential capture
            await db.insert_auth_attempt({
                "ts": datetime.utcnow().isoformat() + "Z",
                "src_ip": src_ip,
                "username": "unknown",
                "password": payload_str[:100],
                "success": False,
                "service": "SSH",
                "session_id": session_id
            })
            auth_attempts = 1
        
        # Send fake authentication success
        writer.write(b"Authentication successful\r\n")
        await writer.drain()
        authenticated = True
        
        # Send fake shell prompt
        writer.write(b"root@honeypot:~# ")
        await writer.drain()
        
    except asyncio.TimeoutError:
        logger.info(f"[SSH SESSION] Timeout waiting for auth from {src_ip}")
    except Exception as e:
        logger.error(f"[SSH SESSION] Error in auth phase: {e}")
    
    # Command execution phase
    commands_executed = 0
    try:
        if authenticated:
            while True:
                # Read command
                cmd_data = await asyncio.wait_for(reader.read(1024), timeout=30.0)
                if not cmd_data:
                    break
                
                command = cmd_data.decode("utf-8", errors="replace").strip()
                if not command:
                    continue
                
                logger.info(f"[COMMAND] {src_ip} executed: {command}")
                commands_executed += 1
                
                # Generate fake response
                response = FAKE_SHELL_RESPONSES.get(command.lower(), f"-bash: {command.split()[0] if command else 'command'}: command not found")
                
                # Log command
                await db.insert_command({
                    "ts": datetime.utcnow().isoformat() + "Z",
                    "session_id": session_id,
                    "src_ip": src_ip,
                    "command": command,
                    "response": response
                })
                
                # Send response
                writer.write(response.encode("utf-8") + b"\r\n")
                writer.write(b"root@honeypot:~# ")
                await writer.drain()
                
                # Broadcast to WebSocket
                await event_queue.put({
                    "type": "command",
                    "session_id": session_id,
                    "src_ip": src_ip,
                    "command": command,
                    "ts": datetime.utcnow().isoformat() + "Z"
                })
                
    except asyncio.TimeoutError:
        logger.info(f"[SSH SESSION] Command timeout from {src_ip}")
    except Exception as e:
        logger.error(f"[SSH SESSION] Error in command phase: {e}")
    
    # Close session
    session_end = datetime.utcnow().isoformat() + "Z"
    duration = 0
    try:
        start_dt = datetime.fromisoformat(session_start.replace("Z", ""))
        end_dt = datetime.fromisoformat(session_end.replace("Z", ""))
        duration = int((end_dt - start_dt).total_seconds())
        
        await db.update_session(session_id, {
            "end_time": session_end,
            "duration_seconds": duration,
            "auth_attempts": auth_attempts,
            "commands_count": commands_executed,
            "success_login": authenticated
        })
    except Exception as e:
        logger.error(f"Failed to update session: {e}")
    
    logger.info(f"[SSH SESSION] Closed {src_ip} | Auth: {auth_attempts} | Cmds: {commands_executed} | Duration: {duration}s")
    
    try:
        writer.close()
        await writer.wait_closed()
    except Exception:
        pass

async def handle_rdp_session(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, event_queue: asyncio.Queue):
    """RDP session handler with credential capture"""
    peer = writer.get_extra_info("peername") or ("unknown", 0)
    src_ip, src_port = peer[0], peer[1]
    
    session_id = str(uuid.uuid4())
    logger.info(f"[RDP SESSION] New connection from {src_ip}:{src_port}")
    
    try:
        # Read RDP handshake/credentials
        data = await asyncio.wait_for(reader.read(PAYLOAD_PREVIEW_BYTES), timeout=5.0)
        payload_str = data.decode("utf-8", errors="replace")
        
        # Try to extract credentials
        if ":" in payload_str:
            parts = payload_str.split(":")
            username = parts[0].strip()[:50]
            password = parts[1].strip() if len(parts) > 1 else ""
            
            await db.insert_auth_attempt({
                "ts": datetime.utcnow().isoformat() + "Z",
                "src_ip": src_ip,
                "username": username,
                "password": password,
                "success": False,
                "service": "RDP",
                "session_id": session_id
            })
            
            logger.warning(f"[RDP AUTH] {src_ip} tried: {username}:{password}")
        
        # Send minimal RDP response
        writer.write(b"\x03\x00\x00\x13\x0e\xd0")
        await writer.drain()
        
    except asyncio.TimeoutError:
        pass
    except Exception as e:
        logger.error(f"[RDP SESSION] Error: {e}")
    
    try:
        writer.close()
        await writer.wait_closed()
    except Exception:
        pass

async def start_enhanced_honeypot(event_queue: asyncio.Queue):
    """Start enhanced honeypot with SSH and RDP emulation"""
    ports_config = os.getenv("HONEYPOT_PORTS", "2222,3389")
    ports = [int(p.strip()) for p in ports_config.split(",") if p.strip()]
    
    servers = []
    
    # SSH on 2222
    if 2222 in ports:
        try:
            ssh_server = await asyncio.start_server(
                lambda r, w: handle_ssh_session(r, w, event_queue),
                host="0.0.0.0",
                port=2222
            )
            servers.append(ssh_server)
            logger.info(f"✓ SSH Honeypot listening on 0.0.0.0:2222")
        except Exception as e:
            logger.error(f"✗ Failed to start SSH honeypot on 2222: {e}")
    
    # RDP on 3389
    if 3389 in ports:
        try:
            rdp_server = await asyncio.start_server(
                lambda r, w: handle_rdp_session(r, w, event_queue),
                host="0.0.0.0",
                port=3389
            )
            servers.append(rdp_server)
            logger.info(f"✓ RDP Honeypot listening on 0.0.0.0:3389")
        except Exception as e:
            logger.error(f"✗ Failed to start RDP honeypot on 3389: {e}")
    
    # Keep running
    try:
        await asyncio.gather(*[s.serve_forever() for s in servers])
    except asyncio.CancelledError:
        logger.info("Honeypot servers shutting down...")
        for server in servers:
            server.close()
            await server.wait_closed()
