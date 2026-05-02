#!/usr/bin/env python3
"""
Claude Code - 修復後的集成實現
展示如何使用消息驗證器防止 session 崩潰
"""

from anthropic import Anthropic
from message_validator import validate_messages

class FixedClaudeCodeSession:
    """修復後的 Claude Code Session 實現"""

    def __init__(self, model="claude-3-5-sonnet-20241022"):
        self.client = Anthropic()
        self.model = model
        self.messages = []

    def add_user_message(self, content: str) -> None:
        """添加用戶消息（帶驗證）"""
        if not content or not content.strip():
            raise ValueError("消息內容不能為空")

        self.messages.append({
            "role": "user",
            "content": content.strip()
        })

    def add_assistant_message(self, content: str) -> None:
        """添加助手消息（帶驗證）"""
        if not content or not content.strip():
            raise ValueError("消息內容不能為空")

        self.messages.append({
            "role": "assistant",
            "content": content.strip()
        })

    def send_message(self, user_input: str) -> str:
        """
        發送消息並獲得回應
        ✅ 關鍵修復：在發送前驗證所有消息
        """
        # 1. 添加用戶消息
        self.add_user_message(user_input)

        # 2. 驗證消息（移除空塊，確保有效）
        try:
            validated_messages = validate_messages(self.messages)
        except ValueError as e:
            # 如果驗證失敗，回滾最後的消息
            self.messages.pop()
            raise ValueError(f"消息驗證失敗: {e}")

        # 3. 安全地發送到 API
        try:
            response = self.client.messages.create(
                model=self.model,
                messages=validated_messages,
                max_tokens=8096
            )

            assistant_message = response.content[0].text
            self.add_assistant_message(assistant_message)

            return assistant_message

        except Exception as e:
            # 如果 API 調用失敗，回滾消息
            self.messages.pop()
            raise RuntimeError(f"API 調用失敗: {e}")

    def get_conversation(self) -> list:
        """獲取整個對話歷史"""
        return self.messages

    def clear_history(self) -> None:
        """清空對話歷史"""
        self.messages = []


# 使用示例
if __name__ == "__main__":
    print("🚀 Claude Code - 修復後的 Session\n")

    session = FixedClaudeCodeSession()

    # 測試 1: 正常對話
    print("測試 1: 正常對話")
    try:
        response = session.send_message("請介紹一下自己")
        print(f"✅ 回應: {response[:50]}...\n")
    except Exception as e:
        print(f"❌ 錯誤: {e}\n")

    # 測試 2: 驗證拒絕空消息
    print("測試 2: 拒絕空消息")
    try:
        session.send_message("")
        print("❌ 不應該到達這裡\n")
    except ValueError as e:
        print(f"✅ 正確拒絕: {e}\n")

    # 測試 3: 多輪對話
    print("測試 3: 多輪對話（不實際調用 API）")
    session.clear_history()
    session.add_user_message("你好")
    session.add_assistant_message("你好！很高興認識你。")
    session.add_user_message("你能做什麼？")

    print(f"✅ 對話歷史: {len(session.get_conversation())} 條消息")
    for msg in session.get_conversation():
        print(f"  {msg['role']}: {msg['content'][:30]}...")

    print("\n✅ 修復完成！Session 現在穩定可靠。")
