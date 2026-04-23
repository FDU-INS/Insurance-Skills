#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
步骤3：初步明确保险责任范围
非车险产品开发工作流 - 第三步
"""

import json
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict, field
from enum import Enum

class PerilType(Enum):
    """风险事故类型"""
    FIRE = "火灾"
    EXPLOSION = "爆炸"
    LIGHTNING = "雷击"
    STORM = "暴风、暴雨、洪水"
    EARTHQUAKE = "地震"
    ACCIDENT = "意外事故"
    NEGLIGENCE = "过失行为"
    LEGAL_LIABILITY = "法律责任"
    CONSEQUENTIAL = "间接损失"

class CoverageScope(Enum):
    """保障范围"""
    BASIC = "基本保障"
    BROAD = "扩展保障"
    ALL_RISK = "一切险"
    SPECIFIED = "特定风险"

@dataclass
class CoverageItem:
    """保险责任项目"""
    name: str  # 责任名称
    description: str  # 责任描述
    perils: List[PerilType]  # 承保风险
    exclusions: List[str]  # 责任免除
    sub_limits: Optional[Dict] = None  # 分项限额
    
    def to_dict(self) -> Dict:
        return {
            "责任名称": self.name,
            "责任描述": self.description,
            "承保风险": [p.value for p in self.perils],
            "责任免除": self.exclusions,
            "分项限额": self.sub_limits or "无"
        }

@dataclass
class CoverageStructure:
    """保险责任结构"""
    main_coverage: List[CoverageItem]  # 主险责任
    additional_coverage: List[CoverageItem]  # 附加险责任
    exclusions: List[str]  # 通用除外责任
    special_clauses: List[str]  # 特别约定
    
    def to_dict(self) -> Dict:
        return {
            "主险责任": [item.to_dict() for item in self.main_coverage],
            "附加险责任": [item.to_dict() for item in self.additional_coverage],
            "通用除外责任": self.exclusions,
            "特别约定": self.special_clauses
        }


class CoverageDesigner:
    """保险责任设计器"""
    
    # 标准责任模板库
    COVERAGE_TEMPLATES = {
        "财产基本险": {
            "scope": CoverageScope.BASIC,
            "perils": [PerilType.FIRE, PerilType.EXPLOSION, PerilType.LIGHTNING],
            "exclusions": [
                "暴雨、洪水、台风等自然灾害",
                "盗窃、抢劫",
                "战争、军事行动",
                "核辐射、核污染",
                "被保险人故意行为",
                "保险标的的内在缺陷"
            ]
        },
        "财产综合险": {
            "scope": CoverageScope.BROAD,
            "perils": [
                PerilType.FIRE, PerilType.EXPLOSION, PerilType.LIGHTNING,
                PerilType.STORM, PerilType.EARTHQUAKE
            ],
            "exclusions": [
                "盗窃、抢劫",
                "战争、军事行动",
                "核辐射、核污染",
                "被保险人故意行为",
                "保险标的的内在缺陷"
            ]
        },
        "财产一切险": {
            "scope": CoverageScope.ALL_RISK,
            "perils": [],  # 一切险采用除外列明
            "exclusions": [
                "盗窃、抢劫（可附加）",
                "战争、军事行动",
                "核辐射、核污染",
                "被保险人故意行为",
                "保险标的的内在缺陷",
                "自然磨损、锈蚀",
                "鼠咬、虫蛀"
            ]
        },
        "公众责任险": {
            "scope": CoverageScope.SPECIFIED,
            "perils": [PerilType.NEGLIGENCE, PerilType.ACCIDENT],
            "exclusions": [
                "故意行为",
                "合同责任（保证险除外）",
                "核风险",
                "污染责任（可附加）",
                "雇主对雇员责任（雇主险承保）",
                "产品责任（产品险承保）"
            ]
        },
        "雇主责任险": {
            "scope": CoverageScope.SPECIFIED,
            "perils": [PerilType.LEGAL_LIABILITY],
            "exclusions": [
                "故意行为",
                "职业病除外责任",
                "境外责任（可附加）",
                "承包商人员（需特别约定）"
            ]
        },
        "产品责任险": {
            "scope": CoverageScope.SPECIFIED,
            "perils": [PerilType.LEGAL_LIABILITY],
            "exclusions": [
                "故意行为",
                "产品召回费用（可附加）",
                "合同责任",
                "惩罚性赔偿（美加地区除外）",
                "产品本身损失"
            ]
        }
    }
    
    # 通用除外责任
    UNIVERSAL_EXCLUSIONS = [
        "投保人、被保险人及其代表的故意或重大过失行为",
        "战争、敌对行为、军事行动、武装冲突、恐怖活动",
        "核辐射、核爆炸、核污染及其他放射性污染",
        "地震、海啸及其次生灾害（另有约定除外）",
        "行政行为或司法行为",
        "保险标的的内在或潜在缺陷、自然磨损、自然损耗",
        "大气、土地、水污染及其他各种污染（责任险除外）",
        "罚款、罚金及惩罚性赔偿"
    ]
    
    def __init__(self):
        self.selected_template = None
        self.custom_coverage = None
    
    def select_template(self, product_type: str) -> Dict:
        """选择责任模板"""
        template = self.COVERAGE_TEMPLATES.get(product_type)
        if not template:
            available = ", ".join(self.COVERAGE_TEMPLATES.keys())
            raise ValueError(f"未知产品类型: {product_type}。可用类型: {available}")
        
        self.selected_template = product_type
        return template
    
    def design_coverage(self, 
                       product_type: str,
                       custom_perils: List[str] = None,
                       custom_exclusions: List[str] = None,
                       add_extensions: List[str] = None) -> CoverageStructure:
        """设计保险责任"""
        
        template = self.select_template(product_type)
        
        # 构建主险责任
        main_coverage = []
        
        if template["scope"] == CoverageScope.ALL_RISK:
            # 一切险责任描述
            main_coverage.append(CoverageItem(
                name="财产一切险责任",
                description="在保险期间内，由于自然灾害或意外事故造成保险标的的直接物质损坏或灭失，保险人按照本保险合同的约定负责赔偿",
                perils=[],  # 一切险不列明风险
                exclusions=template["exclusions"]
            ))
        else:
            # 列明风险责任
            perils_desc = "、".join([p.value for p in template["perils"]])
            main_coverage.append(CoverageItem(
                name=f"{product_type}责任",
                description=f"在保险期间内，由于{perils_desc}造成保险标的的损失，保险人负责赔偿",
                perils=template["perils"],
                exclusions=template["exclusions"]
            ))
        
        # 构建附加险责任
        additional_coverage = []
        if add_extensions:
            for ext in add_extensions:
                ext_coverage = self._get_extension_coverage(ext)
                if ext_coverage:
                    additional_coverage.append(ext_coverage)
        
        # 合并除外责任
        exclusions = self.UNIVERSAL_EXCLUSIONS.copy()
        if custom_exclusions:
            exclusions.extend(custom_exclusions)
        
        # 特别约定
        special_clauses = []
        if custom_perils:
            special_clauses.append(f"扩展承保: {', '.join(custom_perils)}")
        
        return CoverageStructure(
            main_coverage=main_coverage,
            additional_coverage=additional_coverage,
            exclusions=list(set(exclusions)),  # 去重
            special_clauses=special_clauses
        )
    
    def _get_extension_coverage(self, extension_name: str) -> Optional[CoverageItem]:
        """获取扩展责任定义"""
        extensions = {
            "盗窃扩展": CoverageItem(
                name="盗窃、抢劫扩展条款",
                description="扩展承保盗窃、抢劫造成的损失",
                perils=[],
                exclusions=["内部人员盗窃", "盘点短缺"],
                sub_limits={"每次事故": "主险保额的20%"}
            ),
            "玻璃破碎": CoverageItem(
                name="玻璃破碎扩展条款",
                description="扩展承保玻璃单独破碎损失",
                perils=[],
                exclusions=["玻璃贴膜", "框架损坏"]
            ),
            "清理费用": CoverageItem(
                name="残骸清理费用条款",
                description="承保灾后清理残骸的必要费用",
                perils=[],
                exclusions=[],
                sub_limits={"每次事故": "损失金额的10%", "最高": "100万元"}
            ),
            "专业费用": CoverageItem(
                name="专业费用条款",
                description="承保建筑师、工程师等专业技术人员的费用",
                perils=[],
                exclusions=[],
                sub_limits={"每次事故": "保额的10%"}
            ),
            "灭火费用": CoverageItem(
                name="灭火费用条款",
                description="承保为扑灭火灾产生的必要费用",
                perils=[PerilType.FIRE],
                exclusions=[],
                sub_limits={"每次事故": "50万元"}
            )
        }
        return extensions.get(extension_name)
    
    def generate_coverage_report(self, coverage: CoverageStructure) -> str:
        """生成责任范围报告"""
        report = f"""
