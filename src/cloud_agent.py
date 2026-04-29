import requests
import json
import os
import re
from dotenv import load_dotenv

load_dotenv()


class CloudDecisionAgent:
    """云端决策代理（增强版）"""

    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_AUTH_TOKEN")
        self.api_url = os.getenv("ANTHROPIC_BASE_URL", "https://dashscope.aliyuncs.com/apps/anthropic")
        self.model = os.getenv("ANTHROPIC_MODEL", "qwen3-max")
        # 新增：JSON提取正则（匹配最外层{}）
        self.json_pattern = re.compile(r'\{.*\}', re.DOTALL)

    def _extract_json(self, text: str) -> dict:
        """从任意文本中提取JSON（三重保障）"""
        # 保障1：尝试直接解析
        try:
            return json.loads(text)
        except:
            pass

        # 保障2：移除Markdown代码块标记
        text = re.sub(r'```json\s*|\s*```', '', text)

        # 保障3：用正则提取第一个JSON对象
        match = self.json_pattern.search(text)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass

        # 保障4：尝试清理常见干扰字符
        cleaned = re.sub(r'^[^{]*|[^}]*$', '', text).strip()
        if cleaned.startswith('{') and cleaned.endswith('}'):
            try:
                return json.loads(cleaned)
            except:
                pass

        return None

    def get_decision(self, game_state: dict) -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # 【关键】强化系统提示词：要求纯JSON + 禁止任何额外内容
        payload = {
            "model": self.model,
            "input": {
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "你是一个严格的游戏决策引擎。"
                            "仅返回纯JSON对象，格式：{\"action\": \"explore|battle|pathfind|wait|adjust_parameters\", \"reason\": \"简短原因\"}。"
                            "禁止任何解释、Markdown、代码块或其他文本。"
                            "action必须是枚举值之一。"
                        )
                    },
                    {
                        "role": "user",
                        "content": f"当前游戏状态：{json.dumps(game_state, ensure_ascii=False)}"
                    }
                ]
            },
            "parameters": {
                "max_tokens": 100,
                "temperature": 0.1
            }
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            result = response.json()

            # 提取模型回复内容
            if "output" in result and "choices" in result["output"]:
                content = result["output"]["choices"][0]["message"]["content"].strip()

                # 【关键】尝试提取JSON
                decision = self._extract_json(content)
                if decision and "action" in decision and "reason" in decision:
                    return decision
                else:
                    # 调试日志（开发阶段可保留）
                    print(f"[DEBUG] 原始回复: {content[:200]}...")  # 仅打印前200字符
                    return {
                        "action": "continue",
                        "reason": f"解析失败（内容非纯JSON）"
                    }
            else:
                return {"action": "continue", "reason": "API响应结构异常"}

        except requests.exceptions.Timeout:
            return {"action": "continue", "reason": "API超时"}
        except Exception as e:
            return {"action": "continue", "reason": f"API异常: {str(e)[:50]}"}
