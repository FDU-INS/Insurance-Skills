#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
步骤4：撰写产品条款开发可行性研究报告
非车险产品开发工作流 - 第四步
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class MarketAnalysis:
    """市场分析"""
    market_background: str  # 市场背景
    target_customers: List[str]  # 目标客户群
    market_size: str  # 市场规模估算
    competitive_landscape: str  # 竞争格局
    market_opportunity: str  # 市场机会
    
    def to_dict(self) -> Dict:
        return {
            "市场背景": self.market_background,
            "目标客户群": self.target_customers,
            "市场规模": self.market_size,
            "竞争格局": self.competitive_landscape,
            "市场机会": self.market_opportunity
        }

@dataclass
class RiskAnalysis:
    """风险分析"""
    risk_identification: List[Dict]  # 风险识别
    risk_assessment: str  # 风险评估
    loss_history: str  # 历史损失数据
    risk_characteristics: str  # 风险特征
    
    def to_dict(self) -> Dict:
        return {
            "风险识别": self.risk_identification,
            "风险评估": self.risk_assessment,
            "历史损失": self.loss_history,
            "风险特征": self.risk_characteristics
        }

@dataclass
class RiskControl:
    """风险管控"""
    underwriting_control: List[str]  # 核保管控
    claims_control: List[str]  # 理赔管控
    reinsurance_arrangement: str  # 再保险安排
    risk_monitoring: List[str]  # 风险监控
    
    def to_dict(self) -> Dict:
        return {
            "核保管控": self.underwriting_control,
            "理赔管控": self.claims_control,
            "再保险安排": self.reinsurance_arrangement,
            "风险监控": self.risk_monitoring
        }

@dataclass
class FinancialProjection:
    """财务预测"""
    premium_projection: str  # 保费预测
    loss_ratio_estimate: str  # 赔付率预估
    expense_ratio: str  # 费用率
    combined_ratio: str  # 综合成本率
    profitability: str  # 盈利性分析
    
    def to_dict(self) -> Dict:
        return {
            "保费预测": self.premium_projection,
            "赔付率预估": self.loss_ratio_estimate,
            "费用率": self.expense_ratio,
            "综合成本率": self.combined_ratio,
            "盈利性分析": self.profitability
        }

@dataclass
class FeasibilityReport:
    """可行性研究报告"""
    product_name: str  # 产品名称
    report_date: str  # 报告日期
    
    # 开发背景
    development_background: str  # 开发背景
    policy_drivers: List[str]  # 政策驱动
    market_demand: str  # 市场需求
    
    # 保险责任
    coverage_summary: str  # 保险责任概述
    target_risks: List[str]  # 目标风险
    coverage_highlights: List[str]  # 责任亮点
    
    # 分析内容
    market_analysis: MarketAnalysis  # 市场分析
    risk_analysis: RiskAnalysis  # 风险分析
    risk_control: RiskControl  # 风险管控
    financial_projection: FinancialProjection  # 财务预测
    
    # 结论建议
    feasibility_conclusion: str  # 可行性结论
    development_recommendations: List[str]  # 开发建议
    next_steps: List[str]  # 下一步工作
    
    def to_dict(self) -> Dict:
        return {
            "产品名称": self.product_name,
            "报告日期": self.report_date,
            "开发背景": {
                "背景描述": self.development_background,
                "政策驱动": self.policy_drivers,
                "市场需求": self.market_demand
            },
            "保险责任": {
                "责任概述": self.coverage_summary,
                "目标风险": self.target_risks,
                "责任亮点": self.coverage_highlights
            },
            "市场分析": self.market_analysis.to_dict(),
            "风险分析": self.risk_analysis.to_dict(),
            "风险管控": self.risk_control.to_dict(),
            "财务预测": self.financial_projection.to_dict(),
            "结论建议": {
                "可行性结论": self.feasibility_conclusion,
                "开发建议": self.development_recommendations,
                "下一步工作": self.next_steps
            }
        }