# 保险责任范围分析报告

## 一、主险责任

"""
        for i, item in enumerate(coverage.main_coverage, 1):
            report += f"""### {i}. {item.name}
**责任描述**: {item.description}

**承保风险**:
"""
            if item.perils:
                for peril in item.perils:
                    report += f"- {peril.value}\n"
            else:
                report += "- 一切险采用除外列明方式\n"
            
            report += f"""
**责任免除**:
"""
            for exclusion in item.exclusions:
                report += f"- {exclusion}\n"
            
            if item.sub_limits:
                report += f"""
**分项限额**: {item.sub_limits}
"""
            report += "\n"
        
        if coverage.additional_coverage:
            report += """## 二、附加险责任

"""
            for i, item in enumerate(coverage.additional_coverage, 1):
                report += f"""### {i}. {item.name}
**责任描述**: {item.description}

**责任免除**:
"""
                for exclusion in item.exclusions:
                    report += f"- {exclusion}\n"
                
                if item.sub_limits:
                    report += f"""
**分项限额**: {item.sub_limits}
"""
                report += "\n"
        
        report += """## 三、通用除外责任

"""
        for i, exclusion in enumerate(coverage.exclusions, 1):
            report += f"{i}. {exclusion}\n"
        
        if coverage.special_clauses:
            report += """
