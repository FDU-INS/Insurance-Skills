#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
行业数据接口模块
用于获取保险行业统计数据、费率参考数据等
"""

import json
import requests
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class IndustryData:
    """行业数据结构"""
    data_type: str
    year: int
    category: str
    value: float
    unit: str
    source: str

class IndustryDataAPI:
    """行业数据API接口"""
    
    def __init__(self):
        self.base_url = "https://api.example.com/insurance"  # 示例URL
        self.api_key = None
        self.mock_data = self._load_mock_data()
    
    def _load_mock_data(self) -> Dict:
        """加载模拟数据（实际使用时替换为真实API）"""
        return {
            "premium_data": {
                "2023": {
                    "财产险": {
                        "总保费": 1360.0,  # 亿元
                        "企业财产险": 180.0,
                        "工程险": 120.0,
                        "货运险": 80.0,
                        "责任险": 200.0,
                        "农业险": 550.0,
                        "其他": 230.0
                    },
                    "赔付率": {
                        "财产基本险": 0.45,
                        "财产综合险": 0.52,
                        "财产一切险": 0.58,
                        "公众责任险": 0.48,
                        "雇主责任险": 0.55,
                        "产品责任险": 0.42
                    }
                }
            },
            "rate_reference": {
                "财产基本险": {"min": 0.5, "avg": 1.0, "max": 1.5},
                "财产综合险": {"min": 1.0, "avg": 2.0, "max": 3.0},
                "财产一切险": {"min": 2.0, "avg": 3.5, "max": 5.0},
                "公众责任险": {"min": 0.3, "avg": 0.8, "max": 2.0},
                "雇主责任险": {"min": 0.5, "avg": 1.0, "max": 2.0},
                "产品责任险": {"min": 0.2, "avg": 0.6, "max": 1.5}
            },
            "loss_cost": {
                "制造业": {"fire": 0.8, "natural": 1.2},
                "商业": {"fire": 0.6, "natural": 0.9},
                "仓储": {"fire": 1.5, "natural": 1.0},
                "建筑": {"fire": 0.7, "natural": 1.5}
            }
        }
    
    def set_api_key(self, api_key: str):
        """设置API密钥"""
        self.api_key = api_key
    
    def get_premium_statistics(self, year: int, category: str = None) -> Dict:
        """获取保费统计数据"""
        # 实际使用时调用真实API
        # response = requests.get(f"{self.base_url}/premium/{year}")
        # return response.json()
        
        data = self.mock_data.get("premium_data", {}).get(str(year), {})
        if category:
            return data.get(category, {})
        return data
    
    def get_loss_ratio_reference(self, product_type: str) -> Dict:
        """获取赔付率参考数据"""
        year_data = self.mock_data.get("premium_data", {}).get("2023", {})
        return year_data.get("赔付率", {}).get(product_type, 0.50)
    
    def get_rate_reference(self, product_type: str) -> Dict:
        """获取费率参考区间"""
        return self.mock_data.get("rate_reference", {}).get(product_type, {})
    
    def get_loss_cost_by_industry(self, industry: str, peril: str = None) -> Dict:
        """获取行业损失成本数据"""
        data = self.mock_data.get("loss_cost", {}).get(industry, {})
        if peril:
            return {peril: data.get(peril, 1.0)}
        return data
    
    def get_market_competitiveness(self, product_type: str) -> Dict:
        """获取市场竞争度数据"""
        # 模拟市场竞争度数据
        competitiveness = {
            "财产基本险": {"players": 50, "concentration": "低", "price_competition": "激烈"},
            "财产综合险": {"players": 45, "concentration": "中", "price_competition": "较激烈"},
            "财产一切险": {"players": 30, "concentration": "中", "price_competition": "中等"},
            "公众责任险": {"players": 40, "concentration": "低", "price_competition": "激烈"},
            "雇主责任险": {"players": 35, "concentration": "中", "price_competition": "中等"},
            "产品责任险": {"players": 25, "concentration": "高", "price_competition": "温和"}
        }
        return competitiveness.get(product_type, {})


def main():
    """测试接口"""
    api = IndustryDataAPI()
    
    print("=" * 60)
    print("行业数据接口测试")
    print("=" * 60)
    
    # 获取保费统计
    print("\n1. 2023年财产险保费统计:")
    premium_data = api.get_premium_statistics(2023, "财产险")
    for category, value in premium_data.items():
        print(f"  {category}: {value}亿元")
    
    # 获取赔付率参考
    print("\n2. 各险种赔付率参考:")
    products = ["财产基本险", "财产综合险", "公众责任险", "雇主责任险"]
    for product in products:
        loss_ratio = api.get_loss_ratio_reference(product)
        print(f"  {product}: {loss_ratio:.1%}")
    
    # 获取费率参考
    print("\n3. 财产综合险费率参考:")
    rate_ref = api.get_rate_reference("财产综合险")
    print(f"  最低: {rate_ref.get('min', 0)}‰")
    print(f"  平均: {rate_ref.get('avg', 0)}‰")
    print(f"  最高: {rate_ref.get('max', 0)}‰")
    
    # 获取行业损失成本
    print("\n4. 制造业损失成本:")
    loss_cost = api.get_loss_cost_by_industry("制造业")
    for peril, cost in loss_cost.items():
        print(f"  {peril}: {cost}")


if __name__ == "__main__":
    main()
