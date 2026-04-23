#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
步骤6：产品定价和风险因子设定
非车险产品开发工作流 - 第六步
"""

import json
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

class PricingMethod(Enum):
    """定价方法"""
    PURE_PREMIUM = "纯保费法"
    LOSS_RATIO = "损失率法"
    BURNING_COST = "burning cost法"
    FREQUENCY_SEVERITY = "频率-强度法"

@dataclass
class RiskFactor:
    """风险因子"""
    factor_name: str  # 因子名称
    factor_code: str  # 因子代码
    weight: float  # 权重
    levels: Dict[str, float]  # 等级及系数
    description: str  # 说明
    
    def to_dict(self) -> Dict:
        return {
            "因子名称": self.factor_name,
            "因子代码": self.factor_code,
            "权重": f"{self.weight:.1%}",
            "等级系数": self.levels,
            "说明": self.description
        }

@dataclass
class PricingResult:
    """定价结果"""
    base_rate: float  # 基准费率（‰）
    final_rate: float  # 最终费率（‰）
    premium_per_unit: float  # 每风险单位保费
    
    # 费率构成
    pure_premium_rate: float  # 纯保费率
    expense_loading: float  # 费用附加
    profit_loading: float  # 利润附加
    risk_loading: float  # 风险附加
    
    # 调整因子
    applied_factors: Dict[str, float]  # 应用的因子
    factor_adjustment: float  # 因子调整系数
    
    def to_dict(self) -> Dict:
        return {
            "基准费率": f"{self.base_rate:.3f}‰",
            "最终费率": f"{self.final_rate:.3f}‰",
            "每风险单位保费": f"{self.premium_per_unit:.2f}元",
            "费率构成": {
                "纯保费率": f"{self.pure_premium_rate:.3f}‰",
                "费用附加": f"{self.expense_loading:.2%}",
                "利润附加": f"{self.profit_loading:.2%}",
                "风险附加": f"{self.risk_loading:.2%}"
            },
            "调整因子": self.applied_factors,
            "因子调整系数": f"{self.factor_adjustment:.4f}"
        }

@dataclass
class PricingModel:
    """定价模型"""
    product_name: str  # 产品名称
    pricing_method: PricingMethod  # 定价方法
    
    # 基础数据假设
    expected_loss_ratio: float  # 预期赔付率
    expense_ratio: float  # 费用率
    profit_margin: float  # 利润率
    
    # 风险因子体系
    risk_factors: List[RiskFactor]  # 风险因子列表
    
    # 定价结果
    pricing_result: Optional[PricingResult] = None
    
    def to_dict(self) -> Dict:
        return {
            "产品名称": self.product_name,
            "定价方法": self.pricing_method.value,
            "基础假设": {
                "预期赔付率": f"{self.expected_loss_ratio:.1%}",
                "费用率": f"{self.expense_ratio:.1%}",
                "利润率": f"{self.profit_margin:.1%}"
            },
            "风险因子体系": [f.to_dict() for f in self.risk_factors],
            "定价结果": self.pricing_result.to_dict() if self.pricing_result else None
        }


class PricingEngine:
    """定价引擎"""
    
    def __init__(self):
        self.factor_database = self._load_factor_database()
    
    def _load_factor_database(self) -> Dict:
        """加载风险因子数据库"""
        return {
            "财产险": {
                "建筑结构": RiskFactor(
                    factor_name="建筑结构",
                    factor_code="STRUC",
                    weight=0.25,
                    levels={
                        "钢混结构": 0.80,
                        "砖混结构": 1.00,
                        "钢结构": 0.85,
                        "砖木结构": 1.30,
                        "其他结构": 1.50
                    },
                    description="建筑物的结构类型影响火灾等风险的损失程度"
                ),
                "建筑年代": RiskFactor(
                    factor_name="建筑年代",
                    factor_code="AGE",
                    weight=0.15,
                    levels={
                        "5年以内": 0.85,
                        "5-10年": 0.95,
                        "10-20年": 1.00,
                        "20-30年": 1.15,
                        "30年以上": 1.35
                    },
                    description="建筑使用年限影响设施老化风险"
                ),
                "消防设施": RiskFactor(
                    factor_name="消防设施",
                    factor_code="FIRE_PROT",
                    weight=0.20,
                    levels={
                        "自动喷淋+烟感": 0.75,
                        "消火栓+灭火器": 0.90,
                        "仅灭火器": 1.10,
                        "无消防设施": 1.50
                    },
                    description="消防设施配置影响火灾风险防控能力"
                ),
                "占用性质": RiskFactor(
                    factor_name="占用性质",
                    factor_code="OCCUP",
                    weight=0.25,
                    levels={
                        "办公楼": 0.80,
                        "商场": 1.10,
                        "仓库": 1.30,
                        "工厂": 1.20,
                        "餐饮": 1.40,
                        "娱乐场所": 1.50
                    },
                    description="建筑物的使用性质决定风险类型"
                ),
                "安全管理": RiskFactor(
                    factor_name="安全管理",
                    factor_code="MGMT",
                    weight=0.15,
                    levels={
                        "ISO认证": 0.80,
                        "制度完善": 0.90,
                        "一般管理": 1.00,
                        "管理松散": 1.30
                    },
                    description="安全管理水平影响事故预防能力"
                )
            },
            "责任险": {
                "行业类别": RiskFactor(
                    factor_name="行业类别",
                    factor_code="INDUSTRY",
                    weight=0.35,
                    levels={
                        "低风险服务业": 0.50,
                        "一般商业": 0.80,
                        "制造业": 1.00,
                        "建筑业": 1.50,
                        "高危行业": 2.50
                    },
                    description="不同行业的责任风险差异显著"
                ),
                "经营规模": RiskFactor(
                    factor_name="经营规模",
                    factor_code="SCALE",
                    weight=0.15,
                    levels={
                        "小型": 0.90,
                        "中型": 1.00,
                        "大型": 1.10
                    },
                    description="规模影响风险暴露程度"
                ),
                "区域差异": RiskFactor(
                    factor_name="区域差异",
                    factor_code="REGION",
                    weight=0.20,
                    levels={
                        "一线城市": 1.20,
                        "二线城市": 1.00,
                        "三四线城市": 0.85,
                        "美加地区": 2.00,
                        "欧盟": 1.50,
                        "其他地区": 1.00
                    },
                    description="不同地区司法环境和赔偿标准不同"
                ),
                "历史记录": RiskFactor(
                    factor_name="历史记录",
                    factor_code="HISTORY",
                    weight=0.20,
                    levels={
                        "无赔款": 0.70,
                        "赔款率低": 0.85,
                        "正常": 1.00,
                        "赔款率高": 1.50,
                        "频繁索赔": 2.00
                    },
                    description="历史索赔记录反映风险水平"
                ),
                "限额免赔": RiskFactor(
                    factor_name="限额免赔",
                    factor_code="LIMIT",
                    weight=0.10,
                    levels={
                        "高限额低免赔": 1.20,
                        "标准": 1.00,
                        "低限额高免赔": 0.85
                    },
                    description="赔偿限额和免赔额影响风险成本"
                )
            }
        }
    
    def calculate_base_rate(self, 
                          product_type: str,
                          expected_loss_ratio: float,
                          expense_ratio: float,
                          profit_margin: float) -> float:
        """计算基准费率"""
        # 基础费率参考值（‰）
        base_rates = {
            "财产基本险": 1.0,
            "财产综合险": 2.0,
            "财产一切险": 3.5,
            "公众责任险": 0.8,
            "雇主责任险": 1.0,
            "产品责任险": 0.6
        }
        
        base_rate = base_rates.get(product_type, 2.0)
        
        # 根据假设调整
        # 费率 = 纯保费率 / (1 - 费用率 - 利润率)
        pure_premium_rate = base_rate * expected_loss_ratio
        adjusted_rate = pure_premium_rate / (1 - expense_ratio - profit_margin)
        
        return adjusted_rate
    
    def apply_risk_factors(self, 
                          base_rate: float,
                          factors: List[RiskFactor],
                          selected_levels: Dict[str, str]) -> Tuple[float, Dict[str, float]]:
        """应用风险因子"""
        adjustment = 1.0
        applied = {}
        
        for factor in factors:
            level = selected_levels.get(factor.factor_code, "标准")
            coefficient = factor.levels.get(level, 1.0)
            
            # 加权调整
            weighted_adjustment = (coefficient - 1.0) * factor.weight + 1.0
            adjustment *= weighted_adjustment
            
            applied[factor.factor_name] = coefficient
        
        final_rate = base_rate * adjustment
        return final_rate, applied, adjustment
    
    def create_pricing_model(self,
                            product_name: str,
                            product_type: str,
                            risk_type: str = "财产险") -> PricingModel:
        """创建定价模型"""
        
        # 获取风险因子
        factors = list(self.factor_database.get(risk_type, {}).values())
        
        # 基础假设
        model = PricingModel(
            product_name=product_name,
            pricing_method=PricingMethod.LOSS_RATIO,
            expected_loss_ratio=0.60,
            expense_ratio=0.25,
            profit_margin=0.05,
            risk_factors=factors
        )
        
        return model
    
    def calculate_premium(self,
                         model: PricingModel,
                         sum_insured: float,
                         selected_factors: Dict[str, str]) -> PricingResult:
        """计算保费"""
        
        # 计算基准费率
        base_rate = self.calculate_base_rate(
            model.product_name,
            model.expected_loss_ratio,
            model.expense_ratio,
            model.profit_margin
        )
        
        # 应用风险因子
        final_rate, applied, adjustment = self.apply_risk_factors(
            base_rate,
            model.risk_factors,
            selected_factors
        )
        
        # 计算保费
        premium = sum_insured * final_rate / 1000
        
        # 费率构成
        pure_premium = final_rate * model.expected_loss_ratio
        expense_loading = model.expense_ratio
        profit_loading = model.profit_margin
        risk_loading = 1 - model.expected_loss_ratio - model.expense_ratio - model.profit_margin
        
        result = PricingResult(
            base_rate=base_rate,
            final_rate=final_rate,
            premium_per_unit=premium,
            pure_premium_rate=pure_premium,
            expense_loading=expense_loading,
            profit_loading=profit_loading,
            risk_loading=max(0, risk_loading),
            applied_factors=applied,
            factor_adjustment=adjustment
        )
        
        model.pricing_result = result
        return result
    
    def generate_pricing_report(self, model: PricingModel) -> str:
        """生成定价报告"""
        report = f"""
