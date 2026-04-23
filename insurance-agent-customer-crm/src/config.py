"""
配置管理模块 - 用户 API Key 管理
"""
from typing import Optional

class SkillConfig:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.minimax.chat/v1",
        model: str = "MiniMax-M2.7",
        trigger_threshold: float = 0.5,
        min_table_rows: int = 3,
        timeout: int = 120,
        max_retries: int = 3,
        batch_size: int = 5
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.trigger_threshold = trigger_threshold
        self.min_table_rows = min_table_rows
        self.timeout = timeout
        self.max_retries = max_retries
        self.batch_size = batch_size
    
    def to_dict(self):
        return {
            "base_url": self.base_url,
            "model": self.model,
            "trigger_threshold": self.trigger_threshold,
            "min_table_rows": self.min_table_rows
        }
