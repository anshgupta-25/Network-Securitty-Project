"""
WebSocket Real-Time Threat Monitor
Connects to the honeypot WebSocket and displays threats instantly as they happen
"""
import asyncio
import json
import websockets
from datetime import datetime

async def monitor_threats():
    uri = "ws://127.0.0.1:8000/ws/events"
    
    print("\n" + "="*60)
    print("   WEBSOCKET REAL-TIME THREAT MONITOR")
    print("="*60)
    print(f"Connected to: {uri}")
    print("Listening for threats... (Press CTRL+C to stop)\n")
    
    try:
        async with websockets.connect(uri) as websocket:
            event_count = 0
            while True:
                # Receive threat event
                message = await websocket.recv()
                event = json.loads(message)
                event_count += 1
                
                # Display threat in real-time
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"\n{'='*60}")
                print(f"🚨 THREAT #{event_count} DETECTED - {now}")
                print(f"{'='*60}")
                print(f"  Event ID:      {event.get('id', 'N/A')}")
                print(f"  Timestamp:     {event.get('ts', 'N/A')}")
                print(f"  Source:        {event.get('src_ip')}:{event.get('src_port')}")
                print(f"  Target Port:   {event.get('dest_port')}", end="")
                
                # Identify service
                port = event.get('dest_port')
                if port == 2222:
                    print(" [SSH]")
                elif port == 3389:
                    print(" [RDP]")
                else:
                    print(" [Unknown]")
                
                print(f"  Protocol:      {event.get('protocol')}")
                
                # Display payload
                payload = event.get('payload_preview', '')
                if len(payload) > 100:
                    payload = payload[:100] + "..."
                print(f"  Payload:       {payload}")
                
                # Alert sound (system beep)
                print("\a", end="")  # Beep sound
                
    except KeyboardInterrupt:
        print("\n\n[*] Monitoring stopped by user")
    except Exception as e:
        print(f"\n[!] Error: {e}")
        print("[*] Make sure the honeypot backend is running on port 8000")

if __name__ == "__main__":
    print("\nStarting WebSocket Real-Time Monitor...")
    asyncio.run(monitor_threats())
