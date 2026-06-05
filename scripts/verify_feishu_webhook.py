#!/usr/bin/env python3
"""
飞书 Webhook URL 快速验证工具
直接测试提供的 Webhook URL 是否可用
"""

import os
import json
import requests
import hmac
import hashlib
import base64
import time
from datetime import datetime

def verify_feishu_webhook(webhook_url, webhook_secret=None, webhook_keyword=None):
    """验证飞书 Webhook URL"""
    
    print("\n" + "=" * 70)
    print("🔍 飞书 Webhook URL 快速验证")
    print("=" * 70)
    
    # 1. URL 验证
    print("\n📌 第 1 步: URL 格式验证")
    print("-" * 70)
    
    if not webhook_url:
        print("❌ 错误: Webhook URL 为空")
        return False
    
    print(f"URL: {webhook_url}")
    
    if not webhook_url.startswith('https://open.feishu.cn/open-apis/bot/v2/hook/'):
        print("⚠️  警告: URL 格式可能不正确")
        print("   标准格式: https://open.feishu.cn/open-apis/bot/v2/hook/[token]")
    else:
        print("✅ URL 格式正确")
    
    # 2. 签名配置
    print("\n📌 第 2 步: 签名配置检查")
    print("-" * 70)
    
    timestamp = str(int(time.time()))
    sign = ""
    
    if webhook_secret:
        string_to_sign = f"{timestamp}\n{webhook_secret}"
        sign = base64.b64encode(
            hmac.new(
                string_to_sign.encode(),
                digestmod=hashlib.sha256
            ).digest()
        ).decode()
        print("✅ 已配置签名校验")
        print(f"   Secret: {webhook_secret[:20]}...")
    else:
        print("⏭️  未配置签名校验（可选）")
    
    # 3. 消息构建
    print("\n📌 第 3 步: 构建测试消息")
    print("-" * 70)
    
    message_text = "🧪 飞书 Webhook 验证测试"
    
    if webhook_keyword:
        message_text = f"{webhook_keyword}\n{message_text}"
        print(f"✅ 已添加关键词: {webhook_keyword}")
    
    message_text += f"\n\n验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    message_text += "\n状态: 连接成功测试"
    message_text += "\n✅ 如在飞书群内看到此消息，说明 Webhook 配置正确！"
    
    print(f"消息内容:\n{message_text}")
    
    # 4. 发送请求
    print("\n📌 第 4 步: 发送 HTTP 请求")
    print("-" * 70)
    
    payload = {
        "timestamp": timestamp,
        "sign": sign,
        "msg_type": "text",
        "content": {
            "text": message_text
        }
    }
    
    print(f"请求方法: POST")
    print(f"目标 URL: {webhook_url}")
    print(f"请求体大小: {len(json.dumps(payload))} 字节")
    
    try:
        print("\n⏳ 正在发送请求...")
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=10,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"\n📊 HTTP 响应")
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应体: {response.text}")
        
        # 5. 响应解析
        print("\n📌 第 5 步: 响应结果分析")
        print("-" * 70)
        
        if response.status_code == 200:
            try:
                resp_json = response.json()
                code = resp_json.get('code', -1)
                msg = resp_json.get('msg', '')
                
                print(f"返回代码: {code}")
                print(f"返回消息: {msg}")
                
                if code == 0:
                    print("\n" + "🎉" * 35)
                    print("✅ 飞书 Webhook URL 验证成功！")
                    print("🎉" * 35)
                    print("\n✨ 下一步:")
                    print("   1. 检查飞书群是否已收到测试消息")
                    print("   2. 在 GitHub 中正式配置 FEISHU_WEBHOOK_URL Secret")
                    print("   3. 运行 'python main.py' 进行完整分析")
                    return True
                else:
                    print("\n❌ 飞书返回错误")
                    print(f"   错误代码: {code}")
                    print(f"   错误信息: {msg}")
                    
                    # 错误诊断
                    print("\n🔧 错误诊断:")
                    error_map = {
                        19001: ("消息格式错误", "检查消息 JSON 结构"),
                        19002: ("Webhook URL 无效", "检查 URL 是否完整"),
                        19003: ("签名验证失败", "检查 Secret 是否正确"),
                        99991403: ("IP 白名单限制", "检查机器人 IP 白名单")
                    }
                    
                    if code in error_map:
                        title, solution = error_map[code]
                        print(f"   问题: {title}")
                        print(f"   解决: {solution}")
                    
                    return False
            except json.JSONDecodeError:
                print(f"\n❌ 无法解析 JSON 响应")
                print(f"   原始响应: {response.text}")
                return False
        else:
            print(f"\n❌ HTTP 请求失败")
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 404:
                print("   💡 可能原因: URL 不存在或已过期")
                print("      重新复制飞书机器人的 Webhook URL")
            elif response.status_code == 403:
                print("   💡 可能原因: 禁止访问（IP 白名单、安全设置等）")
                print("      检查飞书机器人的安全设置")
            elif response.status_code == 500:
                print("   💡 可能原因: 飞书服务器错误")
                print("      稍后重试")
            
            return False
    
    except requests.exceptions.Timeout:
        print(f"\n❌ 连接超时（10秒）")
        print("   可能原因:")
        print("   - 网络连接问题")
        print("   - 飞书服务暂时不可用")
        print("   - 防火墙阻止")
        return False
    
    except requests.exceptions.ConnectionError as e:
        print(f"\n❌ 连接错误: {e}")
        print("   可能原因:")
        print("   - 网络无法访问")
        print("   - URL 格式错误")
        return False
    
    except Exception as e:
        print(f"\n❌ 未知错误: {type(e).__name__}: {e}")
        return False


if __name__ == '__main__':
    import sys
    
    # 从命令行参数或环境变量读取配置
    webhook_url = os.getenv('FEISHU_WEBHOOK_URL', '').strip()
    webhook_secret = os.getenv('FEISHU_WEBHOOK_SECRET', '').strip() or None
    webhook_keyword = os.getenv('FEISHU_WEBHOOK_KEYWORD', '').strip() or None
    
    # 也支持直接传入 URL
    if len(sys.argv) > 1:
        webhook_url = sys.argv[1]
    
    if not webhook_url:
        print("❌ 错误: 未提供 Webhook URL")
        print("\n使用方法:")
        print("  1. 环境变量: FEISHU_WEBHOOK_URL=<url> python scripts/verify_feishu_webhook.py")
        print("  2. 直接参数: python scripts/verify_feishu_webhook.py <url>")
        sys.exit(1)
    
    success = verify_feishu_webhook(webhook_url, webhook_secret, webhook_keyword)
    sys.exit(0 if success else 1)
