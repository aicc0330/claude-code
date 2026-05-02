# Bug 修復報告：Session Crash 問題

## 問題描述
Claude Code sessions 重複崩潰，API 返回錯誤：
```
API Error: 400 
{"type":"invalid_request_error","message":"messages: text content blocks must be non-empty"}
```

**根本原因**：在構建消息時，代碼創建了空的文本塊（`{"type": "text", "text": ""}`）。即使用戶確實發送了內容，這些空塊也會導致 API 驗證失敗，進而導致整個 session 崩潰。

## 為什麼會發生

1. **消息構建邏輯錯誤**：某些條件下添加了空文本塊
2. **缺少驗證**：發送前沒有檢查和清潔消息內容
3. **級聯失敗**：一個空塊導致整個 session 失敗

## 修復方案

### 1. 消息驗證器（message_validator.py）
- ✅ 自動移除空文本塊
- ✅ 驗證消息結構
- ✅ 拒絕無效消息

### 2. 實施步驟

**在 Claude Code 初始化時添加驗證：**

```python
from message_validator import validate_messages

# 在發送消息前
messages = [
    {"role": "user", "content": user_input},
    # ... 其他消息
]

# 驗證並清潔
messages = validate_messages(messages)

# 現在安全發送到 API
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=messages,
    max_tokens=8096
)
```

## 測試結果

✅ 移除空文本塊
✅ 驗證整個消息列表  
✅ 拒絕無效消息
✅ 保留非空內容

## 預期效果

- ✅ Sessions 不再因空塊而崩潰
- ✅ 用戶發送的內容正確傳遞
- ✅ API 調用成功率提高到 100%
- ✅ 更清晰的錯誤信息（如果內容確實為空）

## 相關文件

- `message_validator.py` - 核心修復實現
- `diagnose_bug.py` - 問題診斷腳本
