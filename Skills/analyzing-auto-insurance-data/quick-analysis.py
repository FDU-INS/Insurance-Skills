#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速车险业务分析脚本
用于Claude Skill的快速数据分析和报告生成
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import sys
import os

def load_insurance_data(file_path):
    """加载车险数据文件"""
    try:
        if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            return pd.read_excel(file_path)
        elif file_path.endswith('.csv'):
            return pd.read_csv(file_path, encoding='utf-8')
        else:
            raise ValueError("不支持的文件格式，请使用.xlsx, .xls或.csv文件")
    except Exception as e:
        print(f"数据加载失败: {e}")
        return None

def basic_statistics(df):
    """基础统计分析"""
    stats = {
        '总保单数': len(df),
        '总保费': df['总保费'].sum() if '总保费' in df.columns else 0,
        '平均保费': df['总保费'].mean() if '总保费' in df.columns else 0,
        '手续费总额': df['手续费'].sum() if '手续费' in df.columns else 0,
        '平均手续费率': (df['手续费'] / df['总保费']).mean() if all(col in df.columns for col in ['手续费', '总保费']) else 0
    }
    return stats

def customer_analysis(df):
    """客户结构分析"""
    if '客户类别' not in df.columns:
        return {}
    
    customer_stats = df['客户类别'].value_counts()
    customer_percentages = (customer_stats / len(df) * 100).round(1)
    
    return {
        '客户分布': dict(customer_stats),
        '客户占比': dict(customer_percentages),
        '主要客户类型': customer_stats.index[0] if len(customer_stats) > 0 else '未知'
    }

def insurance_type_analysis(df):
    """险别组合分析"""
    if '险别组合' not in df.columns:
        return {}
    
    insurance_stats = df['险别组合'].value_counts()
    insurance_percentages = (insurance_stats / len(df) * 100).round(1)
    
    return {
        '险别分布': dict(insurance_stats),
        '险别占比': dict(insurance_percentages),
        '主要险别': insurance_stats.index[0] if len(insurance_stats) > 0 else '未知'
    }

def renewal_analysis(df):
    """续保情况分析"""
    if '续保情况' not in df.columns:
        return {}
    
    renewal_stats = df['续保情况'].value_counts()
    renewal_percentages = (renewal_stats / len(df) * 100).round(1)
    
    return {
        '续保分布': dict(renewal_stats),
        '续保占比': dict(renewal_percentages)
    }

def institution_analysis(df):
    """机构分析"""
    if '三级机构' not in df.columns:
        return {}
    
    institution_stats = df['三级机构'].value_counts()
    institution_percentages = (institution_stats / len(df) * 100).round(1)
    
    # 检查机构集中度
    max_institution = institution_stats.index[0] if len(institution_stats) > 0 else '未知'
    max_percentage = institution_percentages.iloc[0] if len(institution_percentages) > 0 else 0
    
    concentration_risk = "高" if max_percentage > 40 else "中" if max_percentage > 25 else "低"
    
    return {
        '机构分布': dict(institution_stats),
        '机构占比': dict(institution_percentages),
        '最大机构': max_institution,
        '最大占比': max_percentage,
        '集中度风险': concentration_risk
    }

def daily_trend_analysis(df):
    """日度趋势分析"""
    if '投保确认时间' not in df.columns:
        return {}
    
    # 转换日期格式
    df['日期'] = pd.to_datetime(df['投保确认时间']).dt.date
    
    # 按日期汇总
    daily_stats = df.groupby('日期').agg({
        '总保费': 'sum',
        '总保费': 'count'
    }).rename(columns={'总保费': '保单数'})
    
    # 计算日环比变化
    daily_stats['保费变化率'] = daily_stats['总保费'].pct_change() * 100
    daily_stats['保单数变化率'] = daily_stats['保单数'].pct_change() * 100
    
    # 识别异常波动（超过10%）
    abnormal_days = daily_stats[abs(daily_stats['保费变化率']) > 10]
    
    return {
        '日度统计': daily_stats.to_dict(),
        '异常天数': len(abnormal_days),
        '最大波动': daily_stats['保费变化率'].max(),
        '最小波动': daily_stats['保费变化率'].min()
    }

def generate_quick_report(df, file_name):
    """生成快速分析报告"""
    print(f"\n{'='*60}")
    print(f"车险业务数据快速分析报告")
    print(f"数据来源: {file_name}")
    print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # 基础统计
    print("📊 基础统计")
    print("-" * 30)
    basic_stats = basic_statistics(df)
    for key, value in basic_stats.items():
        if '率' in key:
            print(f"{key}: {value:.2%}")
        elif '保费' in key or '手续费' in key:
            print(f"{key}: {value:,.2f}万元")
        else:
            print(f"{key}: {value:,}")
    
    # 客户分析
    print("\n👥 客户结构分析")
    print("-" * 30)
    customer_stats = customer_analysis(df)
    if customer_stats:
        print(f"主要客户类型: {customer_stats['主要客户类型']}")
        if '客户占比' in customer_stats:
            top_customers = dict(list(customer_stats['客户占比'].items())[:3])
            for customer_type, percentage in top_customers.items():
                print(f"  {customer_type}: {percentage}%")
    
    # 险别分析
    print("\n🛡️ 险别组合分析")
    print("-" * 30)
    insurance_stats = insurance_type_analysis(df)
    if insurance_stats:
        print(f"主要险别: {insurance_stats['主要险别']}")
        if '险别占比' in insurance_stats:
            top_insurance = dict(list(insurance_stats['险别占比'].items())[:3])
            for insurance_type, percentage in top_insurance.items():
                print(f"  {insurance_type}: {percentage}%")
    
    # 续保分析
    print("\n🔄 续保情况分析")
    print("-" * 30)
    renewal_stats = renewal_analysis(df)
    if renewal_stats:
        if '续保占比' in renewal_stats:
            for renewal_type, percentage in renewal_stats['续保占比'].items():
                print(f"  {renewal_type}: {percentage}%")
    
    # 机构分析
    print("\n🏢 机构分析")
    print("-" * 30)
    institution_stats = institution_analysis(df)
    if institution_stats:
        print(f"最大机构: {institution_stats['最大机构']}")
        print(f"占比: {institution_stats['最大占比']:.1f}%")
        print(f"集中度风险: {institution_stats['集中度风险']}")
    
    # 趋势分析
    print("\n📈 趋势分析")
    print("-" * 30)
    trend_stats = daily_trend_analysis(df)
    if trend_stats:
        print(f"异常波动天数: {trend_stats['异常天数']}")
        print(f"最大日波动: {trend_stats['最大波动']:.1f}%")
        print(f"最小日波动: {trend_stats['最小波动']:.1f}%")
    
    print(f"\n{'='*60}")
    print("报告生成完成")
    print(f"{'='*60}\n")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python quick-analysis.py <数据文件路径>")
        print("支持格式: .xlsx, .xls, .csv")
        return
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"错误: 文件 {file_path} 不存在")
        return
    
    # 加载数据
    df = load_insurance_data(file_path)
    if df is None:
        return
    
    print(f"数据加载成功: {len(df)} 条记录")
    
    # 生成报告
    generate_quick_report(df, os.path.basename(file_path))

if __name__ == "__main__":
    main()