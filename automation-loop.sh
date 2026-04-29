#!/bin/bash

LOG_DIR="/home/user/claude-code/logs"
mkdir -p "$LOG_DIR"

function run_news_collection() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 執行新聞收集..." >> "$LOG_DIR/news-collector.log"
  /usr/bin/python3 /home/user/claude-code/news-collector.py >> "$LOG_DIR/news-collector.log" 2>&1
}

function run_video_generation() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 執行視頻生成..." >> "$LOG_DIR/video-generator.log"
  /usr/bin/python3 /home/user/claude-code/auto-video-generator.py >> "$LOG_DIR/video-generator.log" 2>&1
}

# 啟動時立即執行一次
run_news_collection
sleep 5
run_video_generation

# 然後定時執行
COUNTER=0
while true; do
  sleep 60

  COUNTER=$((COUNTER + 1))

  # 每小時執行新聞收集 (60 分鐘)
  if [ $((COUNTER % 60)) -eq 0 ]; then
    run_news_collection
  fi

  # 每 6 小時執行視頻生成 (360 分鐘)
  if [ $((COUNTER % 360)) -eq 0 ]; then
    run_video_generation
    COUNTER=0
  fi
done