# {model.product_name}定价分析报告

## 一、定价方法

**采用方法**: {model.pricing_method.value}

## 二、基础假设

| 项目 | 假设值 |
|------|--------|
| 预期赔付率 | {model.expected_loss_ratio:.1%} |
| 费用率 | {model.expense_ratio:.1%} |
| 利润率 | {model.profit_margin:.1%} |

## 三、风险因子体系

"""
        for factor in model.risk_factors:
            report += f"""### {factor.factor_name}（权重{factor.weight:.1%}）

| 等级 | 系数 | 说明 |
|------|------|------|
"""
            for level, coeff in factor.levels.items():
                report += f"| {level} | {coeff:.2f} | |\n"
            report += f"\n{factor.description}\n\n"
        
        if model.pricing_result:
            result = model.pricing_result
            report += f"""
## 四、定价结果

### 4.1 费率水平

| 项目 | 数值 |
|------|------|
| 基准费率 | {result.base_rate:.3f}‰ |
| 最终费率 | {result.final_rate:.3f}‰ |
| 因子调整系数 | {result.factor_adjustment:.4f} |

### 4.2 费率构成

| 项目 | 比例 |
|------|------|
| 纯保费率 | {result.pure_premium_rate:.3f}‰ |
| 费用附加 | {result.expense_loading:.1%} |
| 利润附加 | {result.profit_loading:.1%} |
| 风险附加 | {result.risk_loading:.1%} |

