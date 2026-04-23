#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
步骤1：确定保险标的概念
非车险产品开发工作流 - 第一步
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class SubjectType(Enum):
    """保险标的类型"""
    TANGIBLE_PROPERTY = "有形财产"
    INTANGIBLE_PROPERTY = "无形财产"
    LEGAL_LIABILITY = "法律责任"
    PERSONAL_RELATED = "人身相关"
    CONTRACTUAL_INTEREST = "合同权益"

class RiskLevel(Enum):
    """风险等级"""
    LOW = "低风险"
    MEDIUM = "中风险"
    HIGH = "高风险"
    PROHIBITED = "不可保"

@dataclass
class InsuredSubject:
    """保险标的定义"""
    name: str  # 标的名称
    subject_type: SubjectType  # 标的类型
    description: str  # 标的描述
    valuation_method: str  # 估价方法
    risk_level: RiskLevel  # 风险等级
    
    # 可保性检查
    is_legal: bool = True  # 是否合法
    is_definite: bool = True  # 是否确定
    is_valuable: bool = True  # 是否可估价
    is_transferable: bool = True  # 风险是否可转移
    is_accidental: bool = True  # 损失是否偶然
    
    # 特殊属性
    special_attributes: Dict = None  # 特殊属性
    exclusions: List[str] = None  # 除外事项
    
    def __post_init__(self):
        if self.special_attributes is None:
            self.special_attributes = {}
        if self.exclusions is None:
            self.exclusions = []
    
    def to_dict(self) -> Dict:
        return {
            "标的名称": self.name,
            "标的类型": self.subject_type.value,
            "标的描述": self.description,
            "估价方法": self.valuation_method,
            "风险等级": self.risk_level.value,
            "可保性检查": {
                "合法性": "✓" if self.is_legal else "✗",
                "确定性": "✓" if self.is_definite else "✗",
                "可估价性": "✓" if self.is_valuable else "✗",
                "可转移性": "✓" if self.is_transferable else "✗",
                "偶然性": "✓" if self.is_accidental else "✗"
            },
            "特殊属性": self.special_attributes,
            "除外事项": self.exclusions
        }
    
    def is_insurable(self) -> bool:
        """检查是否可保"""
        return all([
            self.is_legal,
            self.is_definite,
            self.is_valuable,
            self.is_transferable,
            self.is_accidental
        ]) and self.risk_level != RiskLevel.PROHIBITED


