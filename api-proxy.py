#!/usr/bin/env python3
"""
Claude API 代理 - 自動清理空文本塊
防止 session crash：在發送到 Claude API 前清潔所有消息
"""

import json
import sys
from typing import Any, Dict, List
from message_validator import validate_messages


class ClaudeAPIProxy:
    """攔截和清潔消息的 API 代理"""

    @staticmethod
    def clean_message_content(content: Any) -> Any:
        """清潔單個消息的內容"""
        if isinstance(content, str):
            return content.strip() if content else None

        if isinstance(content, list):
            cleaned = []
            for block in content:
                if isinstance(block, dict):
                    if block.get("type") == "text":
                        text = block.get("text", "").strip()
                        if text:  # 只保留非空文本
                            cleaned.append({"type": "text", "text": text})
                    else:
                        # 非文本塊直接保留
                        cleaned.append(block)
            return cleaned if cleaned else None

        return content

    @staticmethod
    def clean_messages(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """清潔整個消息列表"""
        cleaned = []

        for msg in messages:
            role = msg.get("role")
            content = msg.get("content")

            if not role:
                continue

            # 清潔內容
            cleaned_content = ClaudeAPIProxy.clean_message_content(content)

            if cleaned_content:
                cleaned.append({
                    "role": role,
                    "content": cleaned_content
                })

        return cleaned

    @staticmethod
    def intercept_messages_create(client, **kwargs):
        """攔截 client.messages.create() 調用"""
        messages = kwargs.get("messages", [])

        print(f"[API 代理] 收到 {len(messages)} 個消息", file=sys.stderr)

        # 清潔消息
        cleaned_messages = ClaudeAPIProxy.clean_messages(messages)

        print(f"[API 代理] 清潔後 {len(cleaned_messages)} 個消息", file=sys.stderr)

        # 驗證（額外安全）
        try:
            validated_messages = validate_messages(cleaned_messages)
            kwargs["messages"] = validated_messages
            print(f"[API 代理] ✅ 消息驗證通過", file=sys.stderr)
        except Exception as e:
            print(f"[API 代理] ❌ 驗證失敗: {e}", file=sys.stderr)
            raise

        # 實際發送
        return client._original_messages_create(**kwargs)


def patch_anthropic_client(client):
    """為 Anthropic 客户端打補丁"""
    # 保存原始方法
    client._original_messages_create = client.messages.create

    # 替換為我們的攔截版本
    def messages_create(**kwargs):
        return ClaudeAPIProxy.intercept_messages_create(client, **kwargs)

    client.messages.create = messages_create
    print("[API 代理] ✅ 已為客户端打補丁", file=sys.stderr)


# 使用示例
if __name__ == "__main__":
    from anthropic import Anthropic

    print("🔧 Claude API 代理測試\n")

    client = Anthropic()
    patch_anthropic_client(client)

    # 測試：發送包含空塊的消息（正常會失敗）
    print("測試：清潔消息並發送\n")

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": "你好"},
                    {"type": "text", "text": ""},  # ← 這會被自動移除
                    {"type": "text", "text": "世界"}
                ]}
            ],
            max_tokens=100
        )
        print(f"✅ 成功！回應: {response.content[0].text[:50]}...")
    except Exception as e:
        print(f"❌ 失敗: {e}")
