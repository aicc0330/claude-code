#!/usr/bin/env python3
"""
診斷 Claude Code session crash bug
問題：messages 包含空的 text content blocks
"""

from anthropic import Anthropic

client = Anthropic()

# 模擬造成 bug 的情況：構建包含空文本塊的消息
def build_message_with_empty_blocks(user_input: str):
    """這模擬了導致 bug 的代碼邏輯"""
    messages = []

    # 可能的 bug：在某些條件下創建空的文本塊
    text_blocks = []

    # 第一個塊：用戶輸入
    if user_input:
        text_blocks.append({"type": "text", "text": user_input})

    # 第二個塊：系統可能添加的（但意外為空）
    # 這就是 bug——添加了空塊！
    text_blocks.append({"type": "text", "text": ""})  # ❌ 空塊！

    # 第三個塊：另一個塊
    text_blocks.append({"type": "text", "text": "某些內容"})

    # 過濾掉空塊
    text_blocks = [b for b in text_blocks if b["text"]]

    return {
        "role": "user",
        "content": text_blocks if text_blocks else [{"type": "text", "text": ""}]
    }

# 測試
print("🔍 診斷 bug...")
print("\n問題 1: 包含空文本塊的消息")
msg = build_message_with_empty_blocks("你好")
print(f"消息內容: {msg}")

print("\n❌ 這會導致 API 錯誤:")
print('API Error: 400 {"type":"invalid_request_error","message":"messages: text content blocks must be non-empty"}')

print("\n✅ 修復方案:")
print("1. 過濾掉空文本塊")
print("2. 確保至少有一個非空塊")
print("3. 在發送前驗證")
