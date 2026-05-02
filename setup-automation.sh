#!/bin/bash

LOG_DIR="/home/user/claude-code/logs"
mkdir -p "$LOG_DIR"

echo "設置自動化任務..."

# 每小時檢查新聞一次
CRON_NEWS="0 * * * * /usr/bin/python3 /home/user/claude-code/news-collector.py >> $LOG_DIR/news-collector.log 2>&1"

# 每 6 小時自動生成視頻
CRON_VIDEO="0 */6 * * * /usr/bin/python3 /home/user/claude-code/auto-video-generator.py >> $LOG_DIR/video-generator.log 2>&1"

# 每分鐘檢查系統監控
CRON_MONITOR="* * * * * bash /home/user/claude-code/system-monitor.sh >> $LOG_DIR/system-monitor.log 2>&1"

# 檢查是否已經有 crontab
if crontab -l 2>/dev/null | grep -q "news-collector"; then
    echo "⚠️ Cron 任務已存在，跳過設置"
else
    # 添加新的 cron 任務
    (crontab -l 2>/dev/null; echo "$CRON_NEWS"; echo "$CRON_VIDEO") | crontab -
    echo "✓ 已設置 cron 任務:"
    echo "  - 每小時收集新聞"
    echo "  - 每 6 小時生成視頻"
fi

echo "✓ 自動化設置完成"
echo ""
echo "運行日誌位置:"
echo "  - 新聞收集: $LOG_DIR/news-collector.log"
echo "  - 視頻生成: $LOG_DIR/video-generator.log"
echo "  - 系統監控: $LOG_DIR/system-monitor.log"
