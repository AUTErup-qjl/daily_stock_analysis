#!/usr/bin/env python3
"""快速测试您提供的 Webhook URL"""
import os
import json
import requests
import hmac
import hashlib
import base64
import time
from datetime import datetime

webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/fe8adb37-c0a0-469b-9909-eabc591aa8b9"

print("\n" + "=" * 70)
print("🚀 飞书 Webhook 快速验证测试")
print("=" * 70)

print("\n📌 配置信息:")
print(f"   URL: {webhook_url}")
print(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

timestamp = str(int(time.time()))

payload = {
    "timestamp": timestamp,
    "sign": "",
    "msg_type": "text",
    "content": {
        "text": "🧪 飞书 Webhook 验证测试\n\n验证时间: {}\n状态: ✅ 连接成功\n\n如在飞书群内看到此消息，说明 Webhook URL 配置正确！".format(
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
    }
}

print("\n📤 发送测试消息...")
print(f"   消息类型: text")
print(f"   消息内容: {payload['content']['text'][:50]}...")

try:
    response = requests.post(
        webhook_url,
        json=payload,
        timeout=10,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"\n📊 响应结果:")
    print(f"   HTTP 状态码: {response.status_code}")
    print(f"   响应体: {response.text}")
    
    if response.status_code == 200:
        resp_data = response.json()
        code = resp_data.get('code', -1)
        
        if code == 0:
            print("\n" + "🎉" * 35)
            print("✅✅✅ Webhook URL 验证成功！✅✅✅")
            print("🎉" * 35)
            print("\n✨ 下一步操作:")
            print("   1. ✅ 检查飞书群是否已收到测试消息")
            print("   2. ✅ 在 GitHub 中配置 Secret: FEISHU_WEBHOOK_URL")
            print("   3. ✅ 运行 'python main.py' 进行分析")
        else:
            print(f"\n❌ 飞书返回错误 (code={code})")
            print(f"   信息: {resp_data.get('msg', 'Unknown error')}")
    else:
        print(f"\n❌ HTTP 请求失败 (状态码: {response.status_code})")

except Exception as e:
    print(f"\n❌ 请求异常: {type(e).__name__}: {e}")
