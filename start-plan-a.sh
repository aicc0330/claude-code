#!/bin/bash

# 計畫 A：本地 Web 介面包裝本地 CLI
# 無需遠端 API，所有資料存儲在本地

echo "🚀 啟動計畫 A - 本地對話系統"
echo "================================"

# 確保本地資料目錄存在
mkdir -p /home/user/claude-code/local-data/{conversations,system-state,cache}
echo "✓ 本地資料目錄已準備"

# 確保 public 目錄存在
mkdir -p /home/user/claude-code/public
echo "✓ 公開資源目錄已準備"

# 確認 claude CLI 可用
if ! command -v claude &> /dev/null; then
  echo "⚠️ 警告：找不到 claude CLI"
  echo "請確保 /opt/node22/bin/claude 已安裝"
  exit 1
fi
echo "✓ Claude CLI 可用"

# 編譯 TypeScript
echo ""
echo "編譯 TypeScript..."
cd /home/user/claude-code
npm run build 2>/dev/null || {
  echo "⚠️ 編譯失敗，嘗試直接運行..."
}

# 啟動本地 API 伺服器
echo ""
echo "🌐 啟動本地 API 伺服器..."
LOCAL_API_PORT=3001 npx ts-node src/local-api-server.ts &
LOCAL_API_PID=$!

# 等待伺服器啟動
sleep 2

if ps -p $LOCAL_API_PID > /dev/null 2>&1; then
  echo "✓ 本地 API 伺服器運行中 (PID: $LOCAL_API_PID)"
  echo ""
  echo "================================"
  echo "計畫 A 已啟動！"
  echo "================================"
  echo ""
  echo "📱 網頁介面: http://localhost:3001"
  echo "🗂️ 資料存儲: /home/user/claude-code/local-data/"
  echo "💾 對話紀錄: /home/user/claude-code/local-data/conversations/"
  echo "🔧 系統狀態: /home/user/claude-code/local-data/system-state/"
  echo ""
  echo "已停止依賴遠端 API！所有資料本地存儲。"
  echo ""
  echo "按 Ctrl+C 停止伺服器..."
  echo ""

  # 保持進程運行
  wait $LOCAL_API_PID
else
  echo "❌ 啟動失敗"
  exit 1
fi
