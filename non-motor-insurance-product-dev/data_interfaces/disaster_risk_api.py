#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
灾害风险地图数据接口模块
用于查询自然灾害风险评估数据
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class NaturalDisasterRisk:
    """自然灾害风险"""
    region: str  # 地区
    disaster_type: str  # 灾害类型
    risk_level: str  # 风险等级: 极高/高/中/低
    risk_score: float  # 风险评分 0-100
    historical_frequency: str  # 历史频率
    max_loss_record: str  # 最大损失记录
    probability_10y: float  # 10年发生概率
    avg_annual_loss: float  # 年均损失率(‰)


class DisasterRiskAPI:
    """灾害风险地图API"""
    
    def __init__(self):
        self.risk_database = self._load_risk_database()
    
    def _load_risk_database(self) -> Dict:
        """加载灾害风险数据库"""
        return {
            "广东": {
                "台风": NaturalDisasterRisk(
                    region="广东", disaster_type="台风",
                    risk_level="极高", risk_score=92,
                    historical_frequency="年均3-5次",
                    max_loss_record="2018年台风'山竹'损失超200亿元",
                    probability_10y=0.95,
                    avg_annual_loss=8.5
                ),
                "暴雨洪涝": NaturalDisasterRisk(
                    region="广东", disaster_type="暴雨洪涝",
                    risk_level="高", risk_score=78,
                    historical_frequency="年均5-8次",
                    max_loss_record="2020年暴雨洪涝损失超50亿元",
                    probability_10y=0.90,
                    avg_annual_loss=5.2
                ),
                "地震": NaturalDisasterRisk(
                    region="广东", disaster_type="地震",
                    risk_level="中", risk_score=45,
                    historical_frequency="偶发",
                    max_loss_record="较小",
                    probability_10y=0.15,
                    avg_annual_loss=0.5
                )
            },
            "四川": {
                "地震": NaturalDisasterRisk(
                    region="四川", disaster_type="地震",
                    risk_level="极高", risk_score=95,
                    historical_frequency="频繁",
                    max_loss_record="2008年汶川地震损失超8400亿元",
                    probability_10y=0.85,
                    avg_annual_loss=12.0
                ),
                "暴雨洪涝": NaturalDisasterRisk(
                    region="四川", disaster_type="暴雨洪涝",
                    risk_level="高", risk_score=75,
                    historical_frequency="年均3-5次",
                    max_loss_record="2020年暴雨洪涝损失超30亿元",
                    probability_10y=0.80,
                    avg_annual_loss=4.5
                ),
                "山体滑坡": NaturalDisasterRisk(
                    region="四川", disaster_type="山体滑坡",
                    risk_level="高", risk_score=80,
                    historical_frequency="雨季频发",
                    max_loss_record="2017年茂县滑坡",
                    probability_10y=0.70,
                    avg_annual_loss=3.0
                )
            },
            "浙江": {
                "台风": NaturalDisasterRisk(
                    region="浙江", disaster_type="台风",
                    risk_level="高", risk_score=82,
                    historical_frequency="年均2-3次",
                    max_loss_record="2019年台风'利奇马'损失超100亿元",
                    probability_10y=0.88,
                    avg_annual_loss=6.0
                ),
                "暴雨洪涝": NaturalDisasterRisk(
                    region="浙江", disaster_type="暴雨洪涝",
                    risk_level="中", risk_score=60,
                    historical_frequency="年均2-4次",
                    max_loss_record="中等",
                    probability_10y=0.70,
                    avg_annual_loss=3.0
                )
            },
            "北京": {
                "暴雨洪涝": NaturalDisasterRisk(
                    region="北京", disaster_type="暴雨洪涝",
                    risk_level="中", risk_score=55,
                    historical_frequency="偶发",
                    max_loss_record="2012年7·21暴雨损失超100亿元",
                    probability_10y=0.40,
                    avg_annual_loss=1.5
                ),
                "地震": NaturalDisasterRisk(
                    region="北京", disaster_type="地震",
                    risk_level="中", risk_score=50,
                    historical_frequency="低频",
                    max_loss_record="1976年唐山地震影响",
                    probability_10y=0.20,
                    avg_annual_loss=1.0
                )
            },
            "新疆": {
                "地震": NaturalDisasterRisk(
                    region="新疆", disaster_type="地震",
                    risk_level="高", risk_score=85,
                    historical_frequency="较频繁",
                    max_loss_record="多次6级以上地震",
                    probability_10y=0.80,
                    avg_annual_loss=5.0
                ),
                "暴雪": NaturalDisasterRisk(
                    region="新疆", disaster_type="暴雪",
                    risk_level="高", risk_score=75,
                    historical_frequency="冬季频发",
                    max_loss_record="畜牧业损失严重",
                    probability_10y=0.85,
                    avg_annual_loss=3.5
                )
            }
        }
    
    def query_risk(self, region: str, disaster_type: str = None) -> Dict:
        """查询灾害风险"""
        region_data = self.risk_database.get(region)
        if not region_data:
            return {"error": f"未找到{region}地区的灾害数据"}
        
        if disaster_type:
            risk = region_data.get(disaster_type)
            if risk:
                return {
                    "地区": risk.region,
                    "灾害类型": risk.disaster_type,
                    "风险等级": risk.risk_level,
                    "风险评分": risk.risk_score,
                    "历史频率": risk.historical_frequency,
                    "最大损失记录": risk.max_loss_record,
                    "10年发生概率": f"{risk.probability_10y:.0%}",
                    "年均损失率": f"{risk.avg_annual_loss:.1f}‰"
                }
            return {"error": f"未找到{region}地区{disaster_type}的数据"}
        
        # 返回该地区所有灾害风险
        results = []
        for dtype, risk in region_data.items():
            results.append({
                "灾害类型": risk.disaster_type,
                "风险等级": risk.risk_level,
                "风险评分": risk.risk_score,
                "10年发生概率": f"{risk.probability_10y:.0%}",
                "年均损失率": f"{risk.avg_annual_loss:.1f}‰"
            })
        
        return {"地区": region, "灾害风险列表": results}
    
    def get_region_risk_factor(self, region: str, disaster_type: str) -> float:
        """获取地区风险系数（用于定价）"""
        risk_data = self.query_risk(region, disaster_type)
        if "error" in risk_data:
            return 1.0
        
        risk_score = risk_data.get("风险评分", 50)
        
        # 将风险评分转换为系数
        if risk_score >= 80:
            return 1.5
        elif risk_score >= 60:
            return 1.2
        elif risk_score >= 40:
            return 1.0
        else:
            return 0.9
    
    def get_composite_risk_factor(self, region: str) -> Dict:
        """获取综合风险系数"""
        region_data = self.risk_database.get(region)
        if not region_data:
            return {"综合风险系数": 1.0, "详情": "未找到数据，使用默认系数"}
        
        max_score = 0
        main_peril = ""
        total_avg_loss = 0
        count = 0
        
        for dtype, risk in region_data.items():
            if risk.risk_score > max_score:
                max_score = risk.risk_score
                main_peril = risk.disaster_type
            total_avg_loss += risk.avg_annual_loss
            count += 1
        
        avg_loss = total_avg_loss / count if count > 0 else 0
        
        # 综合系数
        if max_score >= 80:
            factor = 1.3 + avg_loss / 100
        elif max_score >= 60:
            factor = 1.1 + avg_loss / 100
        else:
            factor = 1.0 + avg_loss / 200
        
        return {
            "地区": region,
            "主要灾害": main_peril,
            "最高风险评分": max_score,
            "年均综合损失率": f"{avg_loss:.1f}‰",
            "综合风险系数": round(factor, 3)
        }


def main():
    """测试接口"""
    api = DisasterRiskAPI()
    
    print("=" * 60)
    print("灾害风险地图接口测试")
    print("=" * 60)
    
    # 查询地区综合风险
    print("\n1. 地区综合风险:")
    for region in ["广东", "四川", "浙江", "北京"]:
        result = api.get_composite_risk_factor(region)
        print(f"  {region}: 综合系数={result['综合风险系数']}, "
              f"主要灾害={result['主要灾害']}")
    
    # 查询特定灾害风险
    print("\n2. 四川地震风险详情:")
    risk = api.query_risk("四川", "地震")
    for key, value in risk.items():
        print(f"  {key}: {value}")
    
    # 查询地区所有灾害
    print("\n3. 广东所有灾害风险:")
    risks = api.query_risk("广东")
    for item in risks.get("灾害风险列表", []):
        print(f"  {item['灾害类型']}: {item['风险等级']}({item['风险评分']}分)")


if __name__ == "__main__":
    main()