class FeasibilityReportGenerator:
    """可行性研究报告生成器"""
    
    def __init__(self):
        self.report_template = self._load_template()
    
    def _load_template(self) -> Dict:
        """加载报告模板"""
        return {
            "sections": [
                "一、开发背景",
                "二、保险责任",
                "三、市场分析",
                "四、风险分析",
                "五、风险管控手段",
                "六、财务预测",
                "七、可行性结论与建议"
            ]
        }
    
    def generate_report(self, 
                       product_name: str,
                       product_type: str,
                       subject_info: Dict,
                       coverage_info: Dict) -> FeasibilityReport:
        """生成可行性研究报告"""
        
        # 构建开发背景
        background = self._generate_background(product_type, subject_info)
        
        # 构建保险责任概述
        coverage_summary = self._generate_coverage_summary(coverage_info)
        
        # 构建市场分析
        market_analysis = self._generate_market_analysis(product_type, subject_info)
        
        # 构建风险分析
        risk_analysis = self._generate_risk_analysis(product_type, coverage_info)
        
        # 构建风险管控
        risk_control = self._generate_risk_control(product_type)
        
        # 构建财务预测
        financial = self._generate_financial_projection(product_type)
        
        # 构建结论
        conclusion = self._generate_conclusion(product_type, risk_analysis)
        
        return FeasibilityReport(
            product_name=product_name,
            report_date=datetime.now().strftime("%Y年%m月%d日"),
            development_background=background["background"],
            policy_drivers=background["policies"],
            market_demand=background["demand"],
            coverage_summary=coverage_summary["summary"],
            target_risks=coverage_summary["risks"],
            coverage_highlights=coverage_summary["highlights"],
            market_analysis=market_analysis,
            risk_analysis=risk_analysis,
            risk_control=risk_control,
            financial_projection=financial,
            feasibility_conclusion=conclusion["conclusion"],
            development_recommendations=conclusion["recommendations"],
            next_steps=conclusion["next_steps"]
        )
    
    def _generate_background(self, product_type: str, subject_info: Dict) -> Dict:
        """生成开发背景"""
        backgrounds = {
            "财产基本险": {
                "background": "随着企业风险管理意识提升，基础财产保障需求稳定增长。中小企业对成本敏感，需要高性价比的基础保障方案。",
                "policies": ["《保险法》对财产保险的基础规范", "银保监会关于财产险产品监管要求"],
                "demand": "中小企业基础财产保障需求旺盛，市场容量大"
            },
            "财产综合险": {
                "background": "自然灾害频发，企业对扩展自然灾害保障的需求日益增强。传统基本险已不能满足企业全面保障需求。",
                "policies": ["国家防灾减灾政策导向", "巨灾保险制度建设"],
                "demand": "中大型企业需要更全面的财产保障"
            },
            "公众责任险": {
                "background": "随着公众维权意识增强和赔偿标准提高，企业面临的第三者责任风险日益增大。商场、酒店等公共场所事故频发。",
                "policies": ["《民法典》侵权责任编实施", "安全生产法规要求"],
                "demand": "公共场所经营者的强制或半强制需求"
            },
            "雇主责任险": {
                "background": "工伤保险保障有限，企业需要补充雇主赔偿责任保障。劳动争议增多，企业用工风险加大。",
                "policies": ["《工伤保险条例》", "《劳动合同法》", "安全生产责任保险制度"],
                "demand": "各类企业的用工风险转移需求"
            },
            "产品责任险": {
                "background": "产品质量问题引发的赔偿责任案件增多，出口企业面临欧美严格的产品责任法律环境。",
                "policies": ["《产品质量法》", "《消费者权益保护法》", "出口信用保险政策"],
                "demand": "制造业企业、出口企业的刚性需求"
            }
        }
        return backgrounds.get(product_type, {
            "background": "市场对新型非车险产品的需求日益增长",
            "policies": ["保险监管政策鼓励产品创新"],
            "demand": "目标客户群体存在保障缺口"
        })
    
    def _generate_coverage_summary(self, coverage_info: Dict) -> Dict:
        """生成保险责任概述"""
        main_coverage = coverage_info.get("主险责任", [])
        
        risks = []
        highlights = []
        
        for coverage in main_coverage:
            perils = coverage.get("承保风险", [])
            risks.extend(perils)
            highlights.append(coverage.get("责任描述", ""))
        
        return {
            "summary": f"本产品提供{len(main_coverage)}项主险责任，覆盖{'、'.join(list(set(risks))[:3])}等主要风险",
            "risks": list(set(risks)),
            "highlights": highlights
        }
    
    def _generate_market_analysis(self, product_type: str, subject_info: Dict) -> MarketAnalysis:
        """生成市场分析"""
        return MarketAnalysis(
            market_background="非车险市场持续增长，财产险、责任险需求稳步上升",
            target_customers=[
                "中小企业主",
                "大型企业风险管理部门",
                "工商企业",
                "服务业企业"
            ],
            market_size="预计目标市场规模约XX亿元，年增长率8-10%",
            competitive_landscape="市场已有主要竞争者，但产品同质化严重，存在差异化空间",
            market_opportunity="通过精准定价和优质服务，可获取细分市场份额"
        )
    
    def _generate_risk_analysis(self, product_type: str, coverage_info: Dict) -> RiskAnalysis:
        """生成风险分析"""
        
        # 风险识别
        risks = []
        main_coverage = coverage_info.get("主险责任", [])
        for coverage in main_coverage:
            perils = coverage.get("承保风险", [])
            for peril in perils:
                risks.append({
                    "风险类型": peril,
                    "风险等级": "中",
                    "发生频率": "中",
                    "损失程度": "中高"
                })
        
        return RiskAnalysis(
            risk_identification=risks,
            risk_assessment="整体风险可控，主要风险为自然灾害和意外事故，可通过再保险分散",
            loss_history="参考行业历史赔付数据，预估赔付率在50-65%区间",
            risk_characteristics="风险分布较为分散，大灾风险需通过再保险安排"
        )
    
    def _generate_risk_control(self, product_type: str) -> RiskControl:
        """生成风险管控"""
        return RiskControl(
            underwriting_control=[
                "建立标的分级核保制度",
                "高风险业务实行现场查勘",
                "设置合理的免赔额和赔偿限额",
                "实行行业风险分类管理"
            ],
            claims_control=[
                "建立专业理赔团队",
                "实行重大案件专家会诊",
                "加强第三方损失评估",
                "建立反欺诈机制"
            ],
            reinsurance_arrangement="建议安排成数分保或溢额分保，自留额不超过5000万元",
            risk_monitoring=[
                "定期分析赔付率趋势",
                "监控巨灾风险累积",
                "跟踪法律法规变化",
                "评估再保险安排充足性"
            ]
        )
    
    def _generate_financial_projection(self, product_type: str) -> FinancialProjection:
        """生成财务预测"""
        return FinancialProjection(
            premium_projection="首年保费目标5000万元，三年内达到1.5亿元",
            loss_ratio_estimate="预期赔付率55%-65%",
            expense_ratio="费用率控制在25%以内",
            combined_ratio="综合成本率预计85%-95%",
            profitability="预计第二年实现承保盈利，综合投资收益率可达5-8%"
        )
    
    def _generate_conclusion(self, product_type: str, risk_analysis: RiskAnalysis) -> Dict:
        """生成结论"""
        return {
            "conclusion": "经综合分析，本产品具有良好的市场前景和可控的风险水平，技术可行，建议立项开发。",
            "recommendations": [
                "采用稳健的定价策略，确保费率充足",
                "建立完善的核保理赔制度",
                "合理安排再保险，控制累积风险",
                "加强产品培训和推广"
            ],
            "next_steps": [
                "完成产品条款详细设计",
                "进行费率精算和定价",
                "准备监管备案材料",
                "开发承保理赔系统功能",
                "制定产品推广方案"
            ]
        }
    
    def export_report_document(self, report: FeasibilityReport) -> str:
        """导出报告文档（Markdown格式）"""
        doc = f"""# {report.product_name}开发可行性研究报告

**报告日期**: {report.report_date}

---

## 一、开发背景

### 1.1 背景描述
{report.development_background}

### 1.2 政策驱动
"""
        for policy in report.policy_drivers:
            doc += f"- {policy}\n"
        
        doc += f"""
### 1.3 市场需求
{report.market_demand}

---

## 二、保险责任

### 2.1 责任概述
{report.coverage_summary}

### 2.2 目标风险
"""
        for risk in report.target_risks:
            doc += f"- {risk}\n"
        
        doc += """
### 2.3 责任亮点
"""
        for highlight in report.coverage_highlights:
            doc += f"- {highlight}\n"
        
        doc += f"""
---

## 三、市场分析

### 3.1 市场背景
{report.market_analysis.market_background}

### 3.2 目标客户群
"""
        for customer in report.market_analysis.target_customers:
            doc += f"- {customer}\n"
        
        doc += f"""
### 3.3 市场规模
{report.market_analysis.market_size}

### 3.4 竞争格局
{report.market_analysis.competitive_landscape}

### 3.5 市场机会
{report.market_analysis.market_opportunity}

---

## 四、风险分析

### 4.1 风险识别
"""
        for risk in report.risk_analysis.risk_identification:
            doc += f"- **{risk['风险类型']}**: 等级{risk['风险等级']}, 频率{risk['发生频率']}, 程度{risk['损失程度']}\n"
        
        doc += f"""
### 4.2 风险评估
{report.risk_analysis.risk_assessment}

### 4.3 历史损失数据
{report.risk_analysis.loss_history}

### 4.4 风险特征
{report.risk_analysis.risk_characteristics}

---

## 五、风险管控手段

### 5.1 核保管控
"""
        for control in report.risk_control.underwriting_control:
            doc += f"- {control}\n"
        
        doc += """
### 5.2 理赔管控
"""
        for control in report.risk_control.claims_control:
            doc += f"- {control}\n"
        
        doc += f"""
### 5.3 再保险安排
{report.risk_control.reinsurance_arrangement}

### 5.4 风险监控
"""
        for monitor in report.risk_control.risk_monitoring:
            doc += f"- {monitor}\n"
        
        doc += f"""
---

## 六、财务预测

### 6.1 保费预测
{report.financial_projection.premium_projection}

### 6.2 赔付率预估
{report.financial_projection.loss_ratio_estimate}

### 6.3 费用率
{report.financial_projection.expense_ratio}

### 6.4 综合成本率
{report.financial_projection.combined_ratio}

### 6.5 盈利性分析
{report.financial_projection.profitability}

---

## 七、可行性结论与建议

### 7.1 可行性结论
{report.feasibility_conclusion}

### 7.2 开发建议
"""
        for rec in report.development_recommendations:
            doc += f"- {rec}\n"
        
        doc += """
### 7.3 下一步工作
"""
        for step in report.next_steps:
            doc += f"- {step}\n"
        
        return doc


