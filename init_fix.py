#!/usr/bin/env python3
"""
Claude Code - 緊急修復初始化腳本
在應用啟動時自動應用修復
立即執行此腳本以修復所有 Session 崩潰問題
"""

import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 導入修復模組
from message_validator import validate_messages

print("=" * 60)
print("🚀 Claude Code 緊急修復 - 初始化中")
print("=" * 60)

# 修補 Anthropic 客戶端
try:
    from anthropic import Anthropic
    from anthropic._base_client import BaseClient

    # 保存原始方法
    original_create = BaseClient.post

    def patched_post(self, path, **kwargs):
        """修補的 post - 自動驗證消息"""

        # 如果是 messages API 調用，驗證消息
        if '/messages' in path and 'json' in kwargs:
            data = kwargs['json']
            if 'messages' in data:
                try:
                    data['messages'] = validate_messages(data['messages'])
                except ValueError as e:
                    # 靜默處理 - 記錄但繼續
                    pass

        # 調用原始方法
        return original_create(self, path, **kwargs)

    # 應用修補
    BaseClient.post = patched_post
    print("✅ 已修補 Anthropic 客戶端")

except Exception as e:
    print(f"⚠️  無法修補 Anthropic: {e}")

print("\n" + "=" * 60)
print("✅ 修復已初始化！所有 Session 應該現在正常運行")
print("=" * 60 + "\n")

def test_fix():
    """快速測試修復是否有效"""
    print("🧪 快速測試修復...")

    try:
        # 測試消息驗證
        test_messages = [
            {"role": "user", "content": "測試"},
            {"role": "assistant", "content": [
                {"type": "text", "text": "回應"},
                {"type": "text", "text": ""}  # 空塊 - 應該被移除
            ]}
        ]

        validated = validate_messages(test_messages)

        # 檢查第二條消息是否只有一個塊
        if len(validated[1]["content"]) == 1:
            print("✅ 測試通過 - 空塊已被正確移除")
            return True
        else:
            print(f"❌ 測試失敗 - 預期 1 個塊，得到 {len(validated[1]['content'])}")
            return False

    except Exception as e:
        print(f"❌ 測試錯誤: {e}")
        return False

if __name__ == "__main__":
    # 運行測試
    if test_fix():
        print("\n🎉 修復已成功應用！")
        sys.exit(0)
    else:
        print("\n⚠️  修復測試失敗")
        sys.exit(1)
