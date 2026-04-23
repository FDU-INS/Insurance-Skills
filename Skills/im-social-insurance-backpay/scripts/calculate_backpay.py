#!/usr/bin/env python3
"""
内蒙古养老保险补缴计算脚本
支持按历年社平工资计算补缴金额，包含本金、利息、滞纳金
"""

import argparse
import json
import sys
from datetime import datetime

BACKPAY_YEAR_MIN = 1996
BACKPAY_YEAR_MAX = 2025

# 内蒙古历年社平工资（年月平均工资，单位：元），与前端 baseForProvince 对齐
SOCIAL_AVG_WAGES = {
    1996: 4134 / 12,
    1997: 4716 / 12,
    1998: 5124 / 12,
    1999: 5796 / 12,
    2000: 6348 / 12,
    2001: 6972 / 12,
    2002: 8256 / 12,
    2003: 9684 / 12,
    2004: 11280 / 12,
    2005: 13320 / 12,
    2006: 15985 / 12,
    2007: 18468 / 12,
    2008: 21888 / 12,
    2009: 26112 / 12,
    2010: 30699 / 12,
    2011: 35507 / 12,
    2012: 41484 / 12,
    2013: 47052 / 12,
    2014: 51384 / 12,
    2015: 54460 / 12,
    2016: 57870 / 12,
    2017: 61994 / 12,
    2018: 67692 / 12,
    2019: 73836 / 12,
    2020: 68256 / 12,
    2021: 76128 / 12,
    2022: 6751,
    2023: 7649,
    2024: 8105,
    2025: 8179,
}

# 社保个人账户历年记账利率（年利率），与前端 rates 对齐
INTEREST_RATES = {
    1996: 0.10,
    1997: 0.08,
    1998: 0.06,
    1999: 0.05,
    2000: 0.05,
    2001: 0.05,
    2002: 0.05,
    2003: 0.0198,
    2004: 0.0225,
    2005: 0.0225,
    2006: 0.0252,
    2007: 0.031,
    2008: 0.0412,
    2009: 0.0225,
    2010: 0.023,
    2011: 0.05,
    2012: 0.05,
    2013: 0.05,
    2014: 0.05,
    2015: 0.05,
    2016: 0.0831,
    2017: 0.0712,
    2018: 0.0829,
    2019: 0.0761,
    2020: 0.0604,
    2021: 0.0669,
    2022: 0.0612,
    2023: 0.0397,
    2024: 0.0262,
    2025: 0.015,
    2026: 0.015,
}

PERSONAL_RATES = {
    1996: 0.03,
    1997: 0.03,
    1998: 0.04,
    1999: 0.04,
    2000: 0.05,
    2001: 0.06,
    2002: 0.06,
    2003: 0.07,
    2004: 0.07,
}
PERSONAL_RATE_DEFAULT = 0.08


def get_personal_rate(year: int) -> float:
    """获取个人缴费比例（2005 年起统一 8%，此前逐步提高）"""
    return PERSONAL_RATES.get(year, PERSONAL_RATE_DEFAULT)


def get_unit_rate(year: int, month: int) -> float:
    """获取单位缴费比例（随政策调整，含 2018-05 阶段性下调、2019-05 降至 16%）"""
    if year <= 1997:
        return 0.20
    if year <= 1999:
        return 0.26
    if year == 2000:
        return 0.25
    if year <= 2002:
        return 0.24
    if year <= 2004:
        return 0.23
    if year <= 2017:
        return 0.20
    if year == 2018:
        return 0.19 if month >= 5 else 0.20
    if year == 2019:
        return 0.16 if month >= 5 else 0.19
    return 0.16

def calculate_months_to_target(year, month, target_year, target_month):
    """计算从指定年月到目标年月的月数"""
    months = (target_year - year) * 12 + (target_month - month)
    return max(0, months)

def calculate_compound_interest(principal, year, month, rate, target_year, target_month):
    """计算复利利息"""
    months = calculate_months_to_target(year, month, target_year, target_month)
    if months <= 0 or rate <= 0:
        return 0, months
    
    monthly_rate = rate / 12
    final_amount = principal * ((1 + monthly_rate) ** months)
    interest = final_amount - principal
    
    return interest, months