def main():
    """主函数"""
    generator = FeasibilityReportGenerator()
    
    print("=" * 60)
    print("步骤4：撰写产品条款开发可行性研究报告")
    print("=" * 60)
    
    # 读取前几步的结果
    try:
        with open("step1_subject_analysis.json", "r", encoding="utf-8") as f:
            subject_info = json.load(f)
    except:
        subject_info = {}
    
    try:
        with open("step3_coverage_design.json", "r", encoding="utf-8") as f:
            coverage_info = json.load(f)
    except:
        coverage_info = {}
    
    # 输入产品信息
    product_name = input("\n请输入产品名称: ")
    product_type = input("请输入产品类型: ")
    
    # 生成报告
    report = generator.generate_report(
        product_name=product_name,
        product_type=product_type,
        subject_info=subject_info,
        coverage_info=coverage_info
    )
    
    # 导出文档
    doc = generator.export_report_document(report)
    
    # 保存文档
    filename = f"{product_name}可行性研究报告.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(doc)
    
    print(f"\n✓ 可行性研究报告已生成: {filename}")
    
    # 保存结构化数据
    with open("step4_feasibility_report.json", "w", encoding="utf-8") as f:
        json.dump(report.to_dict(), f, ensure_ascii=False, indent=2)
    
    print("✓ 报告数据已保存到 step4_feasibility_report.json")
    
    return report


if __name__ == "__main__":
    main()
