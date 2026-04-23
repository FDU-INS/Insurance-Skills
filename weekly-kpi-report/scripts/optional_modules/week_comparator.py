#!/usr/bin/env python3
"""
周环比对比分析器 - 可选模块
仅在用户同时提供当前周和上周数据时启用
"""
import json
import sys

def calculate_week_over_week_changes(current_kpi, previous_kpi):
    """
    计算周环比变化
    
    参数:
        current_kpi: 当前周 KPI 字典
        previous_kpi: 上周 KPI 字典
    
    返回:
        包含环比变化的字典
    """
    changes = {
        "对比周次": f"第 {current_kpi['周次']} 周 vs 第 {previous_kpi['周次']} 周",
        "业务规模变化": {},
        "盈利能力变化": {},
        "新能源车变化": {},
        "风险指标变化": {},
        "综合评估": []
    }
    
    # 1. 业务规模环比
    current_premium = current_kpi['业务规模']['总保费_万元']
    prev_premium = previous_kpi['业务规模']['总保费_万元']
    premium_change = (current_premium - prev_premium) / prev_premium * 100 if prev_premium > 0 else 0
    
    current_count = current_kpi['业务规模']['保单数量']
    prev_count = previous_kpi['业务规模']['保单数量']
    count_change = (current_count - prev_count) / prev_count * 100 if prev_count > 0 else 0
    
    changes['业务规模变化'] = {
        "保费环比": {
            "当前周": current_premium,
            "上周": prev_premium,
            "变化率": round(premium_change, 2),
            "变化额": round(current_premium - prev_premium, 2)
        },
        "保单数环比": {
            "当前周": current_count,
            "上周": prev_count,
            "变化率": round(count_change, 2),
            "变化数": current_count - prev_count
        }
    }
    
    # 2. 盈利能力环比
    current_ratio = current_kpi['盈利能力']['综合成本率']
    prev_ratio = previous_kpi['盈利能力']['综合成本率']
    ratio_change = current_ratio - prev_ratio
    
    changes['盈利能力变化'] = {
        "综合成本率环比": {
            "当前周": current_ratio,
            "上周": prev_ratio,
            "变化": round(ratio_change, 2),
            "趋势": "改善" if ratio_change < 0 else "恶化" if ratio_change > 0 else "持平"
        },
        "赔付率环比": {
            "当前周": current_kpi['盈利能力']['平均赔付率'],
            "上周": previous_kpi['盈利能力']['平均赔付率'],
            "变化": round(current_kpi['盈利能力']['平均赔付率'] - previous_kpi['盈利能力']['平均赔付率'], 2)
        }
    }
    
    # 3. 新能源车环比
    if '新能源车保费占比' in current_kpi['新能源车分析'] and '新能源车保费占比' in previous_kpi['新能源车分析']:
        current_nev_ratio = current_kpi['新能源车分析']['新能源车保费占比']
        prev_nev_ratio = previous_kpi['新能源车分析']['新能源车保费占比']
        
        changes['新能源车变化'] = {
            "保费占比环比": {
                "当前周": current_nev_ratio,
                "上周": prev_nev_ratio,
                "变化": round(current_nev_ratio - prev_nev_ratio, 2)
            },
            "保单数环比": {
                "当前周": current_kpi['新能源车分析']['新能源车保单数'],
                "上周": previous_kpi['新能源车分析']['新能源车保单数'],
                "变化数": current_kpi['新能源车分析']['新能源车保单数'] - previous_kpi['新能源车分析']['新能源车保单数']
            }
        }
    
    # 4. 风险指标环比
    current_freq = current_kpi['风险指标']['平均出险频度']
    prev_freq = previous_kpi['风险指标']['平均出险频度']
    
    changes['风险指标变化'] = {
        "出险频度环比": {
            "当前周": current_freq,
            "上周": prev_freq,
            "变化": round(current_freq - prev_freq, 2)
        },
        "案均赔款环比": {
            "当前周": current_kpi['风险指标']['案均赔款_元'],
            "上周": previous_kpi['风险指标']['案均赔款_元'],
            "变化": round(current_kpi['风险指标']['案均赔款_元'] - previous_kpi['风险指标']['案均赔款_元'], 2)
        }
    }
    
    # 5. 生成综合评估
    if premium_change > 5:
        changes['综合评估'].append(f"📈 保费收入环比增长 {premium_change:.1f}%，业务规模扩张明显")
    elif premium_change < -5:
        changes['综合评估'].append(f"📉 保费收入环比下降 {abs(premium_change):.1f}%，需关注业务量下滑")
    
    if ratio_change < -2:
        changes['综合评估'].append(f"✅ 综合成本率环比改善 {abs(ratio_change):.1f} 个百分点，盈利能力提升")
    elif ratio_change > 2:
        changes['综合评估'].append(f"⚠️ 综合成本率环比上升 {ratio_change:.1f} 个百分点，需关注成本控制")
    
    if not changes['综合评估']:
        changes['综合评估'].append("📊 本周业务环比变化平稳")
    
    return changes

def generate_comparison_slide_data(changes):
    """
    生成用于 PPT 的环比对比数据
    """
    return {
        "幻灯片标题": f"周环比分析 - {changes['对比周次']}",
        "关键变化": [
            f"保费收入：{changes['业务规模变化']['保费环比']['变化率']:+.1f}%",
            f"综合成本率：{changes['盈利能力变化']['综合成本率环比']['变化']:+.1f}pp ({changes['盈利能力变化']['综合成本率环比']['趋势']})",
            f"出险频度：{changes['风险指标变化']['出险频度环比']['变化']:+.1f}pp"
        ],
        "综合评估": changes['综合评估']
    }

def main():
    if len(sys.argv) < 3:
        print(json.dumps({
            "error": "请提供当前周和上周的 KPI 文件路径",
            "usage": "python week_comparator.py <current_week_kpi.json> <previous_week_kpi.json>"
        }, ensure_ascii=False))
        sys.exit(1)
    
    current_kpi_file = sys.argv[1]
    previous_kpi_file = sys.argv[2]
    
    try:
        # 加载两周的 KPI 数据
        with open(current_kpi_file, 'r', encoding='utf-8') as f:
            current_kpi = json.load(f)
        
        with open(previous_kpi_file, 'r', encoding='utf-8') as f:
            previous_kpi = json.load(f)
        
        # 计算环比变化
        changes = calculate_week_over_week_changes(current_kpi, previous_kpi)
        
        # 生成幻灯片数据
        slide_data = generate_comparison_slide_data(changes)
        
        # 保存环比分析结果
        output_path = f'/home/claude/insurance-weekly-board-report/week_comparison_{current_kpi["周次"]}_vs_{previous_kpi["周次"]}.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                "详细变化": changes,
                "幻灯片数据": slide_data
            }, f, ensure_ascii=False, indent=2)
        
        print(json.dumps({
            "status": "success",
            "comparison_file": output_path,
            "summary": changes,
            "slide_data": slide_data
        }, ensure_ascii=False, indent=2))
        
    except FileNotFoundError as e:
        print(json.dumps({"error": f"文件未找到: {str(e)}"}, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)

if __name__ == '__main__':
    main()
