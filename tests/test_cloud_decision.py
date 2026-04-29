import sys
import os

# 添加当前目录到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cloud_agent import CloudDecisionAgent

def test_cloud_decision():
    """测试云端决策功能"""
    print("🚀 开始测试云端决策功能...")
    
    try:
        # 创建云端决策代理
        agent = CloudDecisionAgent()
        
        # 验证 API Key 是否加载成功
        if not agent.api_key:
            print("❌ API Key 未加载成功，请检查 .env 文件配置")
            return False
        
        print(f"✅ API Key 加载成功")
        print(f"✅ API URL: {agent.api_url}")
        print(f"✅ 模型: {agent.model}")
        
        # 构建测试游戏状态
        test_state = {
            "current_state": "idle",
            "match_results": {
                "battle": {"found": False, "confidence": 0.3},
                "pickup": {"found": False, "confidence": 0.0},
                "pathfind": {"found": True, "confidence": 0.7}
            },
            "failed_attempts": 0,
            "time_elapsed": 120
        }
        
        print("\n📊 测试游戏状态:")
        print(f"  当前状态: {test_state['current_state']}")
        print(f"  战斗检测: {test_state['match_results']['battle']}")
        print(f"  拾取检测: {test_state['match_results']['pickup']}")
        print(f"  寻路检测: {test_state['match_results']['pathfind']}")
        print(f"  失败次数: {test_state['failed_attempts']}")
        print(f"  运行时间: {test_state['time_elapsed']}秒")
        
        print("\n🌐 正在请求云端决策...")
        # 获取云端决策
        decision = agent.get_decision(test_state)
        
        print(f"✅ 云端决策响应:")
        print(f"  动作: {decision.get('action', 'unknown')}")
        print(f"  原因: {decision.get('reason', '无')}")
        
        if decision and "action" in decision:
            print("\n🎉 云端决策功能测试成功！")
            return True
        else:
            print("\n❌ 云端决策功能测试失败：未获取到有效决策")
            return False
            
    except Exception as e:
        print(f"\n❌ 测试异常: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_cloud_decision()
    sys.exit(0 if success else 1)