def calculate_month_backpay(year, month, monthly_base, target_year, target_month):
    """计算单月补缴金额"""
    personal_rate = get_personal_rate(year)
    unit_rate = get_unit_rate(year, month)
    
    personal = monthly_base * personal_rate
    unit = monthly_base * unit_rate
    
    # 获取当年利率
    rate = INTEREST_RATES.get(year, 0.025)
    
    # 计算利息（从当月开始复利到目标时间）
    personal_int, _ = calculate_compound_interest(personal, year, month, rate, target_year, target_month)
    unit_int, _ = calculate_compound_interest(unit, year, month, rate, target_year, target_month)
    
    # 滞纳金计算（从次月1日到目标时间）
    if month == 12:
        late_start_year, late_start_month = year + 1, 1
    else:
        late_start_year, late_start_month = year, month + 1
    
    months_late = calculate_months_to_target(late_start_year, late_start_month, target_year, target_month)
    days_late = months_late * 30
    
    personal_late = personal * 0.0005 * days_late
    unit_late = unit * 0.0005 * days_late
    
    return {
        'year': year,
        'month': month,
        'personal_principal': personal,
        'unit_principal': unit,
        'personal_interest': personal_int,
        'unit_interest': unit_int,
        'personal_late_fee': personal_late,
        'unit_late_fee': unit_late,
    }

def calculate_backpay(
    start_year, start_month, end_year, end_month, base_rate,
    target_year=None, target_month=None,
    custom_monthly_base=None,
):
    """计算补缴金额

    custom_monthly_base: 用户自定义月缴费基数（元），设置后忽略 base_rate 和社平工资
    """
    if start_year < BACKPAY_YEAR_MIN or (end_year > BACKPAY_YEAR_MAX or (end_year == BACKPAY_YEAR_MAX and end_month > 12)):
        raise ValueError(
            f"补缴时段仅支持 {BACKPAY_YEAR_MIN} 年 1 月至 {BACKPAY_YEAR_MAX} 年 12 月，"
            f"{BACKPAY_YEAR_MIN} 年以前尚未建立个人账户制度，{BACKPAY_YEAR_MAX} 年以后暂无数据支持。"
        )

    if target_year is None:
        now = datetime.now()
        target_year, target_month = now.year, now.month
    
    total_personal_principal = 0
    total_unit_principal = 0
    total_personal_interest = 0
    total_unit_interest = 0
    total_personal_late_fee = 0
    total_unit_late_fee = 0
    
    yearly_results = {}
    
    year, month = start_year, start_month
    while (year < end_year) or (year == end_year and month <= end_month):
        if custom_monthly_base is not None:
            monthly_base = custom_monthly_base
        else:
            if year not in SOCIAL_AVG_WAGES:
                year += 1 if month == 12 else 0
                month = 1 if month == 12 else month + 1
                continue
            wage = SOCIAL_AVG_WAGES[year]
            monthly_base = wage * base_rate
        
        result = calculate_month_backpay(year, month, monthly_base, target_year, target_month)
        
        if year not in yearly_results:
            yearly_results[year] = {
                'months': [],
                'personal_principal': 0,
                'unit_principal': 0,
                'personal_interest': 0,
                'unit_interest': 0,
                'personal_late_fee': 0,
                'unit_late_fee': 0,
            }
        
        yearly_results[year]['months'].append(month)
        yearly_results[year]['personal_principal'] += result['personal_principal']
        yearly_results[year]['unit_principal'] += result['unit_principal']
        yearly_results[year]['personal_interest'] += result['personal_interest']
        yearly_results[year]['unit_interest'] += result['unit_interest']
        yearly_results[year]['personal_late_fee'] += result['personal_late_fee']
        yearly_results[year]['unit_late_fee'] += result['unit_late_fee']
        
        total_personal_principal += result['personal_principal']
        total_unit_principal += result['unit_principal']
        total_personal_interest += result['personal_interest']
        total_unit_interest += result['unit_interest']
        total_personal_late_fee += result['personal_late_fee']
        total_unit_late_fee += result['unit_late_fee']
        
        # 下个月
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
    
    # 汇总
    total_principal = total_personal_principal + total_unit_principal
    total_interest = total_personal_interest + total_unit_interest
    total_late_fee = total_personal_late_fee + total_unit_late_fee
    grand_total = total_principal + total_interest + total_late_fee
    
    # 无滞纳金版本
    total_without_late = total_principal + total_interest
    
    return {
        'start_date': f"{start_year}-{start_month:02d}",
        'end_date': f"{end_year}-{end_month:02d}",
        'target_date': f"{target_year}-{target_month:02d}",
        'base_rate': base_rate,
        'yearly_details': yearly_results,
        'summary': {
            'personal_principal': round(total_personal_principal, 2),
            'unit_principal': round(total_unit_principal, 2),
            'total_principal': round(total_principal, 2),
            'personal_interest': round(total_personal_interest, 2),
            'unit_interest': round(total_unit_interest, 2),
            'total_interest': round(total_interest, 2),
            'personal_late_fee': round(total_personal_late_fee, 2),
            'unit_late_fee': round(total_unit_late_fee, 2),
            'total_late_fee': round(total_late_fee, 2),
            'grand_total': round(grand_total, 2),
            'total_without_late_fee': round(total_without_late, 2),
        }
    }

