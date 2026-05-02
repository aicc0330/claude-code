# Claude Code - Session Crash Bug Fix

## 緊急修復：Session 崩潰問題

### 問題症狀
左邊 Recents 中的 Session 反覆崩潰：
- "Fix system crash issue" ❌ 崩潰
- "Fix neighbor's system crash issue" ❌ 崩潰

API 錯誤：
```
API Error: 400 - messages: text content blocks must be non-empty
```

### 根本原因
當 Claude Code 發送消息到 Claude API 時，消息中包含**空的文本塊**。即使用戶有提供內容，這些空塊也會導致 API 驗證失敗，進而使整個 Session 崩潰。

### 修復方案

#### 1. 使用 `message_validator.py`
```python
from message_validator import validate_messages

# 在所有 API 調用前驗證
messages = validate_messages(user_messages)
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=messages,  # 已清潔的消息
    max_tokens=8096
)
```

#### 2. 整合點
修改 Claude Code 核心初始化代碼：
- 在 `Session.create()` 時驗證消息
- 在 `Session.send_message()` 時驗證消息
- 在任何 API 調用前過濾空塊

#### 3. 測試驗證
✅ 移除空文本塊
✅ 驗證消息結構  
✅ 保留非空內容
✅ Session 不再崩潰

### 關鍵文件
- `message_validator.py` - 核心驗證邏輯
- `claude_code_integration.py` - 集成示例
- `diagnose_bug.py` - 問題診斷

### 預期效果
修復後：
- ✅ 兩個 Session 能正常運行
- ✅ 用戶內容正確傳遞
- ✅ 不再有空塊錯誤
- ✅ 系統穩定可靠

---

**優先級**：🔴 高 - 直接影響應用穩定性
**受影響範圍**：所有 Claude Code Sessions
**修復難度**：🟢 簡單 - 插入驗證層即可
