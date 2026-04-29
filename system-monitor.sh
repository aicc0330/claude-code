#!/bin/bash

LOG_DIR="/home/user/claude-code/logs"
MONITOR_DIR="/home/user/claude-code/monitoring"
mkdir -p "$LOG_DIR" "$MONITOR_DIR"

TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
MONITOR_LOG="$MONITOR_DIR/monitor_$TIMESTAMP.log"
SYSTEM_LOG="$LOG_DIR/system_$TIMESTAMP.log"

while true; do
  {
    echo "=== $(date '+%Y-%m-%d %H:%M:%S') ==="

    # Memory
    MEMORY=$(free -h | awk '/^Mem:/ {print "Used: " $3 " / " $2 " (" int($3/$2*100) "%)"}')
    echo "Memory: $MEMORY"

    # CPU
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    echo "CPU: ${CPU_USAGE}% used"

    # Disk
    DISK=$(df -h /home/user/claude-code | awk 'NR==2 {print "Used: " $3 " / " $2 " (" int($3/$2*100) "%)"}')
    echo "Disk: $DISK"

    # Process check
    if pgrep -f "npm run dev" > /dev/null; then
      echo "Dispatch: ✓ Running"
    else
      echo "Dispatch: ✗ NOT Running"
    fi

    # Alert thresholds
    if (( $(echo "$CPU_USAGE > 90" | bc -l) )); then
      echo "⚠️ ALERT: CPU > 90%"
    fi

    if (( $(echo "$MEMORY" | grep -oP '\d+' | head -1) > 80 )); then
      echo "⚠️ ALERT: Memory > 80%"
    fi

    echo ""
  } | tee -a "$SYSTEM_LOG" "$MONITOR_LOG"

  sleep 60
done
