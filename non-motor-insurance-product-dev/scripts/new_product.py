"""
非车险产品开发辅助工具
========================
支持创建标准化的产品开发项目结构
"""

import os
import shutil
from datetime import datetime

# 产品险种大类编码
CATEGORY_CODES = {
    '企财险': 'QC',
    '货运险': 'HY',
    '责任险': 'ZR',
    '保证险': 'BZ',
    '意外险': 'YW',
    '健康险': 'JK',
    '家财险': 'JF',
    '工程险': 'GC',
    '船舶险': 'CB',
    '信用险': 'XY',
    '特殊风险': 'TS',
    '其他': 'QT'
}

# 通用条款板块模板
STANDARD_SECTIONS = """
# {product_name}

{company_name}
{product_name}条款

## 总则
第{num}条 本保险合同由保险条款、投保单、保险单、保险凭证以及批单组成。凡涉及本保险合同的约定，均应采用书面形式。
第{num}条 {def_content}

## 保险标的
第{num}条 本保险合同的保险标的是指：{coverage}

## 保险责任
第{num}条 在保险期间内，因下列原因造成保险标的的损失，保险人按照本保险合同的约定负责赔偿：
（一）{risk_1}
（二）{risk_2}

## 责任免除
第{num}条 下列原因造成的损失、费用，保险人不负责赔偿：
（一）{exclusion_1}
（二）{exclusion_2}

第{num}条 下列损失、费用，保险人也不负责赔偿：
（一）{exclusion_3}
（二）{exclusion_4}

## 保险金额/赔偿限额
第{num}条 {amount_rule}

## 免赔额（率）
第{num}条 {deductible_rule}

## 保险期间
第{num}条 除另有约定外，保险期间为{period}，以本保险合同载明的起讫时间为准。

## 投保人/被保险人义务
第{num}条 订立本保险合同时，保险人就保险标的或者被保险人的有关情况提出询问的，投保人应当如实告知。
第{num}条 投保人应当按照本保险合同的约定交付保险费。

## 赔偿处理
第{num}条 保险事故发生后，被保险人应当及时通知保险人，并提供相关证明材料。
第{num}条 保险人收到赔偿请求后，应当及时作出核定；情形复杂的，应当在{day}日内作出核定。

## 代位追偿
第{num}条 保险人向第三者行使代位请求赔偿权利时，被保险人应当向保险人提供必要的文件和其所知道的有关情况。

## 争议处理
第{num}条 因履行本保险合同发生的争议，由当事人协商解决；协商不成的，提交{location}仲裁委员会仲裁（或依法向人民法院提起诉讼）。
"""

# 费率表模板
RATE_TABLE_TEMPLATE = """
# {product_name}费率表

{company_name}
{product_name}费率表

## 一、基准费率
{base_rate}

## 二、费率调整系数
{adjustment_factors}

## 三、费率计算公式
{formula}

## 四、费率计算示例
### 示例1
- 条件：{example_1_condition}
- 计算过程：{example_1_calculation}
- 保费：{example_1_premium}

### 示例2
- 条件：{example_2_condition}
- 计算过程：{example_2_calculation}
- 保费：{example_2_premium}

## 五、最低保费
{minimum_premium}
"""

