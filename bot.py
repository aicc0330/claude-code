"""
Telegram ↔ Claude Code bridge bot.

Architecture:
  - Telegram bot receives DMs and generates a 6-char pair code
  - A local HTTP server (localhost:BRIDGE_PORT) waits for Claude Code to connect
  - Claude Code runs `python pair.py <code>` to establish the bridge
  - After pairing, Telegram DMs are queued for Claude Code to poll
  - Claude Code sends replies back via POST /reply
  - Health check monitors heartbeats; alerts Telegram user on disconnect

Env vars:
  TELEGRAM_TOKEN   — bot token from @BotFather
  BRIDGE_PORT      — local HTTP port (default: 7842)
"""

import asyncio
import logging
import os
import secrets
import string
from datetime import datetime

from aiohttp import web
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import Update

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN: str = os.environ["TELEGRAM_TOKEN"]
BRIDGE_PORT: int = int(os.environ.get("BRIDGE_PORT", "7842"))
HEALTH_TIMEOUT: int = 60   # seconds without heartbeat → disconnected
HEALTH_CHECK_INTERVAL: int = 30


# ---------------------------------------------------------------------------
# Shared state
# ---------------------------------------------------------------------------

class BridgeState:
    def __init__(self) -> None:
        self.paired_chat_id: int | None = None
        self.pair_code: str | None = None
        self.session_token: str | None = None
        self.last_heartbeat: datetime | None = None
        self.alerted: bool = False
        self.pending: asyncio.Queue[str] = asyncio.Queue()

    def fresh_code(self) -> str:
        alphabet = string.ascii_uppercase + string.digits
        self.pair_code = "".join(secrets.choice(alphabet) for _ in range(6))
        return self.pair_code

    def is_connected(self) -> bool:
        if self.last_heartbeat is None:
            return False
        return (datetime.now() - self.last_heartbeat).total_seconds() < HEALTH_TIMEOUT

    def touch(self) -> None:
        self.last_heartbeat = datetime.now()
        self.alerted = False

    def pair_intro(self, user_id: int) -> str:
        code = self.pair_code or "??????"
        return (
            f"Paired as {user_id}.\n\n"
            "This bot bridges Telegram to a Claude Code session.\n\n"
            "To pair:\n"
            "1. DM me anything — you'll get a 6-char code\n"
            f"2. In Claude Code terminal:  python pair.py {code}\n\n"
            "After that, DMs here reach that session."
        )


state = BridgeState()


# ---------------------------------------------------------------------------
# Local HTTP server — Claude Code connects here
# ---------------------------------------------------------------------------

async def http_pair(request: web.Request) -> web.Response:
    """Claude Code registers with its pair code, receives a session token."""
    code = request.query.get("code", "").upper()
    if not state.pair_code or code != state.pair_code:
        return web.json_response({"error": "invalid code"}, status=403)

    token = secrets.token_hex(16)
    state.session_token = token
    state.touch()
    logger.info("Claude Code session paired (token=%s…)", token[:8])

    bot = request.app["bot"]
    if state.paired_chat_id:
        await bot.send_message(chat_id=state.paired_chat_id, text="Claude Code session connected.")

    return web.json_response({"token": token})


async def http_poll(request: web.Request) -> web.Response:
    """Claude Code polls for the next pending Telegram message."""
    if request.headers.get("X-Session-Token") != state.session_token:
        return web.json_response({"error": "unauthorized"}, status=401)

    state.touch()
    try:
        msg = state.pending.get_nowait()
    except asyncio.QueueEmpty:
        msg = None

    return web.json_response({"message": msg})


async def http_reply(request: web.Request) -> web.Response:
    """Claude Code posts its response to be forwarded to Telegram."""
    if request.headers.get("X-Session-Token") != state.session_token:
        return web.json_response({"error": "unauthorized"}, status=401)

    data = await request.json()
    text: str = data.get("text", "").strip()
    state.touch()

    if text and state.paired_chat_id:
        bot = request.app["bot"]
        await bot.send_message(chat_id=state.paired_chat_id, text=text)

    return web.json_response({"ok": True})


async def http_heartbeat(request: web.Request) -> web.Response:
    """Claude Code sends a heartbeat to signal it is still alive."""
    if request.headers.get("X-Session-Token") != state.session_token:
        return web.json_response({"error": "unauthorized"}, status=401)

    state.touch()
    return web.json_response({"ok": True})


# ---------------------------------------------------------------------------
# Telegram command handlers
# ---------------------------------------------------------------------------

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert update.effective_user and update.message and update.effective_chat
    state.fresh_code()
    state.paired_chat_id = update.effective_chat.id
    await update.message.reply_text(state.pair_intro(update.effective_user.id))


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert update.message
    if not state.paired_chat_id:
        await update.message.reply_text("Not paired. Send /start to begin.")
        return

    if state.is_connected():
        assert state.last_heartbeat
        secs = int((datetime.now() - state.last_heartbeat).total_seconds())
        await update.message.reply_text(f"Status: Connected\nLast heartbeat: {secs}s ago")
    else:
        await update.message.reply_text(
            "Status: Disconnected\n"
            "Run /start to generate a new pair code, then `python pair.py <code>`."
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert update.effective_user and update.message and update.message.text and update.effective_chat

    if not state.paired_chat_id:
        state.fresh_code()
        state.paired_chat_id = update.effective_chat.id
        await update.message.reply_text(state.pair_intro(update.effective_user.id))
        return

    if not state.is_connected():
        await update.message.reply_text(
            "Claude Code session is not connected.\n"
            "Run /start to get a new code, then `python pair.py <code>`."
        )
        return

    await state.pending.put(update.message.text)


# ---------------------------------------------------------------------------
# Background health-check
# ---------------------------------------------------------------------------

async def health_check(context: ContextTypes.DEFAULT_TYPE) -> None:
    if not state.paired_chat_id or not state.session_token:
        return
    if state.is_connected():
        return
    if not state.alerted:
        state.alerted = True
        await context.bot.send_message(
            chat_id=state.paired_chat_id,
            text=(
                "Claude Code session disconnected.\n"
                "Run /start to pair again, then `python pair.py <code>`."
            ),
        )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

async def main() -> None:
    # Build Telegram application
    tg_app = Application.builder().token(TELEGRAM_TOKEN).build()
    tg_app.add_handler(CommandHandler("start", cmd_start))
    tg_app.add_handler(CommandHandler("status", cmd_status))
    tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    assert tg_app.job_queue
    tg_app.job_queue.run_repeating(health_check, interval=HEALTH_CHECK_INTERVAL, first=10)

    # Build local HTTP bridge server
    http_app = web.Application()
    http_app["bot"] = tg_app.bot
    http_app.router.add_post("/pair", http_pair)
    http_app.router.add_get("/poll", http_poll)
    http_app.router.add_post("/reply", http_reply)
    http_app.router.add_post("/heartbeat", http_heartbeat)

    runner = web.AppRunner(http_app)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", BRIDGE_PORT)
    await site.start()
    logger.info("Bridge server listening on localhost:%d", BRIDGE_PORT)

    async with tg_app:
        await tg_app.start()
        assert tg_app.updater
        await tg_app.updater.start_polling(drop_pending_updates=True)
        logger.info("Telegram bot started. Waiting…")
        await asyncio.Event().wait()
        await tg_app.updater.stop()
        await tg_app.stop()


if __name__ == "__main__":
    asyncio.run(main())
