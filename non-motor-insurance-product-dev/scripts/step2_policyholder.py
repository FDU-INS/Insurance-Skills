#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
步骤2：明确投保人、被保险人身份
非车险产品开发工作流 - 第二步
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime

class EntityType(Enum):
    """实体类型"""
    INDIVIDUAL = "个人"
    ENTERPRISE = "企业"
    GOVERNMENT = "政府机构"
    ORGANIZATION = "社会组织"

class InsuranceInterestType(Enum):
    """保险利益类型"""
    OWNERSHIP = "所有权"
    USAGE_RIGHT = "使用权"
    CUSTODY_RIGHT = "保管权"
    MORTGAGE_RIGHT = "抵押权"
    CONTRACT_RIGHT = "合同权益"
    LEGAL_LIABILITY = "法定责任"

@dataclass
class Entity:
    """投保人/被保险人实体"""
    name: str  # 名称
    entity_type: EntityType  # 实体类型
    id_number: str  # 证件号码（统一社会信用代码/身份证号）
    address: str  # 地址
    contact: str  # 联系方式
    
    # 企业特有
    legal_representative: str = ""  # 法定代表人
    business_scope: str = ""  # 经营范围
    registered_capital: float = 0.0  # 注册资本
    establishment_date: str = ""  # 成立日期
    
    # 资格审查
    has_legal_capacity: bool = True  # 是否具有民事行为能力
    has_insurance_interest: bool = True  # 是否具有保险利益
    credit_status: str = "良好"  # 信用状况
    risk_history: List[str] = None  # 风险历史
    
    def __post_init__(self):
        if self.risk_history is None:
            self.risk_history = []
    
    def to_dict(self) -> Dict:
        return {
            "名称": self.name,
            "实体类型": self.entity_type.value,
            "证件号码": self.id_number,
            "地址": self.address,
            "联系方式": self.contact,
            "法定代表人": self.legal_representative,
            "经营范围": self.business_scope,
            "注册资本": self.registered_capital,
            "成立日期": self.establishment_date,
            "资格审查": {
                "民事行为能力": "✓" if self.has_legal_capacity else "✗",
                "保险利益": "✓" if self.has_insurance_interest else "✗",
                "信用状况": self.credit_status
            },
            "风险历史": self.risk_history
        }

@dataclass
class InsuranceInterest:
    """保险利益定义"""
    interest_type: InsuranceInterestType  # 利益类型
    description: str  # 利益描述
    proof_documents: List[str] = None  # 证明文件
    interest_value: float = 0.0  # 利益价值
    
    def __post_init__(self):
        if self.proof_documents is None:
            self.proof_documents = []
    
    def to_dict(self) -> Dict:
        return {
            "利益类型": self.interest_type.value,
            "利益描述": self.description,
            "证明文件": self.proof_documents,
            "利益价值": self.interest_value
        }

@dataclass
class PolicyholderInsured:
    """投保人与被保险人关系"""
    policyholder: Entity  # 投保人
    insured: Entity  # 被保险人
    beneficiary: Optional[Entity] = None  # 受益人
    interest: InsuranceInterest = None  # 保险利益
    is_same_entity: bool = False  # 是否为同一主体
    
    def __post_init__(self):
        self.is_same_entity = (self.policyholder.id_number == self.insured.id_number)
    
    def to_dict(self) -> Dict:
        return {
            "投保人": self.policyholder.to_dict(),
            "被保险人": self.insured.to_dict(),
            "受益人": self.beneficiary.to_dict() if self.beneficiary else "法定受益人",
            "保险利益": self.interest.to_dict() if self.interest else {},
            "是否为同一主体": "是" if self.is_same_entity else "否"
        }


