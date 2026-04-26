"""
Telegram ↔ Claude Code bridge bot.

Env vars required:
  TELEGRAM_TOKEN   — bot token from @BotFather
  ALLOWED_USER_ID  — Telegram user ID allowed to pair (optional; leave blank to allow anyone)

Pairing flow:
  1. User DMs the bot → receives a 6-char code + Telegram user ID
  2. User runs in Claude Code terminal:  /telegram:access pair <code>
  3. All subsequent DMs are forwarded to that Claude Code session
"""

import asyncio
import logging
import os
import secrets
import string
import subprocess
import sys
from datetime import datetime

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN: str = os.environ["TELEGRAM_TOKEN"]
ALLOWED_USER_ID: int | None = (
    int(os.environ["ALLOWED_USER_ID"]) if os.environ.get("ALLOWED_USER_ID") else None
)
HEALTH_CHECK_INTERVAL = 30  # seconds between connection probes
RECONNECT_ATTEMPTS = 3


# ---------------------------------------------------------------------------
# Shared state
# ---------------------------------------------------------------------------

class BridgeState:
    def __init__(self) -> None:
        self.paired_chat_id: int | None = None
        self.pair_code: str | None = None
        self.claude_proc: subprocess.Popen | None = None
        self.last_active: datetime | None = None
        self.consecutive_failures: int = 0

    # --- helpers ---

    def is_paired(self) -> bool:
        return self.paired_chat_id is not None

    def is_session_alive(self) -> bool:
        """Return True if the Claude Code subprocess is running."""
        if self.claude_proc is None:
            return False
        return self.claude_proc.poll() is None

    def fresh_pair_code(self) -> str:
        alphabet = string.ascii_uppercase + string.digits
        self.pair_code = "".join(secrets.choice(alphabet) for _ in range(6))
        return self.pair_code

    def start_session(self) -> bool:
        """Launch (or relaunch) the Claude Code subprocess."""
        self.stop_session()
        try:
            self.claude_proc = subprocess.Popen(
                ["claude", "--dangerously-skip-permissions"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            self.consecutive_failures = 0
            logger.info("Claude Code session started (pid=%d)", self.claude_proc.pid)
            return True
        except FileNotFoundError:
            logger.error("'claude' command not found — is Claude Code installed?")
            return False

    def stop_session(self) -> None:
        if self.claude_proc and self.claude_proc.poll() is None:
            self.claude_proc.terminate()
            try:
                self.claude_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.claude_proc.kill()
        self.claude_proc = None

    async def send_to_claude(self, text: str) -> str | None:
        """Write a message to Claude Code stdin and read the response."""
        if not self.is_session_alive():
            return None
        try:
            assert self.claude_proc and self.claude_proc.stdin and self.claude_proc.stdout
            self.claude_proc.stdin.write(text + "\n")
            self.claude_proc.stdin.flush()
            # Read lines until a blank line (simple delimiter heuristic)
            lines: list[str] = []
            loop = asyncio.get_event_loop()
            while True:
                line = await loop.run_in_executor(None, self.claude_proc.stdout.readline)
                if not line or line.strip() == "":
                    break
                lines.append(line.rstrip())
            self.last_active = datetime.now()
            return "\n".join(lines) if lines else None
        except Exception as exc:
            logger.error("Error communicating with Claude Code: %s", exc)
            return None


state = BridgeState()


# ---------------------------------------------------------------------------
# Telegram command handlers
# ---------------------------------------------------------------------------

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert update.effective_user and update.message
    user_id = update.effective_user.id

    if ALLOWED_USER_ID and user_id != ALLOWED_USER_ID:
        await update.message.reply_text("Unauthorized.")
        return

    code = state.fresh_pair_code()
    state.paired_chat_id = update.effective_chat.id if update.effective_chat else None

    await update.message.reply_text(
        f"Paired as {user_id}.\n\n"
        "This bot bridges Telegram to a Claude Code session.\n\n"
        "To pair:\n"
        f"1. DM me anything — you'll get a 6-char code\n"
        f"2. In Claude Code: /telegram:access pair {code}\n\n"
        "After that, DMs here reach that session."
    )

    if not state.is_session_alive():
        started = state.start_session()
        if not started:
            await update.message.reply_text(
                "Warning: Could not start Claude Code session. "
                "Make sure the `claude` CLI is installed."
            )


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert update.message

    if not state.is_paired():
        await update.message.reply_text("Not paired. Send /start to begin.")
        return

    if state.is_session_alive():
        idle = ""
        if state.last_active:
            secs = int((datetime.now() - state.last_active).total_seconds())
            idle = f"\nLast activity: {secs}s ago"
        await update.message.reply_text(f"Status: Connected{idle}")
    else:
        await update.message.reply_text(
            "Status: Disconnected\n"
            "Send /start to reconnect the Claude Code session."
        )


# ---------------------------------------------------------------------------
# Message forwarding
# ---------------------------------------------------------------------------

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert update.effective_user and update.message and update.message.text
    user_id = update.effective_user.id
    text = update.message.text

    if ALLOWED_USER_ID and user_id != ALLOWED_USER_ID:
        await update.message.reply_text("Unauthorized.")
        return

    # First contact — auto-pair
    if not state.is_paired():
        code = state.fresh_pair_code()
        state.paired_chat_id = update.effective_chat.id if update.effective_chat else None
        await update.message.reply_text(
            f"Paired as {user_id}.\n\n"
            "This bot bridges Telegram to a Claude Code session.\n\n"
            "To pair:\n"
            "1. DM me anything — you'll get a 6-char code\n"
            f"2. In Claude Code: /telegram:access pair {code}\n\n"
            "After that, DMs here reach that session."
        )
        state.start_session()
        return

    if not state.is_session_alive():
        await update.message.reply_text(
            "Claude Code session is not running. Send /start to reconnect."
        )
        return

    reply = await state.send_to_claude(text)
    if reply:
        await update.message.reply_text(reply)
    else:
        await update.message.reply_text(
            "(No response from Claude Code — session may have ended.)"
        )


# ---------------------------------------------------------------------------
# Background health-check job
# ---------------------------------------------------------------------------

async def health_check(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Periodically verify the Claude Code session is alive; alert + reconnect if not."""
    if not state.is_paired():
        return

    if state.is_session_alive():
        state.consecutive_failures = 0
        return

    state.consecutive_failures += 1
    logger.warning(
        "Health check: Claude Code session is down (failure #%d)",
        state.consecutive_failures,
    )

    chat_id = state.paired_chat_id
    assert chat_id is not None

    if state.consecutive_failures <= RECONNECT_ATTEMPTS:
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                f"Connection lost (attempt {state.consecutive_failures}/{RECONNECT_ATTEMPTS}). "
                "Reconnecting…"
            ),
        )
        restarted = state.start_session()
        if restarted:
            await context.bot.send_message(
                chat_id=chat_id, text="Reconnected to Claude Code."
            )
        else:
            await context.bot.send_message(
                chat_id=chat_id, text="Reconnect failed. Check that `claude` CLI is available."
            )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                "Claude Code session is offline and could not be restarted automatically.\n"
                "Send /start to try again manually."
            ),
        )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    job_queue = app.job_queue
    assert job_queue is not None
    job_queue.run_repeating(health_check, interval=HEALTH_CHECK_INTERVAL, first=10)

    logger.info("Bot starting…")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