class SubjectAnalyzer:
    """保险标的分析器"""
    
    # 不可保标的清单
    PROHIBITED_SUBJECTS = [
        "土地", "矿藏", "水资源", "森林（特殊约定除外）",
        "货币", "票证", "有价证券", "文件账册",
        "违章建筑", "非法财产", "走私物品",
        "核武器", "放射性物质（特殊险种除外）"
    ]
    
    # 高风险标的提示
    HIGH_RISK_SUBJECTS = [
        "易燃易爆物品", "危险化学品", "烟花爆竹",
        "大型活动", "高层建筑", "地下空间"
    ]
    
    def __init__(self):
        self.subject_database = self._load_subject_database()
    
    def _load_subject_database(self) -> Dict:
        """加载标的类型数据库"""
        return {
            "企业财产": {
                "type": SubjectType.TANGIBLE_PROPERTY,
                "valuation": "重置价值/账面价值",
                "risk_factors": ["建筑结构", "消防设施", "安全管理"]
            },
            "机器设备": {
                "type": SubjectType.TANGIBLE_PROPERTY,
                "valuation": "重置价值/折旧价值",
                "risk_factors": ["设备类型", "使用年限", "维护状况"]
            },
            "存货商品": {
                "type": SubjectType.TANGIBLE_PROPERTY,
                "valuation": "账面余额/成本价",
                "risk_factors": ["存储条件", "商品性质", "周转速度"]
            },
            "在建工程": {
                "type": SubjectType.TANGIBLE_PROPERTY,
                "valuation": "工程预算/实际支出",
                "risk_factors": ["工程类型", "施工环境", "承包商资质"]
            },
            "公众责任": {
                "type": SubjectType.LEGAL_LIABILITY,
                "valuation": "赔偿限额",
                "risk_factors": ["场所性质", "人流密度", "安全管理"]
            },
            "产品责任": {
                "type": SubjectType.LEGAL_LIABILITY,
                "valuation": "赔偿限额",
                "risk_factors": ["产品类型", "销售区域", "质量控制"]
            },
            "雇主责任": {
                "type": SubjectType.LEGAL_LIABILITY,
                "valuation": "赔偿限额",
                "risk_factors": ["行业风险", "员工数量", "安全记录"]
            },
            "营业中断": {
                "type": SubjectType.INTANGIBLE_PROPERTY,
                "valuation": "预期利润/固定费用",
                "risk_factors": ["行业特点", "经营历史", "恢复能力"]
            },
            "货物运输": {
                "type": SubjectType.TANGIBLE_PROPERTY,
                "valuation": "货值/发票金额",
                "risk_factors": ["运输方式", "货物性质", "运输路线"]
            }
        }
    
    def analyze_subject(self, subject_name: str, 
                       description: str = "",
                       custom_attributes: Dict = None) -> InsuredSubject:
        """分析保险标的"""
        
        # 检查是否在不可保清单
        if any(prohibited in subject_name for prohibited in self.PROHIBITED_SUBJECTS):
            return InsuredSubject(
                name=subject_name,
                subject_type=SubjectType.TANGIBLE_PROPERTY,
                description=description or "该标的属于不可保范围",
                valuation_method="不可估价",
                risk_level=RiskLevel.PROHIBITED,
                is_legal=False
            )
        
        # 从数据库获取基础信息
        base_info = None
        for key, value in self.subject_database.items():
            if key in subject_name or subject_name in key:
                base_info = value
                break
        
        if base_info:
            subject_type = base_info["type"]
            valuation = base_info["valuation"]
        else:
            subject_type = SubjectType.TANGIBLE_PROPERTY
            valuation = "需根据具体情况确定"
        
        # 判断风险等级
        risk_level = RiskLevel.MEDIUM
        if any(high_risk in subject_name for high_risk in self.HIGH_RISK_SUBJECTS):
            risk_level = RiskLevel.HIGH
        
        return InsuredSubject(
            name=subject_name,
            subject_type=subject_type,
            description=description,
            valuation_method=valuation,
            risk_level=risk_level,
            special_attributes=custom_attributes or {}
        )
    
    def generate_subject_report(self, subject: InsuredSubject) -> str:
        """生成标的分析报告"""
        report = f"""
# 保险标的分析报告

## 一、标的基本信息
- **标的名称**: {subject.name}
- **标的类型**: {subject.subject_type.value}
- **风险等级**: {subject.risk_level.value}

## 二、标的描述
{subject.description}

## 三、估价方法
{subject.valuation_method}

## 四、可保性检查
"""
        for check, result in subject.to_dict()["可保性检查"].items():
            report += f"- {check}: {result}\n"
        
        if subject.is_insurable():
            report += "\n## 五、结论\n✅ **该标的可以承保**\n"
        else:
            report += "\n## 五、结论\n❌ **该标的不可承保**\n"
            report += "\n### 不可保原因:\n"
            if not subject.is_legal:
                report += "- 标的合法性存疑\n"
            if not subject.is_definite:
                report += "- 标的不确定，无法界定\n"
            if not subject.is_valuable:
                report += "- 标的无法用货币衡量\n"
            if not subject.is_transferable:
                report += "- 风险无法转移\n"
            if not subject.is_accidental:
                report += "- 损失不具有偶然性\n"
        
        if subject.special_attributes:
            report += f"\n## 六、特殊属性\n"
            for key, value in subject.special_attributes.items():
                report += f"- {key}: {value}\n"
        
        if subject.exclusions:
            report += f"\n## 七、除外事项\n"
            for exclusion in subject.exclusions:
                report += f"- {exclusion}\n"
        
        return report


def main():
    """主函数 - 交互式标的分析"""
    analyzer = SubjectAnalyzer()
    
    print("=" * 60)
    print("步骤1：确定保险标的概念")
    print("=" * 60)
    
    subject_name = input("\n请输入保险标的名称: ")
    description = input("请输入标的描述（可选）: ")
    
    # 分析标的
    subject = analyzer.analyze_subject(subject_name, description)
    
    # 生成报告
    report = analyzer.generate_subject_report(subject)
    print(report)
    
    # 保存结果
    output = {
        "step": 1,
        "subject": subject.to_dict(),
        "is_insurable": subject.is_insurable()
    }
    
    with open("step1_subject_analysis.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print("\n✓ 分析结果已保存到 step1_subject_analysis.json")
    
    return subject


if __name__ == "__main__":
    main()
