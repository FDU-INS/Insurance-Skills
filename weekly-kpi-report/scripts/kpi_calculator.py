#!/usr/bin/env python3
"""
华安保险车险周报 KPI 计算器 v2.0
支持多种数据格式(Excel/CSV)和字段映射(中文/英文)
提取董事会关注的核心指标,支持可配置的预警阈值
"""
import pandas as pd
import numpy as np
import json
import sys
import os
from datetime import datetime

# 加载配置文件
def load_config():
    """加载业务规则配置"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "预警阈值": {
                "综合成本率_上限": 95,
                "新能源车赔付率差距": 10,
                "出险频度_上限": 25
            }
        }

def load_field_mapping():
    """加载字段映射配置"""
    mapping_path = os.path.join(os.path.dirname(__file__), '..', 'field_mapping.json')
    try:
        with open(mapping_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ Warning: field_mapping.json not found, using fallback mapping", file=sys.stderr)
        return None

CONFIG = load_config()
FIELD_MAPPING = load_field_mapping()

def get_field(df, logical_name):
    """
    根据逻辑字段名获取实际数据列
    自动匹配中文/英文字段名
    """
    if FIELD_MAPPING is None:
        # Fallback: 尝试常见字段名
        fallback_mappings = {
            'premium': ['signed_premium_yuan', '跟单保费(Ten Thousand)', '签单保费'],
            'business_type': ['business_type_category', '业务类型分类'],
            'third_level_org': ['third_level_organization', '三级机构'],
            'is_nev': ['is_new_energy_vehicle', '是否新能源车1'],
            'policy_count': ['policy_count', '保单数'],
            'claim_cases': ['claim_case_count', '出险次数'],
            'claim_amount': ['reported_claim_payment_yuan', '报案赔款'],
            'expense_amount': ['expense_amount_yuan', '费用金额'],
            'customer_category': ['customer_category_3', '客户类别3'],
            'renewal_status': ['renewal_status', '续保情况']
        }
        aliases = fallback_mappings.get(logical_name, [])
    else:
        field_config = FIELD_MAPPING['field_mappings'].get(logical_name, {})
        aliases = field_config.get('aliases', [])

    # 尝试匹配字段
    for alias in aliases:
        if alias in df.columns:
            return df[alias]

    # 未找到字段
    raise KeyError(f"找不到逻辑字段 '{logical_name}' 对应的实际字段。尝试过: {aliases}")

def get_field_name(df, logical_name):
    """获取实际存在的字段名"""
    if FIELD_MAPPING is None:
        fallback_mappings = {
            'premium': ['signed_premium_yuan', '跟单保费(Ten Thousand)'],
            'business_type': ['business_type_category', '业务类型分类']
        }
        aliases = fallback_mappings.get(logical_name, [])
    else:
        field_config = FIELD_MAPPING['field_mappings'].get(logical_name, {})
        aliases = field_config.get('aliases', [])

    for alias in aliases:
        if alias in df.columns:
            return alias

    return None

def normalize_boolean_field(series):
    """标准化布尔字段(True/False, 是/否等)"""
    true_values = [True, 'True', '是', 'Y', 'yes', 1, '1']
    return series.isin(true_values)

def load_and_clean_data(file_path):
    """加载并清洗数据,自动检测格式"""
    file_ext = os.path.splitext(file_path)[1].lower()

    # 根据文件扩展名选择加载方式
    if file_ext in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path)
        print(f"✅ 已加载 Excel 文件: {file_path}", file=sys.stderr)
    elif file_ext == '.csv':
        # 尝试不同编码
        for encoding in ['utf-8', 'utf-8-sig', 'gb2312', 'gbk']:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                print(f"✅ 已加载 CSV 文件: {file_path} (编码: {encoding})", file=sys.stderr)
                break
            except UnicodeDecodeError:
                continue
        else:
            raise ValueError(f"无法以任何编码读取CSV文件: {file_path}")
    else:
        raise ValueError(f"不支持的文件格式: {file_ext}")

    print(f"📊 数据行数: {len(df)}, 列数: {len(df.columns)}", file=sys.stderr)
    print(f"📋 列名: {list(df.columns[:10])}..." if len(df.columns) > 10 else f"📋 列名: {list(df.columns)}", file=sys.stderr)

    return df

def calculate_business_scale(df):
    """业务规模指标"""
    premium = get_field(df, 'premium')
    policy_count = get_field(df, 'policy_count')
    business_type = get_field(df, 'business_type')

    # 检查保费字段单位(是否需要转换)
    premium_field_name = get_field_name(df, 'premium')
    if 'Ten Thousand' in premium_field_name:
        premium_sum = premium.sum()  # 已经是万元
        unit = "万元"
    else:
        premium_sum = premium.sum() / 10000  # 转换为万元
        unit = "万元(从元转换)"

    total_policies = policy_count.sum()
    avg_premium = premium.sum() / total_policies if total_policies > 0 else 0

    # 业务类型分布
    business_type_dist = df.groupby(business_type.name)[premium.name].sum().sort_values(ascending=False).head(5).to_dict()

    return {
        '总保费_万元': round(premium_sum, 2),
        '保费单位': unit,
        '保单数量': int(total_policies),
        '单均保费_元': round(avg_premium if 'yuan' in premium_field_name else avg_premium * 10000, 2),
        '业务类型占比': business_type_dist
    }

def calculate_profitability(df):
    """盈利能力指标"""
    premium = get_field(df, 'premium')
    claim_amount = get_field(df, 'claim_amount')
    expense_amount = get_field(df, 'expense_amount')

    total_premium = premium.sum()
    total_claims = claim_amount.sum()
    total_expense = expense_amount.sum()

    loss_ratio = (total_claims / total_premium * 100) if total_premium > 0 else 0
    expense_ratio = (total_expense / total_premium * 100) if total_premium > 0 else 0
    combined_ratio = loss_ratio + expense_ratio

    # 尝试获取边际贡献
    try:
        marginal_contrib = get_field(df, 'marginal_contribution')
        total_margin = marginal_contrib.sum()
    except KeyError:
        total_margin = total_premium - total_claims - total_expense

    return {
        '赔付率_%': round(loss_ratio, 2),
        '费用率_%': round(expense_ratio, 2),
        '综合成本率_%': round(combined_ratio, 2),
        '边际贡献_元': round(total_margin, 2),
        '总赔款_元': round(total_claims, 2),
        '总费用_元': round(total_expense, 2)
    }

def calculate_nev_insights(df):
    """新能源车专题分析"""
    try:
        is_nev = normalize_boolean_field(get_field(df, 'is_nev'))
        premium = get_field(df, 'premium')
        claim_amount = get_field(df, 'claim_amount')
        policy_count = get_field(df, 'policy_count')

        nev_mask = is_nev
        traditional_mask = ~is_nev

        nev_policies = policy_count[nev_mask].sum()
        total_policies = policy_count.sum()

        if nev_policies == 0:
            return {'新能源车数据': '无新能源车保单'}

        nev_premium = premium[nev_mask].sum()
        nev_claims = claim_amount[nev_mask].sum()
        traditional_claims = claim_amount[traditional_mask].sum()
        traditional_premium = premium[traditional_mask].sum()

        nev_loss_ratio = (nev_claims / nev_premium * 100) if nev_premium > 0 else 0
        traditional_loss_ratio = (traditional_claims / traditional_premium * 100) if traditional_premium > 0 else 0

        return {
            '新能源车渗透率_%': round(nev_policies / total_policies * 100, 2),
            '新能源车保单数': int(nev_policies),
            '新能源车赔付率_%': round(nev_loss_ratio, 2),
            '传统车赔付率_%': round(traditional_loss_ratio, 2),
            '赔付率差距_pp': round(nev_loss_ratio - traditional_loss_ratio, 2)
        }
    except KeyError as e:
        return {'新能源车数据': f'字段缺失: {str(e)}'}

def calculate_risk_metrics(df):
    """风险管理指标"""
    try:
        claim_cases = get_field(df, 'claim_cases')
        policy_count = get_field(df, 'policy_count')
        claim_amount = get_field(df, 'claim_amount')

        total_policies = policy_count.sum()
        total_claims = claim_cases.sum()
        total_claim_amount = claim_amount.sum()

        claim_frequency = (total_claims / total_policies * 100) if total_policies > 0 else 0
        avg_claim_amount = (total_claim_amount / total_claims) if total_claims > 0 else 0

        return {
            '出险频度_%': round(claim_frequency, 2),
            '总案件数': int(total_claims),
            '案均赔款_元': round(avg_claim_amount, 2),
            '出险保单占比_%': round(claim_frequency, 2)
        }
    except KeyError as e:
        return {'风险指标': f'字段缺失: {str(e)}'}

def calculate_customer_mix(df):
    """客户结构分析"""
    try:
        renewal_status = get_field(df, 'renewal_status')
        premium = get_field(df, 'premium')
        policy_count = get_field(df, 'policy_count')
        customer_category = get_field(df, 'customer_category')
        third_level_org = get_field(df, 'third_level_org')

        # 续保率计算
        renewal_mask = renewal_status == '续保'
        renewal_policies = policy_count[renewal_mask].sum()
        total_policies = policy_count.sum()
        renewal_rate = (renewal_policies / total_policies * 100) if total_policies > 0 else 0

        # 客户类别分布
        customer_dist = df.groupby(customer_category.name)[premium.name].sum().sort_values(ascending=False).head(5).to_dict()

        # 三级机构贡献
        org_contrib = df.groupby(third_level_org.name)[premium.name].sum().sort_values(ascending=False).head(5).to_dict()

        return {
            '续保率_%': round(renewal_rate, 2),
            '续保保单数': int(renewal_policies),
            '客户类别分布_TOP5': customer_dist,
            '三级机构贡献_TOP5': org_contrib
        }
    except KeyError as e:
        return {'客户结构': f'字段缺失: {str(e)}'}

def generate_action_items(kpis):
    """基于 KPI 自动生成行动建议"""
    actions = []
    thresholds = CONFIG.get('预警阈值', {})

    # 综合成本率预警
    if '盈利能力' in kpis and '综合成本率_%' in kpis['盈利能力']:
        combined_ratio = kpis['盈利能力']['综合成本率_%']
        ratio_limit = thresholds.get('综合成本率_上限', 95)
        ratio_danger = thresholds.get('综合成本率_危险线', 100)

        if combined_ratio > ratio_danger:
            actions.append(f"⚠️ 综合成本率达{combined_ratio}%，超过危险线，建议立即收紧承保")
        elif combined_ratio > ratio_limit:
            actions.append(f"⚠️ 综合成本率达{combined_ratio}%，建议收紧高成本业务承保")

    # 新能源车预警
    if '新能源车分析' in kpis and '赔付率差距_pp' in kpis['新能源车分析']:
        gap = kpis['新能源车分析']['赔付率差距_pp']
        nev_gap_threshold = thresholds.get('新能源车赔付率差距', 10)

        if gap > nev_gap_threshold:
            actions.append(f"🔋 新能源车赔付率较传统车高{round(gap, 1)}个百分点，建议优化定价模型")

    # 出险频度预警
    if '风险指标' in kpis and '出险频度_%' in kpis['风险指标']:
        freq = kpis['风险指标']['出险频度_%']
        freq_limit = thresholds.get('出险频度_上限', 25)

        if freq > freq_limit:
            actions.append(f"🚨 平均出险频度{freq}%偏高，建议加强风险筛查")

    # 续保率预警
    if '客户结构' in kpis and '续保率_%' in kpis['客户结构']:
        renewal_rate = kpis['客户结构']['续保率_%']

        if renewal_rate < 45:
            actions.append(f"📉 续保率{renewal_rate}%偏低，建议强化客户维护")

    return actions if actions else ["✅ 本周业务指标运行平稳"]

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python kpi_calculator.py <file_path> [week_number]"}, ensure_ascii=False))
        sys.exit(1)

    file_path = sys.argv[1]
    week_num = sys.argv[2] if len(sys.argv) > 2 else "未知"

    try:
        print(f"\n🚀 开始处理: {file_path}", file=sys.stderr)
        df = load_and_clean_data(file_path)

        kpis = {
            'week_number': week_num,
            'calculation_date': datetime.now().strftime("%Y-%m-%d"),
            'data_summary': {
                'total_records': len(df),
                'data_source': os.path.basename(file_path)
            },
            '业务规模': calculate_business_scale(df),
            '盈利能力': calculate_profitability(df),
            '新能源车分析': calculate_nev_insights(df),
            '风险指标': calculate_risk_metrics(df),
            '客户结构': calculate_customer_mix(df)
        }

        kpis['行动建议'] = generate_action_items(kpis)

        # 保存 KPI 到 JSON
        output_dir = os.path.join(os.path.dirname(__file__), '..')
        output_path = os.path.join(output_dir, f'kpis_week_{week_num}.json')

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(kpis, f, ensure_ascii=False, indent=2)

        print(f"\n✅ KPI计算完成", file=sys.stderr)
        print(f"📁 输出文件: {output_path}", file=sys.stderr)
        print(f"📊 综合成本率: {kpis['盈利能力'].get('综合成本率_%', 'N/A')}%", file=sys.stderr)

        # 标准输出JSON结果
        print(json.dumps({
            "status": "success",
            "kpi_file": output_path,
            "summary": {
                "week": week_num,
                "records": len(df),
                "combined_ratio": kpis['盈利能力'].get('综合成本率_%', None)
            }
        }, ensure_ascii=False, indent=2))

    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"\n❌ 错误: {str(e)}", file=sys.stderr)
        print(error_detail, file=sys.stderr)
        print(json.dumps({"error": str(e), "traceback": error_detail}, ensure_ascii=False))
        sys.exit(1)

if __name__ == '__main__':
    main()
