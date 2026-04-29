#!/usr/bin/env python3
"""
测试 MCP 服务器是否正常运行
"""

import requests
import time

def test_mcp_status():
    """测试 MCP 服务状态"""
    url = "http://localhost:8000/mcp/status"
    print(f"测试 MCP 服务状态: {url}")
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            status = response.json()
            print("✅ MCP 服务正常运行！")
            print(f"   状态: {status.get('status')}")
            print(f"   时间戳: {time.ctime(status.get('timestamp', time.time()))}")
            print(f"   纠正指令数: {status.get('correction_count', 0)}")
            print(f"   学习数据数: {status.get('learning_count', 0)}")
            return True
        else:
            print(f"❌ MCP 服务返回错误状态码: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到 MCP 服务，请检查服务是否启动")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False

def test_get_correction():
    """测试获取纠正指令"""
    url = "http://localhost:8000/mcp/get_correction"
    print(f"\n测试获取纠正指令: {url}")
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            correction = response.json()
            print("✅ 获取纠正指令成功！")
            print(f"   响应: {correction}")
            return True
        else:
            print(f"❌ 获取纠正指令失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== MCP 服务测试 ===")
    
    # 测试服务状态
    status_ok = test_mcp_status()
    
    # 如果服务正常，测试获取纠正指令
    if status_ok:
        test_get_correction()
    
    print("\n=== 测试完成 ===")