## 四、特别约定

"""
            for clause in coverage.special_clauses:
                report += f"- {clause}\n"
        
        return report


def main():
    """主函数 - 交互式责任设计"""
    designer = CoverageDesigner()
    
    print("=" * 60)
    print("步骤3：初步明确保险责任范围")
    print("=" * 60)
    
    # 显示可用模板
    print("\n可用产品类型:")
    for i, ptype in enumerate(designer.COVERAGE_TEMPLATES.keys(), 1):
        print(f"  {i}. {ptype}")
    
    # 选择产品类型
    product_type = input("\n请选择产品类型: ")
    
    # 选择扩展条款
    print("\n可用扩展条款:")
    extensions = ["盗窃扩展", "玻璃破碎", "清理费用", "专业费用", "灭火费用"]
    for i, ext in enumerate(extensions, 1):
        print(f"  {i}. {ext}")
    
    ext_input = input("\n请选择扩展条款（多选用逗号分隔，无则回车）: ")
    selected_extensions = [e.strip() for e in ext_input.split(",") if e.strip()] if ext_input else []
    
    # 设计责任
    coverage = designer.design_coverage(
        product_type=product_type,
        add_extensions=selected_extensions
    )
    
    # 生成报告
    report = designer.generate_coverage_report(coverage)
    print(report)
    
    # 保存结果
    output = {
        "step": 3,
        "coverage": coverage.to_dict()
    }
    
    with open("step3_coverage_design.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print("\n✓ 责任设计已保存到 step3_coverage_design.json")
    
    return coverage


if __name__ == "__main__":
    main()