# 可研报告模板
FEASIBILITY_REPORT_TEMPLATE = """
# {product_name}产品开发可行性研究报告

{company_name}
{product_name}
开发可行性研究报告

## 一、总体开发说明
根据国家金融监督管理总局印发的《关于加强非车险业务监管有关事项的通知》（金发〔2025〕36号），《财产保险公司保险条款和保险费率管理办法》（银保监会令2021年第10号）以及《财产保险公司保险产品开发指引》（保监发〔2016〕115号）等相关监管规定要求，为保护投保人、被保险人利益，确保产品开发的合理性，保障公司经营的稳健性，维护保险市场秩序，{company_name}（以下称"我司"）深入调研市场，在总结、借鉴同业公司产品和经验的基础上，根据我司目标业务，开发了本保险产品。

## 二、开发背景
### 2.1 市场规模
{market_size}

### 2.2 政策支持
{policy_support}

### 2.3 法律依据
{legal_basis}

## 三、产品主要特点
### 3.1 投保人/被保险人
{insured_info}

### 3.2 保险责任
{coverage_highlights}

### 3.3 责任免除
{exclusions_highlights}

### 3.4 保险金额/责任限额
{limit_info}

### 3.5 保险期间
{period_info}

## 四、保险费率及保费测算
### 4.1 费率结构
{rate_structure}

### 4.2 保费测算
{premium_estimation}

## 五、风险分析及风险控制
### 5.1 主要风险
{risks}

### 5.2 风险控制措施
{risk_controls}

## 六、经营模式
### 6.1 销售模式
{sales_model}

### 6.2 承保流程
{underwriting_process}

### 6.3 理赔流程
{claims_process}

### 6.4 业绩监控
{performance_monitoring}

## 七、总体结论
{conclusion}
"""


def create_product_folder(product_name, company_name="太平科技保险股份有限公司", category="其他"):
    """创建标准化的产品开发目录"""
    
    # 生成编码
    category_code = CATEGORY_CODES.get(category, 'QT')
    today = datetime.now().strftime('%Y%m%d')
    folder_name = f"{company_name}_{product_name}"
    
    # 创建目录
    if not os.path.exists('cases'):
        os.makedirs('cases')
    
    product_path = os.path.join('cases', folder_name)
    if os.path.exists(product_path):
        print(f"警告: 目录已存在: {product_path}")
        return product_path
    
    os.makedirs(product_path)
    print(f"创建目录: {product_path}")
    
    # 创建文档模板
    create_template_files(product_path, product_name, company_name, category, category_code)
    
    return product_path


