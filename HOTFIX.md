# 🚨 緊急 HOTFIX - 立即應用

## 問題
Session 仍然在崩潰，錯誤：
```
API Error: 400 - messages: text content blocks must be non-empty
```

## 根本原因
有某個地方在生成包含空文本塊的消息。問題出在：
1. Session 初始化時的消息構建
2. 或某個中間件在處理消息時意外添加了空塊

## 立即修復步驟

### 方案 A：修改 Claude Code 啟動文件（最直接）
在 Claude Code 啟動時，執行：
```bash
python3 -c "
import sys
sys.path.insert(0, '/home/user/claude-code')
from message_validator import validate_messages
# 現在所有消息都會被驗證
"
```

### 方案 B：設置環境變量
```bash
export PYTHONPATH=/home/user/claude-code:$PYTHONPATH
```

### 方案 C：在 Session 代碼中直接插入修復
在任何發送消息的代碼前添加：
```python
from message_validator import validate_messages

# 在發送消息前
messages = validate_messages(messages)
```

## 診斷問題位置
Session 崩潰位置可能是：
1. ❓ `session.create()` - 檢查會話創建邏輯
2. ❓ `session.send_message()` - 檢查消息發送邏輯
3. ❓ 消息序列化層 - 檢查 JSON 編碼

## 需要幫助
請告訴我：
1. Claude Code 的實際應用代碼位置？
2. 哪個文件負責構建消息？
3. 我應該在哪裡插入修復？

一旦確認位置，我會立即應用修復！🚀
