#!/bin/bash
set -euo pipefail

# Session Start Hook - 自動加載 Claude 記憶系統
# 此腳本在每次 Claude Code 會話啟動時執行

# 同步模式：確保記憶已加載後才啟動會話
echo '{"async": false}'

# ===== 記憶系統初始化 =====

MEMORY_FILE="/home/user/CLAUDE_MEMORY.json"
ENV_FILE="${CLAUDE_ENV_FILE:-/tmp/claude-env}"

# 檢查記憶檔案是否存在
if [ ! -f "$MEMORY_FILE" ]; then
    echo "[WARNING] 記憶檔案不存在: $MEMORY_FILE"
    exit 0
fi

# 驗證JSON格式
if ! jq empty "$MEMORY_FILE" 2>/dev/null; then
    echo "[ERROR] 記憶檔案格式無效"
    exit 1
fi

# 提取關鍵信息
OWNER=$(jq -r '.identity.owner' "$MEMORY_FILE")
PRIMARY_GOAL=$(jq -r '.core_goals.primary' "$MEMORY_FILE")
PERSONALITY=$(jq -r '.identity.personality' "$MEMORY_FILE")

# 將記憶信息寫入環境檔案供會話使用
{
    echo "export CLAUDE_MEMORY_FILE='$MEMORY_FILE'"
    echo "export CLAUDE_OWNER='$OWNER'"
    echo "export CLAUDE_PRIMARY_GOAL='$PRIMARY_GOAL'"
    echo "export CLAUDE_PERSONALITY='$PERSONALITY'"
} >> "$ENV_FILE"

# 驗證寫入成功
if grep -q "CLAUDE_MEMORY_FILE" "$ENV_FILE"; then
    echo "[OK] 記憶系統已加載"
else
    echo "[ERROR] 記憶系統加載失敗"
    exit 1
fi

# ===== 系統驗證 =====

# 檢查 Claude Code 版本
if command -v claude &> /dev/null; then
    echo "[OK] Claude CLI 可用"
else
    echo "[WARNING] Claude CLI 未找到"
fi

# 檢查 git 狀態
if [ -d ".git" ]; then
    BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    echo "[OK] Git 分支: $BRANCH"
fi

exit 0
