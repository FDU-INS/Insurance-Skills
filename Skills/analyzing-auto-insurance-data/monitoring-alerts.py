#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
车险业务监控预警脚本
用于Claude Skill的自动化业务异常检测
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import sys
import os

class InsuranceMonitoringAlerts:
    """车险业务监控预警类"""
    
    def __init__(self):
        # 预警阈值设置
        self.VOLATILITY_THRESHOLD = 0.10  # 10%波动率
        self.WEEKEND_GROWTH_THRESHOLD = 10  # 周末增长10倍
        self.INSTITUTION_CONCENTRATION_THRESHOLD = 0.40  # 机构集中度40%
        self.SINGLE_DAY_DROP_THRESHOLD = 0.20  # 单日下降20%
    
    def check_daily_volatility(self, df):
        """检查日保费波动率预警"""
        alerts = []
        
        if '投保确认时间' not in df.columns or '总保费' not in df.columns:
            return alerts
        
        # 转换日期并按日汇总
        df['日期'] = pd.to_datetime(df['投保确认时间']).dt.date
        daily_premium = df.groupby('日期')['总保费'].sum().reset_index()
        daily_premium.columns = ['日期', '日保费']
        
        # 计算日环比变化
        daily_premium['保费变化'] = daily_premium['日保费'].pct_change()
        daily_premium['波动率'] = abs(daily_premium['保费变化'])
        
        # 筛选异常波动
        abnormal_days = daily_premium[daily_premium['波动率'] > self.VOLATILITY_THRESHOLD]
        
        for _, row in abnormal_days.iterrows():
            change_direction = "增长" if row['保费变化'] > 0 else "下降"
            severity = "高" if row['波动率'] > 0.20 else "中"
            
            alerts.append({
                'type': '日保费波动异常',
                'date': str(row['日期']),
                'premium': round(row['日保费'], 2),
                'change_rate': round(row['保费变化'] * 100, 1),
                'volatility_rate': round(row['波动率'] * 100, 1),
                'severity': severity,
                'description': f"{row['日期']}日保费{change_direction}{row['波动率']*100:.1f}%({row['保费变化']*100:.1f}%)，超过{self.VOLATILITY_THRESHOLD*100:.0f}%阈值"
            })
        
        return alerts
    
    def check_weekday_pattern(self, df):
        """检查工作日模式异常"""
        alerts = []
        
        if '投保确认时间' not in df.columns or '总保费' not in df.columns:
            return alerts
        
        # 添加星期信息
        df['日期'] = pd.to_datetime(df['投保确认时间'])
        df['星期'] = df['日期'].dt.day_name()
        df['周期'] = df['日期'].dt.strftime('%Y-%m-%d')
        
        # 按星期汇总
        weekday_premium = df.groupby(['星期', '周期'])['总保费'].sum().reset_index()
        
        # 计算各星期的平均值和波动
        weekday_avg = weekday_premium.groupby('星期')['总保费'].mean()
        weekday_std = weekday_premium.groupby('星期')['总保费'].std()
        
        # 检查每个星期的异常值
        for weekday in weekday_avg.index:
            weekday_data = weekday_premium[weekday_premium['星期'] == weekday]
            
            if len(weekday_data) < 2:
                continue
            
            mean_val = weekday_avg[weekday]
            std_val = weekday_std[weekday]
            
            # 识别偏离超过2个标准差的异常值
            abnormal_data = weekday_data[
                abs(weekday_data['总保费'] - mean_val) > 2 * std_val
            ]
            
            for _, row in abnormal_data.iterrows():
                deviation = (row['总保费'] - mean_val) / mean_val * 100
                severity = "高" if abs(deviation) > 50 else "中"
                
                alerts.append({
                    'type': '工作日模式异常',
                    'weekday': weekday,
                    'date': row['周期'],
                    'premium': round(row['总保费'], 2),
                    'avg_premium': round(mean_val, 2),
                    'deviation': round(deviation, 1),
                    'severity': severity,
                    'description': f"{weekday}({row['周期']})保费偏离平均值{deviation:.1f}%"
                })
        
        return alerts
    
    def check_weekend_surge(self, df):
        """检查周末业务激增"""
        alerts = []
        
        if '投保确认时间' not in df.columns or '总保费' not in df.columns:
            return alerts
        
        # 添加星期信息
        df['日期'] = pd.to_datetime(df['投保确认时间'])
        df['星期'] = df['日期'].dt.day_name()
        df['周期'] = df['日期'].dt.strftime('%Y-%m-%d')
        
        # 分离工作日和周末数据
        weekday_data = df[df['星期'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])]
        weekend_data = df[df['星期'].isin(['Saturday', 'Sunday'])]
        
        if len(weekday_data) == 0 or len(weekend_data) == 0:
            return alerts
        
        # 计算工作日平均保费
        weekday_avg = weekday_data.groupby('周期')['总保费'].sum().mean()
        
        # 检查周末数据
        weekend_daily = weekend_data.groupby(['星期', '周期'])['总保费'].sum().reset_index()
        
        for _, row in weekend_daily.iterrows():
            weekend_premium = row['总保费']
            growth_multiple = weekend_premium / weekday_avg if weekday_avg > 0 else 0
            
            if growth_multiple > self.WEEKEND_GROWTH_THRESHOLD:
                severity = "高" if growth_multiple > 15 else "中"
                
                alerts.append({
                    'type': '周末业务激增异常',
                    'weekday': row['星期'],
                    'date': row['周期'],
                    'weekend_premium': round(weekend_premium, 2),
                    'weekday_avg': round(weekday_avg, 2),
                    'growth_multiple': round(growth_multiple, 1),
                    'severity': severity,
                    'description': f"{row['星期']}({row['周期']})保费{weekend_premium:.0f}万，是工作日平均的{growth_multiple:.1f}倍"
                })
        
        return alerts
    
    def check_institution_concentration(self, df):
        """检查机构集中度过高"""
        alerts = []
        
        if '三级机构' not in df.columns:
            return alerts
        
        # 计算各机构业务占比
        institution_stats = df['三级机构'].value_counts()
        total_business = len(df)
        institution_percentages = (institution_stats / total_business * 100)
        
        # 检查最大机构占比
        max_institution = institution_stats.index[0]
        max_percentage = institution_percentages.iloc[0]
        max_count = institution_stats.iloc[0]
        
        if max_percentage > self.INSTITUTION_CONCENTRATION_THRESHOLD * 100:
            severity = "高" if max_percentage > 50 else "中"
            
            alerts.append({
                'type': '机构集中度过高风险',
                'institution': max_institution,
                'concentration_ratio': round(max_percentage, 1),
                'business_count': max_count,
                'severity': severity,
                'description': f"{max_institution}占比{max_percentage:.1f}%({max_count}笔)，超过{self.INSTITUTION_CONCENTRATION_THRESHOLD*100:.0f}%阈值"
            })
        
        return alerts
    
    def check_friday_decline(self, df):
        """检查周五业务下滑（特定日期模式）"""
        alerts = []
        
        if '投保确认时间' not in df.columns or '总保费' not in df.columns:
            return alerts
        
        # 转换日期
        df['日期'] = pd.to_datetime(df['投保确认时间'])
        df['星期'] = df['日期'].dt.day_name()
        df['周期'] = df['日期'].dt.strftime('%Y-%m-%d')
        
        # 筛选周五数据
        friday_data = df[df['星期'] == 'Friday'].groupby('周期')['总保费'].sum().reset_index()
        friday_data.columns = ['周期', '周五保费']
        
        # 计算相邻周五的变化
        friday_data['变化率'] = friday_data['周五保费'].pct_change()
        
        # 检查特定日期模式（如文档提到的3/14→3/21下降24%）
        significant_declines = friday_data[friday_data['变化率'] < -0.20]  # 下降超过20%
        
        for _, row in significant_declines.iterrows():
            alerts.append({
                'type': '周五业务大幅下滑',
                'date': row['周期'],
                'friday_premium': round(row['周五保费'], 2),
                'decline_rate': round(row['变化率'] * 100, 1),
                'severity': '高',
                'description': f"{row['周期']}周五保费下降{row['变化率']*100:.1f}%"
            })
        
        return alerts
    
    def check_monday_volatility(self, df):
        """检查周一波动巨大"""
        alerts = []
        
        if '投保确认时间' not in df.columns or '总保费' not in df.columns:
            return alerts
        
        # 转换日期
        df['日期'] = pd.to_datetime(df['投保确认时间'])
        df['星期'] = df['日期'].dt.day_name()
        df['周期'] = df['日期'].dt.strftime('%Y-%m-%d')
        
        # 筛选周一数据
        monday_data = df[df['星期'] == 'Monday'].groupby('周期')['总保费'].sum().reset_index()
        monday_data.columns = ['周期', '周一保费']
        
        # 计算连续周一的变化（如文档提到的318万→209万→274万）
        if len(monday_data) >= 3:
            for i in range(2, len(monday_data)):
                current = monday_data.iloc[i]['周一保费']
                previous = monday_data.iloc[i-1]['周一保费']
                two_weeks_ago = monday_data.iloc[i-2]['周一保费']
                
                # 计算波动率
                change1 = abs(current - previous) / previous
                change2 = abs(previous - two_weeks_ago) / two_weeks_ago
                
                if change1 > self.VOLATILITY_THRESHOLD and change2 > self.VOLATILITY_THRESHOLD:
                    alerts.append({
                        'type': '周一波动巨大',
                        'current_date': monday_data.iloc[i]['周期'],
                        'values': [round(two_weeks_ago, 2), round(previous, 2), round(current, 2)],
                        'volatility_rates': [round(change1*100, 1), round(change2*100, 1)],
                        'severity': '高',
                        'description': f"连续周一波动异常: {two_weeks_ago:.0f}万→{previous:.0f}万→{current:.0f}万"
                    })
        
        return alerts
    
    def generate_monitoring_report(self, df):
        """生成完整的监控报告"""
        report = {
            '监控时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '数据记录数': len(df),
            '监控规则版本': '1.0',
            '预警结果': {}
        }
        
        # 执行各项检查
        all_alerts = []
        
        # 1. 日保费波动检查
        all_alerts.extend(self.check_daily_volatility(df))
        
        # 2. 工作日模式检查
        all_alerts.extend(self.check_weekday_pattern(df))
        
        # 3. 周末激增检查
        all_alerts.extend(self.check_weekend_surge(df))
        
        # 4. 机构集中度检查
        all_alerts.extend(self.check_institution_concentration(df))
        
        # 5. 周五下滑检查
        all_alerts.extend(self.check_friday_decline(df))
        
        # 6. 周一波动检查
        all_alerts.extend(self.check_monday_volatility(df))
        
        # 按严重程度分类
        high_alerts = [alert for alert in all_alerts if alert.get('severity') == '高']
        medium_alerts = [alert for alert in all_alerts if alert.get('severity') == '中']
        info_alerts = [alert for alert in all_alerts if alert.get('severity') == '信息']
        
        report['预警结果'] = {
            '总计预警数量': len(all_alerts),
            '高优先级预警': len(high_alerts),
            '中优先级预警': len(medium_alerts),
            '信息类预警': len(info_alerts),
            '高优先级列表': high_alerts,
            '中优先级列表': medium_alerts,
            '所有预警列表': all_alerts
        }
        
        return report
    
    def print_monitoring_summary(self, report):
        """打印监控摘要"""
        print(f"\n{'='*80}")
        print("车险业务监控预警报告")
        print(f"监控时间: {report['监控时间']}")
        print(f"数据记录: {report['数据记录数']} 条")
        print(f"{'='*80}\n")
        
        results = report['预警结果']
        
        print(f"📊 预警统计")
        print(f"  总计预警: {results['总计预警数量']} 个")
        print(f"  🔴 高优先级: {results['高优先级预警']} 个")
        print(f"  🟡 中优先级: {results['中优先级预警']} 个")
        print(f"  🔵 信息类: {results['信息类预警']} 个")
        
        # 显示高优先级预警
        if results['高优先级预警'] > 0:
            print(f"\n🚨 高优先级预警详情:")
            for i, alert in enumerate(results['高优先级列表'], 1):
                print(f"  {i}. {alert['type']}: {alert['description']}")
        
        # 显示中优先级预警
        if results['中优先级预警'] > 0:
            print(f"\n⚠️ 中优先级预警详情:")
            for i, alert in enumerate(results['中优先级列表'], 1):
                print(f"  {i}. {alert['type']}: {alert['description']}")
        
        if results['总计预警数量'] == 0:
            print(f"\n✅ 未发现异常，业务运行正常")
        
        print(f"\n{'='*80}")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python monitoring-alerts.py <数据文件路径>")
        return
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"错误: 文件 {file_path} 不存在")
        return
    
    # 加载数据
    try:
        if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            df = pd.read_excel(file_path)
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path, encoding='utf-8')
        else:
            print("错误: 不支持的文件格式")
            return
    except Exception as e:
        print(f"数据加载失败: {e}")
        return
    
    print(f"数据加载成功: {len(df)} 条记录")
    
    # 运行监控
    monitor = InsuranceMonitoringAlerts()
    report = monitor.generate_monitoring_report(df)
    
    # 输出结果
    monitor.print_monitoring_summary(report)
    
    # 保存详细报告
    report_file = f"monitoring_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"详细报告已保存至: {report_file}")

if __name__ == "__main__":
    main()