### 4.3 应用的调整因子

| 因子 | 系数 |
|------|------|
"""
            for factor_name, coeff in result.applied_factors.items():
                report += f"| {factor_name} | {coeff:.2f} |\n"
        
        return report
    
    def export_rate_table(self, model: PricingModel) -> pd.DataFrame:
        """导出费率表"""
        data = []
        
        # 生成标准费率表（示例：按行业和保额）
        industries = ["办公楼", "商场", "工厂", "仓库"]
        amounts = [1000000, 5000000, 10000000, 50000000]
        
        for industry in industries:
            for amount in amounts:
                selected = {"OCCUP": industry}
                result = self.calculate_premium(model, amount, selected)
                
                data.append({
                    "行业": industry,
                    "保险金额": amount,
                    "基准费率(‰)": result.base_rate,
                    "调整系数": result.factor_adjustment,
                    "最终费率(‰)": result.final_rate,
                    "保费(元)": result.premium_per_unit
                })
        
        return pd.DataFrame(data)


def main():
    """主函数"""
    engine = PricingEngine()
    
    print("=" * 60)
    print("步骤6：产品定价和风险因子设定")
    print("=" * 60)
    
    # 输入产品信息
    product_name = input("\n请输入产品名称: ")
    risk_type = input("请选择风险类型(财产险/责任险): ")
    
    # 创建定价模型
    model = engine.create_pricing_model(product_name, product_name, risk_type)
    
    # 显示风险因子
    print("\n风险因子体系:")
    for factor in model.risk_factors:
        print(f"\n{factor.factor_name}:")
        for level, coeff in factor.levels.items():
            print(f"  - {level}: {coeff:.2f}")
    
    # 选择因子等级
    print("\n请为各因子选择等级:")
    selected_factors = {}
    for factor in model.risk_factors:
        level = input(f"{factor.factor_name} (默认: 标准): ") or "标准"
        # 如果输入的等级不存在，使用最接近的
        if level not in factor.levels:
            level = list(factor.levels.keys())[0]
        selected_factors[factor.factor_code] = level
    
    # 输入保额
    sum_insured = float(input("\n请输入保险金额(元): ") or "10000000")
    
    # 计算保费
    result = engine.calculate_premium(model, sum_insured, selected_factors)
    
    # 显示结果
    print(f"\n定价结果:")
    print(f"  基准费率: {result.base_rate:.3f}‰")
    print(f"  最终费率: {result.final_rate:.3f}‰")
    print(f"  保费: {result.premium_per_unit:,.2f}元")
    
    # 生成报告
    report = engine.generate_pricing_report(model)
    
    # 保存报告
    filename = f"{product_name}定价报告.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n✓ 定价报告已生成: {filename}")
    
    # 导出费率表
    rate_table = engine.export_rate_table(model)
    rate_table.to_excel(f"{product_name}费率表.xlsx", index=False)
    print(f"✓ 费率表已导出: {product_name}费率表.xlsx")
    
    # 保存模型数据
    with open("step6_pricing_model.json", "w", encoding="utf-8") as f:
        json.dump(model.to_dict(), f, ensure_ascii=False, indent=2)
    
    print("✓ 定价数据已保存到 step6_pricing_model.json")
    
    return model


if __name__ == "__main__":
    main()
