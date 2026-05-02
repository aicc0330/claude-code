#!/usr/bin/env python3
"""
修復 Claude Code session crash bug
問題根源：empty text content blocks
解決方案：在發送前驗證和清潔消息
"""

from typing import Any, Dict, List


def validate_message_content(content: Any) -> List[Dict[str, str]]:
    """
    驗證並清潔消息內容
    移除所有空的文本塊，確保消息有效
    """
    if isinstance(content, str):
        # 如果是字符串，包裝成適當格式
        if not content.strip():
            raise ValueError("消息內容不能為空")
        return [{"type": "text", "text": content}]

    if isinstance(content, list):
        cleaned_blocks = []

        for block in content:
            # 跳過空塊
            if block.get("type") == "text":
                text = block.get("text", "").strip()
                if text:  # 只保留非空文本
                    cleaned_blocks.append({"type": "text", "text": text})
            else:
                # 保留非文本塊（圖片等）
                if block:
                    cleaned_blocks.append(block)

        if not cleaned_blocks:
            raise ValueError("消息必須至少包含一個非空內容塊")

        return cleaned_blocks

    raise ValueError(f"無效的消息內容類型: {type(content)}")


def validate_messages(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    驗證整個消息列表
    確保沒有空塊會被發送到 API
    """
    validated = []

    for msg in messages:
        if not msg.get("role"):
            raise ValueError("每個消息必須有 'role'")

        # 驗證內容
        content = msg.get("content")
        if not content:
            raise ValueError(f"消息缺少內容 (role: {msg['role']})")

        cleaned_content = validate_message_content(content)

        validated.append({
            "role": msg["role"],
            "content": cleaned_content
        })

    return validated


# 測試修復
if __name__ == "__main__":
    print("✅ 測試消息驗證...\n")

    # 測試 1: 包含空塊的消息
    print("測試 1: 移除空文本塊")
    content_with_empty = [
        {"type": "text", "text": "hello"},
        {"type": "text", "text": ""},  # 空塊
        {"type": "text", "text": "world"}
    ]
    result = validate_message_content(content_with_empty)
    print(f"輸入: {content_with_empty}")
    print(f"輸出: {result}")
    assert len(result) == 2, "應該只有 2 個塊"
    print("✓ 通過\n")

    # 測試 2: 整個消息列表
    print("測試 2: 驗證整個消息列表")
    messages = [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": [
            {"type": "text", "text": "你好！"},
            {"type": "text", "text": ""}  # 空塊
        ]}
    ]
    validated = validate_messages(messages)
    print(f"驗證後: {len(validated)} 個消息")
    assert validated[1]["content"][0]["text"] == "你好！"
    print("✓ 通過\n")

    # 測試 3: 拒絕完全空的消息
    print("測試 3: 拒絕空消息")
    try:
        validate_message_content("")
        print("✗ 失敗：應該拒絕")
    except ValueError as e:
        print(f"✓ 正確拒絕: {e}\n")

    print("🎉 所有測試通過！")
