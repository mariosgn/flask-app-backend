import asyncio
import json
from datetime import datetime

import websockets
import os

connected = set()
POLLING_DIR = "./store/websocket_messages"
POLL_INTERVAL = 1  # seconds
PING_INTERVAL = 10  # seconds

async def handler(websocket):
    print("Client connected")
    connected.add(websocket)
    try:
        async for message in websocket:
            print(f"Received: {message}")
            # Echo to all clients
            await broadcast(f"Echo: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        connected.discard(websocket)

async def broadcast(message):
    if connected:
        await asyncio.gather(*[
            ws.send(message) for ws in connected if ws.state == websockets.protocol.State.OPEN
        ])

async def poll_directory():
    while True:
        try:
            files = [
                f for f in os.listdir(POLLING_DIR)
                if f.endswith(".txt") and not f.startswith(".") and os.path.isfile(os.path.join(POLLING_DIR, f))
            ]
            for filename in files:
                file_path = os.path.join(POLLING_DIR, filename)
                with open(file_path, 'r') as f:
                    content = f.read()
                    print(f"Sending content of {filename} to clients")
                    await broadcast(content)
                os.remove(file_path)
        except Exception as e:
            print(f"Error while polling directory: {e}")
        await asyncio.sleep(POLL_INTERVAL)

async def periodic_ping():
    while True:
        msg = {"action": "ping", "value": datetime.now().isoformat()}
        await broadcast( json.dumps(msg) )
        await asyncio.sleep(PING_INTERVAL)

async def main():
    os.makedirs(POLLING_DIR, exist_ok=True)
    print("WebSocket server listening on ws://localhost:8765")
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.gather(poll_directory(), periodic_ping())

if __name__ == "__main__":
    asyncio.run(main())