class PolicyholderAnalyzer:
    """投保人/被保险人分析器"""
    
    # 高风险行业提示
    HIGH_RISK_INDUSTRIES = [
        "危险化学品", "烟花爆竹", "煤矿开采", "建筑施工",
        "金属冶炼", "水上运输", "航空运输"
    ]
    
    def __init__(self):
        self.validation_rules = self._load_validation_rules()
    
    def _load_validation_rules(self) -> Dict:
        """加载验证规则"""
        return {
            "企业": {
                "required_documents": [
                    "营业执照", "组织机构代码证", "税务登记证"
                ],
                "credit_check": True,
                "industry_risk_check": True
            },
            "个人": {
                "required_documents": ["身份证"],
                "credit_check": False,
                "industry_risk_check": False
            }
        }
    
    def validate_entity(self, entity: Entity) -> Dict:
        """验证实体资格"""
        validation_result = {
            "is_valid": True,
            "issues": [],
            "warnings": []
        }
        
        # 检查民事行为能力
        if not entity.has_legal_capacity:
            validation_result["is_valid"] = False
            validation_result["issues"].append("不具备民事行为能力")
        
        # 检查保险利益
        if not entity.has_insurance_interest:
            validation_result["is_valid"] = False
            validation_result["issues"].append("不具有保险利益")
        
        # 检查信用状况
        if entity.credit_status in ["不良", "黑名单"]:
            validation_result["is_valid"] = False
            validation_result["issues"].append("信用状况不良")
        
        # 企业特有检查
        if entity.entity_type == EntityType.ENTERPRISE:
            # 检查经营范围
            for industry in self.HIGH_RISK_INDUSTRIES:
                if industry in entity.business_scope:
                    validation_result["warnings"].append(f"属于高风险行业: {industry}")
            
            # 检查注册资本
            if entity.registered_capital < 100000:  # 10万元
                validation_result["warnings"].append("注册资本较低，需关注偿付能力")
        
        # 检查风险历史
        if entity.risk_history:
            validation_result["warnings"].append(f"有风险历史记录: {len(entity.risk_history)}条")
        
        return validation_result
    
    def determine_insurance_interest(self, 
                                    policyholder: Entity,
                                    insured: Entity,
                                    subject_description: str) -> InsuranceInterest:
        """确定保险利益"""
        
        # 同一主体
        if policyholder.id_number == insured.id_number:
            return InsuranceInterest(
                interest_type=InsuranceInterestType.OWNERSHIP,
                description="投保人对自身财产/责任具有所有权/法定责任",
                proof_documents=["身份证明", "财产证明"]
            )
        
        # 判断利益类型
        interest_type = InsuranceInterestType.CONTRACT_RIGHT
        description = "基于合同关系产生的保险利益"
        
        # 根据实体关系判断
        if policyholder.entity_type == EntityType.ENTERPRISE and \
           insured.entity_type == EntityType.INDIVIDUAL:
            # 企业对个人（雇主责任、产品责任等）
            interest_type = InsuranceInterestType.LEGAL_LIABILITY
            description = "雇主对雇员的法定赔偿责任/产品责任"
        
        elif "租赁" in subject_description or "承租" in subject_description:
            interest_type = InsuranceInterestType.USAGE_RIGHT
            description = "基于租赁关系产生的使用权"
        
        elif "抵押" in subject_description or "贷款" in subject_description:
            interest_type = InsuranceInterestType.MORTGAGE_RIGHT
            description = "基于抵押关系产生的抵押权"
        
        elif "保管" in subject_description or "仓储" in subject_description:
            interest_type = InsuranceInterestType.CUSTODY_RIGHT
            description = "基于保管关系产生的保管权"
        
        return InsuranceInterest(
            interest_type=interest_type,
            description=description,
            proof_documents=["合同", "权属证明"]
        )
    
    def generate_relationship_report(self, pi: PolicyholderInsured) -> str:
        """生成关系分析报告"""
        # 验证双方资格
        ph_validation = self.validate_entity(pi.policyholder)
        ins_validation = self.validate_entity(pi.insured)
        
        report = f"""
# 投保人/被保险人身份分析报告

## 一、投保人信息
- **名称**: {pi.policyholder.name}
- **类型**: {pi.policyholder.entity_type.value}
- **证件号码**: {pi.policyholder.id_number}
- **地址**: {pi.policyholder.address}
- **联系方式**: {pi.policyholder.contact}
"""
        
        if pi.policyholder.entity_type == EntityType.ENTERPRISE:
            report += f"""\
- **法定代表人**: {pi.policyholder.legal_representative}
- **经营范围**: {pi.policyholder.business_scope}
- **注册资本**: {pi.policyholder.registered_capital:,.2f}元
- **成立日期**: {pi.policyholder.establishment_date}
"""
        
        report += f"""
## 二、被保险人信息
- **名称**: {pi.insured.name}
- **类型**: {pi.insured.entity_type.value}
- **证件号码**: {pi.insured.id_number}
- **地址**: {pi.insured.address}
- **联系方式**: {pi.insured.contact}
"""
        
        if pi.insured.entity_type == EntityType.ENTERPRISE:
            report += f"""\
- **法定代表人**: {pi.insured.legal_representative}
- **经营范围**: {pi.insured.business_scope}
"""
        
        report += f"""
## 三、保险利益认定
- **利益类型**: {pi.interest.interest_type.value if pi.interest else "待确定"}
- **利益描述**: {pi.interest.description if pi.interest else "待确定"}
- **是否为同一主体**: {"是" if pi.is_same_entity else "否"}

## 四、资格审查

### 投保人资格
- **民事行为能力**: {"✓ 合格" if pi.policyholder.has_legal_capacity else "✗ 不合格"}
- **保险利益**: {"✓ 具备" if pi.policyholder.has_insurance_interest else "✗ 不具备"}
- **信用状况**: {pi.policyholder.credit_status}
"""
        
        if ph_validation["issues"]:
            report += "\n**问题**: " + "; ".join(ph_validation["issues"])
        if ph_validation["warnings"]:
            report += "\n**提示**: " + "; ".join(ph_validation["warnings"])
        
        report += f"""

### 被保险人资格
- **民事行为能力**: {"✓ 合格" if pi.insured.has_legal_capacity else "✗ 不合格"}
- **保险利益**: {"✓ 具备" if pi.insured.has_insurance_interest else "✗ 不具备"}
- **信用状况**: {pi.insured.credit_status}
"""
        
        if ins_validation["issues"]:
            report += "\n**问题**: " + "; ".join(ins_validation["issues"])
        if ins_validation["warnings"]:
            report += "\n**提示**: " + "; ".join(ins_validation["warnings"])
        
        # 结论
        if ph_validation["is_valid"] and ins_validation["is_valid"]:
            report += "\n\n## 五、结论\n✅ **投保人和被保险人均符合资格要求**\n"
        else:
            report += "\n\n## 五、结论\n❌ **存在资格问题，需进一步核实**\n"
        
        return report


