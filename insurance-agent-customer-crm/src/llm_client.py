"""
LLM 客户端模块
"""
import json
import time
import requests
from typing import Dict, List, Any


class LLMClient:
    """LLM API 调用客户端"""

    def __init__(self, config):
        self.config = config
        self.api_key = config.api_key
        self.base_url = config.base_url.rstrip("/")
        self.model = config.model
        self.timeout = config.timeout
        self.max_retries = config.max_retries

    def chat(self, messages: List[Dict[str, str]]) -> str:
        """发送聊天请求到 LLM API"""
        url = f"{self.base_url}/text/chatcompletion_v2"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7
        }

        last_error = ""

        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=self.timeout
                )
                response.raise_for_status()

                result = response.json()

                if "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"]

                return "错误: 响应格式异常"

            except requests.exceptions.Timeout:
                last_error = f"请求超时 (尝试 {attempt + 1}/{self.max_retries})"
                print(f"   警告: {last_error}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)

            except requests.exceptions.RequestException as e:
                last_error = f"网络请求错误 (尝试 {attempt + 1}/{self.max_retries}): {e}"
                print(f"   警告: {last_error}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)

            except (KeyError, ValueError, json.JSONDecodeError) as e:
                last_error = f"响应解析错误: {e}"
                print(f"   警告: {last_error}")
                if attempt < self.max_retries - 1:
                    time.sleep(1)

            except Exception as e:
                last_error = f"未知错误: {e}"
                print(f"   错误: {last_error}")
                if attempt < self.max_retries - 1:
                    time.sleep(1)

        raise Exception(f"API 请求失败，已重试 {self.max_retries} 次。最后错误: {last_error}")

    def extract_info(self, prompt: str) -> Dict[str, Any]:
        """提取信息并返回 JSON 格式"""
        response = self.chat([{"role": "user", "content": prompt}])

        try:
            json_str = self._extract_json_from_response(response)
            return json.loads(json_str.strip())

        except json.JSONDecodeError as e:
            raise Exception(f"JSON 解析失败: {e}。原始响应: {response[:500]}")

    def _extract_json_from_response(self, response: str) -> str:
        """从响应中提取 JSON 字符串"""
        if "```json" in response:
            parts = response.split("```json")
            if len(parts) > 1:
                json_part = parts[1].split("```")[0]
                return json_part.strip()

        if "```" in response:
            parts = response.split("```")
            if len(parts) > 1:
                return parts[1].strip()

        return response.strip()
