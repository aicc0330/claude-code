"""
Claude Code side of the Telegram bridge.

Usage (in your Claude Code terminal):
  python pair.py <6-char-code>

What it does:
  1. Connects to the local bot server with your pair code
  2. Polls every 2 s for new Telegram messages
  3. Displays them in the terminal; read your reply from stdin
  4. Sends heartbeats so the bot knows this session is alive
"""

import asyncio
import os
import sys

import aiohttp

BRIDGE_PORT = int(os.environ.get("BRIDGE_PORT", "7842"))
BASE_URL = f"http://localhost:{BRIDGE_PORT}"
POLL_INTERVAL = 2  # seconds


async def run(code: str) -> None:
    async with aiohttp.ClientSession() as session:
        # --- Pair ---
        try:
            async with session.post(f"{BASE_URL}/pair?code={code.upper()}") as resp:
                if resp.status != 200:
                    body = await resp.text()
                    print(f"Pairing failed ({resp.status}): {body}")
                    return
                data = await resp.json()
                token: str = data["token"]
        except aiohttp.ClientConnectorError:
            print(
                f"Cannot reach bot server at localhost:{BRIDGE_PORT}.\n"
                "Make sure bot.py is running first."
            )
            return

        headers = {"X-Session-Token": token}
        print("Paired! Listening for Telegram messages. Press Ctrl-C to quit.\n")

        loop = asyncio.get_event_loop()

        while True:
            try:
                # Poll for next message (also acts as heartbeat)
                async with session.get(f"{BASE_URL}/poll", headers=headers) as resp:
                    if resp.status == 401:
                        print("Session expired. Re-run with a new pair code.")
                        return
                    data = await resp.json()
                    msg: str | None = data.get("message")

                if msg:
                    print(f"Telegram → {msg}")
                    reply = await loop.run_in_executor(None, input, "You → ")
                    if reply.strip():
                        async with session.post(
                            f"{BASE_URL}/reply",
                            headers=headers,
                            json={"text": reply.strip()},
                        ) as _:
                            pass
                else:
                    # No message — just send a heartbeat
                    async with session.post(
                        f"{BASE_URL}/heartbeat", headers=headers
                    ) as _:
                        pass

                await asyncio.sleep(POLL_INTERVAL)

            except aiohttp.ClientConnectorError:
                print("Lost connection to bot server. Retrying in 5 s…")
                await asyncio.sleep(5)
            except KeyboardInterrupt:
                print("\nDisconnected.")
                return


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python pair.py <6-char-code>")
        sys.exit(1)
    asyncio.run(run(sys.argv[1]))


if __name__ == "__main__":
    main()