def create_template_files(product_path, product_name, company_name, category, category_code):
    """创建标准化的文档模板"""
    
    # 1. 条款模板
    clause_file = os.path.join(product_path, f"{company_name}_{product_name}条款.md")
    with open(clause_file, 'w', encoding='utf-8') as f:
        f.write(f"""---
source_file: {company_name}_{product_name}条款.docx
product: {product_name}
category: {category}
category_code: {category_code}
type: clause
version: 1.0
date: {datetime.now().strftime('%Y-%m-%d')}
---
""")
        f.write(f"\n{STANDARD_SECTIONS.format(\n")
        f.write(f"    product_name=product_name,\n")
        f.write(f"    company_name=company_name,\n")
        f.write(f"    num='一',\n")
        f.write(f"    def_content='被保险人须为...',\n")
        f.write(f"    coverage='...',\n")
        f.write(f"    risk_1='自然灾害或意外事故',\n")
        f.write(f"    risk_2='',\n")
        f.write(f"    exclusion_1='投保人、被保险人的故意行为',\n")
        f.write(f"    exclusion_2='战争、军事行动',\n")
        f.write(f"    exclusion_3='各种间接损失',\n")
        f.write(f"    exclusion_4='自然磨损等',\n")
        f.write(f"    amount_rule='保险金额由双方协商确定',\n")
        f.write(f"    deductible_rule='免赔额由双方协商确定',\n")
        f.write(f"    period='一年',\n")
        f.write(f"    day='30',\n")
        f.write(f"    location='保险合同载明的'\n")
        f.write(")")
    print(f"  创建: {clause_file}")
    
    # 2. 费率表模板
    rate_file = os.path.join(product_path, f"{company_name}_{product_name}费率表.md")
    with open(rate_file, 'w', encoding='utf-8') as f:
        f.write(f"""---
source_file: {company_name}_{product_name}费率表.docx
product: {product_name}
category: {category}
category_code: {category_code}
type: rate_table
version: 1.0
date: {datetime.now().strftime('%Y-%m-%d')}
---
""")
        f.write(f"\n{RATE_TABLE_TEMPLATE.format(\n")
        f.write(f"    product_name=product_name,\n")
        f.write(f"    company_name=company_name,\n")
        f.write(f"    base_rate='基准费率：X‰（千分比）',\n")
        f.write(f"    adjustment_factors='1. 风险等级系数：1.0-2.0\\n2. 免赔额系数：0.8-1.2',\n")
        f.write(f"    formula='保费 = 保险金额 × 基准费率 × 费率调整系数',\n")
        f.write(f"    example_1_condition='保险金额100万元，风险等级1级，免赔额1万元',\n")
        f.write(f"    example_1_calculation='100万 × 2‰ × 1.0 × 1.0',\n")
        f.write(f"    example_1_premium='2000元',\n")
        f.write(f"    example_2_condition='保险金额500万元，风险等级2级，免赔额5万元',\n")
        f.write(f"    example_2_calculation='500万 × 2‰ × 1.2 × 0.9',\n")
        f.write(f"    example_2_premium='10800元',\n")
        f.write(f"    minimum_premium='每笔业务最低保费不低于XXX元'\n")
        f.write(")")
    print(f"  创建: {rate_file}")
    
    # 3. 可研报告模板
    feas_file = os.path.join(product_path, f"{company_name}_{product_name}产品开发可行性研究报告.md")
    with open(feas_file, 'w', encoding='utf-8') as f:
        f.write(f"""---
source_file: {company_name}_{product_name}产品开发可行性研究报告.docx
product: {product_name}
category: {category}
category_code: {category_code}
type: feasibility_report
version: 1.0
date: {datetime.now().strftime('%Y-%m-%d')}
---
""")
        f.write(f"\n{FEASIBILITY_REPORT_TEMPLATE.format(\n")
        f.write(f"    product_name=product_name,\n")
        f.write(f"    company_name=company_name,\n")
        f.write(f"    market_size='[填写市场规模数据]',\n")
        f.write(f"    policy_support='[填写相关政策]',\n")
        f.write(f"    legal_basis='[填写法律依据]',\n")
        f.write(f"    insured_info='[填写投保人/被保险人条件]',\n")
        f.write(f"    coverage_highlights='[填写主要保险责任]',\n")
        f.write(f"    exclusions_highlights='[填写主要责任免除]',\n")
        f.write(f"    limit_info='[填写金额/限额设定]',\n")
        f.write(f"    period_info='[填写保险期间]',\n")
        f.write(f"    rate_structure='[填写费率结构]',\n")
        f.write(f"    premium_estimation='[填写预期保费]',\n")
        f.write(f"    risks='[填写主要风险]',\n")
        f.write(f"    risk_controls='[填写风控措施]',\n")
        f.write(f"    sales_model='[填写销售模式]',\n")
        f.write(f"    underwriting_process='[填写承保流程]',\n")
        f.write(f"    claims_process='[填写理赔流程]',\n")
        f.write(f"    performance_monitoring='[填写业绩监控]',\n")
        f.write(f"    conclusion='[填写总体结论]'\n")
        f.write(")")
    print(f"  创建: {feas_file}")


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python new_product.py <产品名称> [险种大类]")
        print("\n险种大类选项:")
        for cat in CATEGORY_CODES.keys():
            print(f"  - {cat}")
        return
    
    product_name = sys.argv[1]
    category = sys.argv[2] if len(sys.argv) > 2 else "其他"
    
    if category not in CATEGORY_CODES:
        print(f"错误: 未知的险种大类 '{category}'")
        return
    
    print(f"\n{'='*60}")
    print(f"创建产品开发项目: {product_name}")
    print(f"险种大类: {category}")
    print(f"{'='*60}\n")
    
    path = create_product_folder(product_name, category=category)
    
    print(f"\n{'='*60}")
    print("创建完成！")
    print(f"目录: {path}")
    print("\n生成的文件:")
    print("  1. XX条款.md - 条款文件模板")
    print("  2. XX费率表.md - 费率表模板")
    print("  3. XX可研报告.md - 可行性研究报告模板")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
