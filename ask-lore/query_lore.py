#!/usr/bin/env python3
"""Query the Lore (librarian) agent via the Fera gateway websocket."""

import asyncio
import json
import sys
import uuid

sys.path.insert(0, '/opt/fera/src')


async def query_lore(question: str, session: str = "librarian/dm-fera", timeout: float = 120.0) -> str:
    import websockets
    from fera.config import ensure_auth_token, load_config

    config = load_config()
    gw = config["gateway"]
    token = ensure_auth_token(config, save=False)
    url = f"ws://127.0.0.1:{gw['port']}"

    async with websockets.connect(url) as ws:
        # Authenticate
        req = {"type": "req", "id": str(uuid.uuid4()), "method": "connect", "params": {"token": token}}
        await ws.send(json.dumps(req))
        resp = json.loads(await ws.recv())
        if not resp.get("ok"):
            return f"Auth failed: {resp.get('error')}"

        # Send message
        msg = {
            "type": "req",
            "id": str(uuid.uuid4()),
            "method": "chat.send",
            "params": {"text": question, "session": session},
        }
        await ws.send(json.dumps(msg))

        # Collect streamed response
        parts = []
        try:
            async with asyncio.timeout(timeout):
                async for raw in ws:
                    frame = json.loads(raw)
                    if frame.get("type") == "event":
                        evt = frame.get("event", "")
                        if evt == "agent.text":
                            parts.append(frame.get("data", {}).get("text", ""))
                        elif evt == "agent.done":
                            break
                        elif evt == "agent.error":
                            return f"Agent error: {frame.get('data', {}).get('error')}"
        except asyncio.TimeoutError:
            if parts:
                parts.append("\n[response timed out]")
            else:
                return "Timed out waiting for Lore's response."

    return "".join(parts)


def main():
    if len(sys.argv) < 2:
        print("Usage: query_lore.py <question>", file=sys.stderr)
        sys.exit(1)
    question = " ".join(sys.argv[1:])
    result = asyncio.run(query_lore(question))
    print(result)


if __name__ == "__main__":
    main()