def main():
    """主函数 - 交互式身份确认"""
    analyzer = PolicyholderAnalyzer()
    
    print("=" * 60)
    print("步骤2：明确投保人、被保险人身份")
    print("=" * 60)
    
    # 输入投保人信息
    print("\n【投保人信息】")
    ph_name = input("名称: ")
    ph_type = input("类型(企业/个人/政府机构/社会组织): ")
    ph_id = input("证件号码: ")
    ph_address = input("地址: ")
    ph_contact = input("联系方式: ")
    
    entity_type_map = {
        "企业": EntityType.ENTERPRISE,
        "个人": EntityType.INDIVIDUAL,
        "政府机构": EntityType.GOVERNMENT,
        "社会组织": EntityType.ORGANIZATION
    }
    
    policyholder = Entity(
        name=ph_name,
        entity_type=entity_type_map.get(ph_type, EntityType.ENTERPRISE),
        id_number=ph_id,
        address=ph_address,
        contact=ph_contact
    )
    
    # 输入被保险人信息
    print("\n【被保险人信息】")
    ins_same = input("被保险人与投保人是否为同一主体?(是/否): ")
    
    if ins_same == "是":
        insured = policyholder
    else:
        ins_name = input("名称: ")
        ins_type = input("类型(企业/个人/政府机构/社会组织): ")
        ins_id = input("证件号码: ")
        ins_address = input("地址: ")
        ins_contact = input("联系方式: ")
        
        insured = Entity(
            name=ins_name,
            entity_type=entity_type_map.get(ins_type, EntityType.ENTERPRISE),
            id_number=ins_id,
            address=ins_address,
            contact=ins_contact
        )
    
    # 确定保险利益
    subject_desc = input("\n保险标的描述: ")
    interest = analyzer.determine_insurance_interest(policyholder, insured, subject_desc)
    
    # 创建关系对象
    pi = PolicyholderInsured(
        policyholder=policyholder,
        insured=insured,
        interest=interest
    )
    
    # 生成报告
    report = analyzer.generate_relationship_report(pi)
    print(report)
    
    # 保存结果
    output = {
        "step": 2,
        "policyholder_insured": pi.to_dict()
    }
    
    with open("step2_policyholder_analysis.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print("\n✓ 分析结果已保存到 step2_policyholder_analysis.json")
    
    return pi


if __name__ == "__main__":
    main()
