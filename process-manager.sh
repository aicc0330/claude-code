#!/bin/bash

LOG_DIR="/home/user/claude-code/logs"
PID_FILE="/tmp/claude-code.pid"
RESTART_LOG="$LOG_DIR/restarts.log"
mkdir -p "$LOG_DIR"

function log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$RESTART_LOG"
}

function start_dispatch() {
  log "Starting Dispatch server..."
  cd /home/user/claude-code
  npm run dev > "$LOG_DIR/dispatch.log" 2>&1 &
  DISPATCH_PID=$!
  echo $DISPATCH_PID > "$PID_FILE"
  log "Dispatch started with PID $DISPATCH_PID"
}

function check_and_restart() {
  if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ! ps -p $PID > /dev/null 2>&1; then
      log "⚠️ Process $PID is dead, restarting..."
      start_dispatch
      log "✓ Restarted after crash"
    fi
  else
    log "No PID file found, starting fresh..."
    start_dispatch
  fi
}

# Initial start
start_dispatch

# Monitor loop
while true; do
  sleep 30
  check_and_restart
done