def calculate_all_tiers(start_year, start_month, end_year, end_month, target_year=None, target_month=None):
    """计算所有档次的补缴金额"""
    tiers = [0.6, 0.8, 1.0, 1.5, 2.0, 3.0]
    tier_names = ['60%', '80%', '100%', '150%', '200%', '300%']
    
    results = {}
    for tier, name in zip(tiers, tier_names):
        result = calculate_backpay(start_year, start_month, end_year, end_month, tier, target_year, target_month)
        results[name] = result['summary']
    
    return results

def format_tier_comparison(results):
    """格式化多档次对比输出"""
    print("\n" + "="*120)
    print("【各档次补缴金额对比表】")
    print("="*120)
    
    # 表头
    header = f"{'项目':<20}"
    for tier in ['60%', '80%', '100%', '150%', '200%', '300%']:
        header += f"{tier:>16}"
    print(header)
    print("-"*120)
    
    # 个人本金
    row = f"{'个人本金':<20}"
    for tier in ['60%', '80%', '100%', '150%', '200%', '300%']:
        row += f"{results[tier]['personal_principal']:>15,.2f}"
    print(row)
    
    # 单位本金
    row = f"{'单位本金':<20}"
    for tier in ['60%', '80%', '100%', '150%', '200%', '300%']:
        row += f"{results[tier]['unit_principal']:>15,.2f}"
    print(row)
    
    # 本金小计
    row = f"{'本金小计':<20}"
    for tier in ['60%', '80%', '100%', '150%', '200%', '300%']:
        row += f"{results[tier]['total_principal']:>15,.2f}"
    print(row)
    print("-"*120)
    
    # 个人利息
    row = f"{'个人利息':<20}"
    for tier in ['60%', '80%', '100%', '150%', '200%', '300%']:
        row += f"{results[tier]['personal_interest']:>15,.2f}"
    print(row)
    
    # 单位利息
    row = f"{'单位利息':<20}"
    for tier in ['60%', '80%', '100%', '150%', '200%', '300%']:
        row += f"{results[tier]['unit_interest']:>15,.2f}"
    print(row)
    
    # 利息小计
    row = f"{'利息小计':<20}"
    for tier in ['60%', '80%', '100%', '150%', '200%', '300%']:
        row += f"{results[tier]['total_interest']:>15,.2f}"
    print(row)
    print("-"*120)
    
    # 个人滞纳金
    row = f"{'个人滞纳金':<20}"
    for tier in ['60%', '80%', '100%', '150%', '200%', '300%']:
        row += f"{results[tier]['personal_late_fee']:>15,.2f}"
    print(row)
    
    # 单位滞纳金
    row = f"{'单位滞纳金':<20}"
    for tier in ['60%', '80%', '100%', '150%', '200%', '300%']:
        row += f"{results[tier]['unit_late_fee']:>15,.2f}"
    print(row)
    
    # 滞纳金小计
    row = f"{'滞纳金小计':<20}"
    for tier in ['60%', '80%', '100%', '150%', '200%', '300%']:
        row += f"{results[tier]['total_late_fee']:>15,.2f}"
    print(row)
    print("-"*120)
    
    # 无滞纳金总计
    row = f"{'无滞纳金总计':<20}"
    for tier in ['60%', '80%', '100%', '150%', '200%', '300%']:
        row += f"{results[tier]['total_without_late_fee']:>15,.2f}"
    print(row)
    
    # 含滞纳金总计
    row = f"{'含滞纳金总计':<20}"
    for tier in ['60%', '80%', '100%', '150%', '200%', '300%']:
        row += f"{results[tier]['grand_total']:>15,.2f}"
    print(row)
    print("="*120)
    
    # 万元单位显示
    print("\n【万元单位显示】")
    print("-"*120)
    row = f"{'无滞纳金总计(万元)':<20}"
    for tier in ['60%', '80%', '100%', '150%', '200%', '300%']:
        row += f"{results[tier]['total_without_late_fee']/10000:>15.2f}"
    print(row)
    
    row = f"{'含滞纳金总计(万元)':<20}"
    for tier in ['60%', '80%', '100%', '150%', '200%', '300%']:
        row += f"{results[tier]['grand_total']/10000:>15.2f}"
    print(row)
    print("="*120)

