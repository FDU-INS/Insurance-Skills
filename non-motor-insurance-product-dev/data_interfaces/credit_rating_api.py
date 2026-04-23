#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业信用评级接口模块
用于获取投保人/被保险人的信用评级数据
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class CreditRating:
    """信用评级数据"""
    entity_name: str
    credit_code: str
    rating_level: str  # AAA, AA, A, BBB, BB, B, CCC, CC, C, D
    rating_score: float  # 0-100
    rating_date: str
    rating_agency: str
    outlook: str  # 稳定、正面、负面、观察
    
    # 风险指标
    financial_risk: float  # 财务风险得分
    operational_risk: float  # 经营风险得分
    industry_risk: float  # 行业风险得分
    management_risk: float  # 管理风险得分
    
    # 历史记录
    default_history: List[Dict]  # 违约历史
    litigation_history: List[Dict]  # 诉讼历史
    penalty_history: List[Dict]  # 处罚历史


class CreditRatingAPI:
    """企业信用评级API接口"""
    
    def __init__(self):
        self.mock_database = self._load_mock_database()
    
    def _load_mock_database(self) -> Dict:
        """加载模拟信用评级数据库"""
        return {
            "91110000123456789X": {
                "entity_name": "某制造有限公司",
                "credit_code": "91110000123456789X",
                "rating_level": "AA",
                "rating_score": 85.5,
                "rating_date": "2023-12-01",
                "rating_agency": "中诚信",
                "outlook": "稳定",
                "financial_risk": 82.0,
                "operational_risk": 88.0,
                "industry_risk": 85.0,
                "management_risk": 87.0,
                "default_history": [],
                "litigation_history": [
                    {"date": "2022-03", "type": "合同纠纷", "status": "已结案", "amount": 500000}
                ],
                "penalty_history": []
            },
            "91110000987654321Y": {
                "entity_name": "某贸易有限公司",
                "credit_code": "91110000987654321Y",
                "rating_level": "BBB",
                "rating_score": 65.0,
                "rating_date": "2023-11-15",
                "rating_agency": "联合资信",
                "outlook": "负面",
                "financial_risk": 58.0,
                "operational_risk": 70.0,
                "industry_risk": 65.0,
                "management_risk": 67.0,
                "default_history": [
                    {"date": "2023-06", "type": "贷款逾期", "amount": 2000000, "status": "已清偿"}
                ],
                "litigation_history": [
                    {"date": "2023-01", "type": "债务纠纷", "status": "执行中", "amount": 1500000}
                ],
                "penalty_history": [
                    {"date": "2023-04", "type": "税务处罚", "amount": 50000}
                ]
            }
        }
    
    def query_credit_rating(self, credit_code: str) -> Optional[CreditRating]:
        """查询企业信用评级"""
        data = self.mock_database.get(credit_code)
        if not data:
            return None
        
        return CreditRating(
            entity_name=data["entity_name"],
            credit_code=data["credit_code"],
            rating_level=data["rating_level"],
            rating_score=data["rating_score"],
            rating_date=data["rating_date"],
            rating_agency=data["rating_agency"],
            outlook=data["outlook"],
            financial_risk=data["financial_risk"],
            operational_risk=data["operational_risk"],
            industry_risk=data["industry_risk"],
            management_risk=data["management_risk"],
            default_history=data["default_history"],
            litigation_history=data["litigation_history"],
            penalty_history=data["penalty_history"]
        )
    
    def get_rating_factor(self, rating_level: str) -> float:
        """获取评级系数（用于定价）"""
        rating_factors = {
            "AAA": 0.70,
            "AA": 0.80,
            "A": 0.90,
            "BBB": 1.00,
            "BB": 1.20,
            "B": 1.50,
            "CCC": 2.00,
            "CC": 2.50,
            "C": 3.00,
            "D": 5.00
        }
        return rating_factors.get(rating_level, 1.00)
    
    def assess_insurance_risk(self, credit_code: str) -> Dict:
        """评估保险承保风险"""
        rating = self.query_credit_rating(credit_code)
        if not rating:
            return {"error": "未找到该企业信用评级信息"}
        
        risk_assessment = {
            "基本信息": {
                "企业名称": rating.entity_name,
                "信用代码": rating.credit_code,
                "信用等级": rating.rating_level,
                "评级得分": rating.rating_score,
                "评级展望": rating.outlook
            },
            "风险评分": {
                "财务风险": rating.financial_risk,
                "经营风险": rating.operational_risk,
                "行业风险": rating.industry_risk,
                "管理风险": rating.management_risk,
                "综合得分": rating.rating_score
            },
            "承保建议": {
                "风险等级": self._get_risk_category(rating.rating_level),
                "费率调整系数": self.get_rating_factor(rating.rating_level),
                "承保条件": self._get_underwriting_conditions(rating),
                "特别关注": self._get_special_attention(rating)
            },
            "历史记录": {
                "违约记录": len(rating.default_history),
                "诉讼记录": len(rating.litigation_history),
                "处罚记录": len(rating.penalty_history)
            }
        }
        
        return risk_assessment
    
    def _get_risk_category(self, rating_level: str) -> str:
        """获取风险分类"""
        if rating_level in ["AAA", "AA"]:
            return "低风险"
        elif rating_level in ["A", "BBB"]:
            return "中风险"
        elif rating_level in ["BB", "B"]:
            return "高风险"
        else:
            return "极高风险"
    
    def _get_underwriting_conditions(self, rating: CreditRating) -> List[str]:
        """获取承保条件建议"""
        conditions = []
        
        if rating.rating_level in ["AAA", "AA"]:
            conditions.append("标准承保条件")
            conditions.append("可享受费率优惠")
        elif rating.rating_level in ["A", "BBB"]:
            conditions.append("标准承保条件")
        elif rating.rating_level in ["BB", "B"]:
            conditions.append("提高免赔额")
            conditions.append("增加费率上浮")
            conditions.append("加强风险查勘")
        else:
            conditions.append("谨慎承保")
            conditions.append("大幅提高免赔额")
            conditions.append("大幅费率上浮")
            conditions.append("要求提供担保")
        
        # 根据历史记录调整
        if rating.default_history:
            conditions.append("关注历史违约记录")
        if len(rating.litigation_history) > 2:
            conditions.append("诉讼较多，需法律尽调")
        
        return conditions
    
    def _get_special_attention(self, rating: CreditRating) -> List[str]:
        """获取特别关注事项"""
        attention = []
        
        if rating.outlook == "负面":
            attention.append("评级展望为负面，需密切关注经营状况")
        
        for default in rating.default_history:
            attention.append(f"历史违约记录: {default['date']} {default['type']}")
        
        for litigation in rating.litigation_history:
            if litigation["status"] == "执行中":
                attention.append(f"未决诉讼: {litigation['type']} 金额{litigation['amount']}元")
        
        return attention


def main():
    """测试接口"""
    api = CreditRatingAPI()
    
    print("=" * 60)
    print("企业信用评级接口测试")
    print("=" * 60)
    
    # 查询优质企业
    print("\n1. 查询优质企业(AA级):")
    credit_code = "91110000123456789X"
    rating = api.query_credit_rating(credit_code)
    if rating:
        print(f"  企业名称: {rating.entity_name}")
        print(f"  信用等级: {rating.rating_level}")
        print(f"  评级得分: {rating.rating_score}")
        print(f"  费率系数: {api.get_rating_factor(rating.rating_level)}")
    
    # 查询风险企业
    print("\n2. 查询风险企业(BBB级):")
    credit_code = "91110000987654321Y"
    assessment = api.assess_insurance_risk(credit_code)
    print(f"  企业名称: {assessment['基本信息']['企业名称']}")
    print(f"  风险等级: {assessment['承保建议']['风险等级']}")
    print(f"  承保条件:")
    for condition in assessment['承保建议']['承保条件']:
        print(f"    - {condition}")


if __name__ == "__main__":
    main()