def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description="内蒙古养老保险补缴计算工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例:\n"
            "  python calculate_backpay.py 2004 4 2011 3\n"
            "  python calculate_backpay.py 2004 4 2011 3 --rate 0.6 --target 2026 3\n"
            "  python calculate_backpay.py 2004 4 2011 3 --all --target 2026 3\n"
            "  python calculate_backpay.py 2004 4 2011 3 --monthly-base 5000\n"
        ),
    )
    parser.add_argument("start_year", type=int, help="补缴起始年")
    parser.add_argument("start_month", type=int, help="补缴起始月")
    parser.add_argument("end_year", type=int, help="补缴终止年")
    parser.add_argument("end_month", type=int, help="补缴终止月")
    parser.add_argument("--rate", type=float, default=0.6, help="缴费档次比例，默认 0.6（60%%）")
    parser.add_argument("--all", action="store_true", dest="all_tiers", help="计算全部六档对比")
    parser.add_argument("--target", type=int, nargs=2, metavar=("YEAR", "MONTH"), help="补缴时间，默认当前年月")
    parser.add_argument("--monthly-base", type=float, default=None, help="自定义月缴费基数（元），设置后忽略 --rate 和社平工资")
    return parser


def main():
    """主函数"""
    parser = build_parser()
    args = parser.parse_args()

    if args.start_year < BACKPAY_YEAR_MIN:
        parser.error(f"补缴起始年不能早于 {BACKPAY_YEAR_MIN} 年（此前尚未建立个人账户制度）")
    if args.end_year > BACKPAY_YEAR_MAX or (args.end_year == BACKPAY_YEAR_MAX and args.end_month > 12):
        parser.error(f"补缴终止年不能晚于 {BACKPAY_YEAR_MAX} 年 12 月（之后暂无数据支持）")

    target_year = args.target[0] if args.target else None
    target_month = args.target[1] if args.target else None

    if args.all_tiers:
        if args.monthly_base is not None:
            parser.error("--all 模式按社平工资×档次计算，不支持同时指定 --monthly-base")
        results = calculate_all_tiers(
            args.start_year, args.start_month, args.end_year, args.end_month,
            target_year, target_month,
        )
        format_tier_comparison(results)
        print("\n【JSON格式输出】")
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        result = calculate_backpay(
            args.start_year, args.start_month, args.end_year, args.end_month,
            args.rate, target_year, target_month,
            custom_monthly_base=args.monthly_base,
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
