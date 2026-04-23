#!/usr/bin/env python3
"""
社保缴费计算器
支持：职工社保、灵活就业、居民社保
覆盖全国主要城市

作者：QQ 1817694478
微信扫码留言：assets/qr-wechat.png

用法示例：
  python social_security_calculator.py --city 北京 --salary 15000
  python social_security_calculator.py --city 上海 --type flex --base-rate 100
  python social_security_calculator.py --city 广州 --type resident --age 40
  python social_security_calculator.py --retirement --years 30 --avg-index 0.8 --city 北京
"""

import argparse
import sys

# ─────────────────────────────────────────
# 各城市社保参数数据库（2024年度）
# ─────────────────────────────────────────
CITY_DATA = {
    "北京": {
        "avg_wage": 11761,   # 月社平工资
        "base_low_ratio": 0.60,
        "base_high_ratio": 3.0,
        "pension_company": 0.16,
        "pension_personal": 0.08,
        "medical_company": 0.10,
        "medical_personal": 0.02,
        "medical_extra": 3,   # 大病统筹元/月
        "unemployment_company": 0.008,
        "unemployment_personal": 0.002,
        "maternity_company": 0.008,
        "injury_company": 0.004,  # 取中间值
        "flex_pension_rate": 0.20,
        "flex_medical_rate": 0.098,
    },
    "上海": {
        "avg_wage": 12183,
        "base_low_ratio": 0.60,
        "base_high_ratio": 3.0,
        "pension_company": 0.16,
        "pension_personal": 0.08,
        "medical_company": 0.10,
        "medical_personal": 0.02,
        "medical_extra": 0,
        "unemployment_company": 0.005,
        "unemployment_personal": 0.005,
        "maternity_company": 0.01,
        "injury_company": 0.004,
        "flex_pension_rate": 0.24,
        "flex_medical_rate": 0.115,
    },
    "广州": {
        "avg_wage": 9853,
        "base_low_ratio": 0.60,
        "base_high_ratio": 3.0,
        "pension_company": 0.14,
        "pension_personal": 0.08,
        "medical_company": 0.065,
        "medical_personal": 0.02,
        "medical_extra": 0,
        "unemployment_company": 0.007,
        "unemployment_personal": 0.003,
        "maternity_company": 0.005,
        "injury_company": 0.004,
        "flex_pension_rate": 0.20,
        "flex_medical_rate": 0.075,
    },
    "深圳": {
        "avg_wage": 9000,
        "base_low": 2360,
        "base_high": 23088,
        "pension_company": 0.14,
        "pension_personal": 0.08,
        "medical_company": 0.062,
        "medical_personal": 0.005,
        "medical_extra": 0,
        "unemployment_company": 0.007,
        "unemployment_personal": 0.003,
        "maternity_company": 0.0,
        "injury_company": 0.004,
        "flex_pension_rate": 0.20,
        "flex_medical_rate": 0.062,
    },
    "杭州": {
        "avg_wage": 10370,
        "base_low_ratio": 0.60,
        "base_high_ratio": 3.0,
        "pension_company": 0.14,
        "pension_personal": 0.08,
        "medical_company": 0.095,
        "medical_personal": 0.02,
        "medical_extra": 3,
        "unemployment_company": 0.005,
        "unemployment_personal": 0.005,
        "maternity_company": 0.008,
        "injury_company": 0.004,
        "flex_pension_rate": 0.20,
        "flex_medical_rate": 0.095,
    },
    "南京": {
        "avg_wage": 8972,
        "base_low_ratio": 0.60,
        "base_high_ratio": 3.0,
        "pension_company": 0.16,
        "pension_personal": 0.08,
        "medical_company": 0.09,
        "medical_personal": 0.02,
        "medical_extra": 0,
        "unemployment_company": 0.005,
        "unemployment_personal": 0.005,
        "maternity_company": 0.006,
        "injury_company": 0.004,
        "flex_pension_rate": 0.20,
        "flex_medical_rate": 0.09,
    },
    "成都": {
        "avg_wage": 7707,
        "base_low_ratio": 0.60,
        "base_high_ratio": 3.0,
        "pension_company": 0.16,
        "pension_personal": 0.08,
        "medical_company": 0.085,
        "medical_personal": 0.02,
        "medical_extra": 0,
        "unemployment_company": 0.005,
        "unemployment_personal": 0.005,
        "maternity_company": 0.007,
        "injury_company": 0.004,
        "flex_pension_rate": 0.20,
        "flex_medical_rate": 0.085,
    },
    "武汉": {
        "avg_wage": 7057,
        "base_low_ratio": 0.60,
        "base_high_ratio": 3.0,
        "pension_company": 0.16,
        "pension_personal": 0.08,
        "medical_company": 0.08,
        "medical_personal": 0.02,
        "medical_extra": 3,
        "unemployment_company": 0.005,
        "unemployment_personal": 0.005,
        "maternity_company": 0.005,
        "injury_company": 0.004,
        "flex_pension_rate": 0.20,
        "flex_medical_rate": 0.08,
    },
    "西安": {
        "avg_wage": 6856,
        "base_low_ratio": 0.60,
        "base_high_ratio": 3.0,
        "pension_company": 0.16,
        "pension_personal": 0.08,
        "medical_company": 0.065,
        "medical_personal": 0.02,
        "medical_extra": 0,
        "unemployment_company": 0.005,
        "unemployment_personal": 0.005,
        "maternity_company": 0.005,
        "injury_company": 0.004,
        "flex_pension_rate": 0.20,
        "flex_medical_rate": 0.065,
    },
    "长沙": {
        "avg_wage": 7248,
        "base_low_ratio": 0.60,
        "base_high_ratio": 3.0,
        "pension_company": 0.16,
        "pension_personal": 0.08,
        "medical_company": 0.08,
        "medical_personal": 0.02,
        "medical_extra": 0,
        "unemployment_company": 0.005,
        "unemployment_personal": 0.005,
        "maternity_company": 0.005,
        "injury_company": 0.004,
        "flex_pension_rate": 0.20,
        "flex_medical_rate": 0.08,
    },
    "郑州": {
        "avg_wage": 6431,
        "base_low_ratio": 0.60,
        "base_high_ratio": 3.0,
        "pension_company": 0.16,
        "pension_personal": 0.08,
        "medical_company": 0.07,
        "medical_personal": 0.02,
        "medical_extra": 0,
        "unemployment_company": 0.005,
        "unemployment_personal": 0.005,
        "maternity_company": 0.005,
        "injury_company": 0.004,
        "flex_pension_rate": 0.20,
        "flex_medical_rate": 0.07,
    },
    "济南": {
        "avg_wage": 7137,
        "base_low_ratio": 0.60,
        "base_high_ratio": 3.0,
        "pension_company": 0.16,
        "pension_personal": 0.08,
        "medical_company": 0.09,
        "medical_personal": 0.02,
        "medical_extra": 0,
        "unemployment_company": 0.005,
        "unemployment_personal": 0.005,
        "maternity_company": 0.005,
        "injury_company": 0.004,
        "flex_pension_rate": 0.20,
        "flex_medical_rate": 0.09,
    },
    "重庆": {
        "avg_wage": 6911,
        "base_low_ratio": 0.60,
        "base_high_ratio": 3.0,
        "pension_company": 0.16,
        "pension_personal": 0.08,
        "medical_company": 0.08,
        "medical_personal": 0.02,
        "medical_extra": 0,
        "unemployment_company": 0.005,
        "unemployment_personal": 0.005,
        "maternity_company": 0.005,
        "injury_company": 0.004,
        "flex_pension_rate": 0.20,
        "flex_medical_rate": 0.08,
    },
    "天津": {
        "avg_wage": 9631,
        "base_low_ratio": 0.60,
        "base_high_ratio": 3.0,
        "pension_company": 0.16,
        "pension_personal": 0.08,
        "medical_company": 0.10,
        "medical_personal": 0.02,
        "medical_extra": 3,
        "unemployment_company": 0.005,
        "unemployment_personal": 0.005,
        "maternity_company": 0.005,
        "injury_company": 0.004,
        "flex_pension_rate": 0.20,
        "flex_medical_rate": 0.10,
    },
    "厦门": {
        "avg_wage": 10610,
        "base_low_ratio": 0.60,
        "base_high_ratio": 3.0,
        "pension_company": 0.14,
        "pension_personal": 0.08,
        "medical_company": 0.08,
        "medical_personal": 0.02,
        "medical_extra": 0,
        "unemployment_company": 0.005,
        "unemployment_personal": 0.005,
        "maternity_company": 0.004,
        "injury_company": 0.004,
        "flex_pension_rate": 0.20,
        "flex_medical_rate": 0.08,
    },
}

# 计发月数（按退休年龄）
PAYMENT_MONTHS = {
    50: 195, 51: 190, 52: 185, 53: 180, 54: 175,
    55: 170, 56: 164, 57: 158, 58: 152, 59: 145,
    60: 139, 61: 132, 62: 125, 63: 116, 64: 107, 65: 101,
}


def get_base(city_info: dict, salary: float) -> dict:
    """计算缴费基数（上下限约束）"""
    avg = city_info["avg_wage"]
    if "base_low" in city_info:
        low = city_info["base_low"]
        high = city_info["base_high"]
    else:
        low = avg * city_info["base_low_ratio"]
        high = avg * city_info["base_high_ratio"]
    base = max(low, min(salary, high))
    return {"base": round(base, 2), "low": round(low, 2), "high": round(high, 2)}


def calc_employee(city: str, salary: float) -> None:
    """计算职工社保缴费"""
    if city not in CITY_DATA:
        print(f"❌ 暂不支持 {city}，已支持城市：{', '.join(CITY_DATA.keys())}")
        return

    c = CITY_DATA[city]
    b_info = get_base(c, salary)
    base = b_info["base"]

    pension_p = base * c["pension_personal"]
    medical_p = base * c["medical_personal"] + c.get("medical_extra", 0)
    unemployment_p = base * c["unemployment_personal"]
    total_personal = pension_p + medical_p + unemployment_p

    pension_c = base * c["pension_company"]
    medical_c = base * c["medical_company"]
    unemployment_c = base * c["unemployment_company"]
    maternity_c = base * c.get("maternity_company", 0)
    injury_c = base * c.get("injury_company", 0)
    total_company = pension_c + medical_c + unemployment_c + maternity_c + injury_c

    print(f"\n{'='*55}")
    print(f"  [{city}] 职工社保月缴费计算（2024年度）")
    print(f"{'='*55}")
    print(f"  本人月工资：       {salary:>10,.0f} 元")
    print(f"  缴费基数：         {base:>10,.2f} 元（下限 {b_info['low']:,.0f} / 上限 {b_info['high']:,.0f}）")
    print(f"  {'-'*50}")
    print(f"  【个人缴纳部分】")
    print(f"    养老保险（{c['pension_personal']*100:.0f}%）：  {pension_p:>8,.2f} 元")
    print(f"    医疗保险（{c['medical_personal']*100:.0f}%+{c.get('medical_extra',0)}元）：{medical_p:>6,.2f} 元")
    print(f"    失业保险（{c['unemployment_personal']*100:.1f}%）：{unemployment_p:>7,.2f} 元")
    print(f"    {'-'*42}")
    print(f"    个人合计：         {total_personal:>8,.2f} 元/月")
    print(f"  {'-'*50}")
    print(f"  【单位缴纳部分】")
    print(f"    养老保险（{c['pension_company']*100:.0f}%）：  {pension_c:>8,.2f} 元")
    print(f"    医疗保险（{c['medical_company']*100:.1f}%）：{medical_c:>8,.2f} 元")
    print(f"    失业保险（{c['unemployment_company']*100:.1f}%）：{unemployment_c:>7,.2f} 元")
    print(f"    生育保险（{c.get('maternity_company',0)*100:.1f}%）：{maternity_c:>7,.2f} 元")
    print(f"    工伤保险（{c.get('injury_company',0)*100:.1f}%）：{injury_c:>7,.2f} 元")
    print(f"    {'-'*42}")
    print(f"    单位合计：         {total_company:>8,.2f} 元/月")
    print(f"  {'-'*50}")
    print(f"  用工总成本：        {salary + total_company:>8,.2f} 元/月")
    print(f"  税前到手（扣前）：  {salary - total_personal:>8,.2f} 元/月")
    print(f"{'='*55}\n")


def calc_flexible(city: str, base_rate: int = 60) -> None:
    """计算灵活就业人员社保缴费"""
    if city not in CITY_DATA:
        print(f"❌ 暂不支持 {city}")
        return

    c = CITY_DATA[city]
    avg = c["avg_wage"]
    base = avg * (base_rate / 100)
    if "base_low" in c:
        base = max(c["base_low"], min(base, c["base_high"]))
    else:
        base = max(avg * c["base_low_ratio"], min(base, avg * c["base_high_ratio"]))
    base = round(base, 2)

    pension = base * c["flex_pension_rate"]
    medical = base * c["flex_medical_rate"]
    total = pension + medical

    print(f"\n{'='*55}")
    print(f"  [{city}] 灵活就业社保月缴费（2024年度）")
    print(f"{'='*55}")
    print(f"  当地月社平工资：   {avg:>10,} 元")
    print(f"  选择缴费档位：     {base_rate}%")
    print(f"  实际缴费基数：     {base:>10,.2f} 元")
    print(f"  {'-'*50}")
    print(f"  养老保险（{c['flex_pension_rate']*100:.0f}%）：     {pension:>8,.2f} 元/月")
    print(f"  医疗保险（{c['flex_medical_rate']*100:.1f}%）：    {medical:>8,.2f} 元/月")
    print(f"  {'-'*50}")
    print(f"  月缴费合计：        {total:>8,.2f} 元/月")
    print(f"  年缴费合计：        {total*12:>8,.2f} 元/年")
    print(f"{'='*55}")
    print(f"\n  不同档位对比：")
    print(f"  {'档位':>6}  {'缴费基数':>10}  {'养老':>8}  {'医疗':>8}  {'月合计':>8}")
    print(f"  {'-'*50}")
    for rate in [60, 80, 100, 150, 200, 300]:
        b = avg * (rate / 100)
        if "base_low" in c:
            b = max(c["base_low"], min(b, c["base_high"]))
        else:
            b = max(avg * c["base_low_ratio"], min(b, avg * c["base_high_ratio"]))
        p = b * c["flex_pension_rate"]
        m = b * c["flex_medical_rate"]
        mark = " <--" if rate == base_rate else ""
        print(f"  {rate:>5}%  {b:>10,.0f}  {p:>8,.0f}  {m:>8,.0f}  {p+m:>8,.0f}{mark}")
    print()


def calc_retirement(city: str, years: int, avg_index: float,
                    retire_age: int = 60, personal_account: float = None) -> None:
    """估算退休养老金"""
    if city not in CITY_DATA:
        print(f"❌ 暂不支持 {city}")
        return

    avg_wage = CITY_DATA[city]["avg_wage"]

    # 基础养老金
    indexed_wage = avg_wage * avg_index
    basic_pension = (avg_wage + indexed_wage) / 2 * years * 0.01

    # 个人账户养老金
    if personal_account is None:
        # 估算：假设平均工资 × 平均指数 × 8% × 12 × years
        personal_account = avg_wage * avg_index * 0.08 * 12 * years

    months = PAYMENT_MONTHS.get(retire_age, 139)
    account_pension = personal_account / months

    total = basic_pension + account_pension
    replacement = total / (avg_wage * avg_index) * 100

    print(f"\n{'='*55}")
    print(f"  [{city}] 养老金待遇估算")
    print(f"{'='*55}")
    print(f"  当地月社平工资：   {avg_wage:>10,} 元（2024年参考）")
    print(f"  累计缴费年限：     {years:>10} 年")
    print(f"  平均缴费指数：     {avg_index:>10.2f}（如60%基数=0.6，100%基数=1.0）")
    print(f"  退休年龄：         {retire_age:>10} 岁")
    print(f"  个人账户余额（估）：{personal_account:>8,.0f} 元")
    print(f"  计发月数：         {months:>10} 个月")
    print(f"  {'-'*50}")
    print(f"  基础养老金：       {basic_pension:>8,.0f} 元/月")
    print(f"  个人账户养老金：   {account_pension:>8,.0f} 元/月")
    print(f"  {'-'*50}")
    print(f"  月养老金合计：     {total:>8,.0f} 元/月")
    print(f"  替代率（对比社平）：{replacement:.1f}%")
    print(f"{'='*55}")
    print(f"\n  不同缴费年限对比（平均指数 {avg_index}，退休年龄{retire_age}岁）：")
    print(f"  {'年限':>6}  {'基础养老金':>10}  {'个账养老金':>10}  {'月合计':>8}")
    print(f"  {'-'*46}")
    for y in [15, 20, 25, 30, 35, 40]:
        bp = (avg_wage + avg_wage * avg_index) / 2 * y * 0.01
        pa = avg_wage * avg_index * 0.08 * 12 * y
        ap = pa / months
        mark = " <--" if y == years else ""
        print(f"  {y:>5}年  {bp:>10,.0f}  {ap:>10,.0f}  {bp+ap:>8,.0f}{mark}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="社保缴费与待遇计算器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例：
  职工社保：  python social_security_calculator.py --city 北京 --salary 15000
  灵活就业：  python social_security_calculator.py --city 上海 --type flex --base-rate 80
  养老估算：  python social_security_calculator.py --retirement --city 成都 --years 30 --avg-index 0.9
  支持城市：  python social_security_calculator.py --list-cities
        """
    )
    parser.add_argument("--city", type=str, default="北京", help="城市名称（如：北京、上海、广州）")
    parser.add_argument("--salary", type=float, help="月工资（元）")
    parser.add_argument("--type", choices=["employee", "flex", "resident"],
                        default="employee", help="参保类型：employee=职工 flex=灵活就业 resident=居民")
    parser.add_argument("--base-rate", type=int, default=60,
                        help="灵活就业缴费档位（%），如 60/80/100/200")
    parser.add_argument("--retirement", action="store_true", help="养老金待遇测算模式")
    parser.add_argument("--years", type=int, default=30, help="累计缴费年限")
    parser.add_argument("--avg-index", type=float, default=1.0, help="平均缴费指数（0.6~3.0）")
    parser.add_argument("--retire-age", type=int, default=60, help="退休年龄")
    parser.add_argument("--personal-account", type=float, help="个人账户实际余额（元）")
    parser.add_argument("--list-cities", action="store_true", help="列出所有支持的城市")

    args = parser.parse_args()

    if args.list_cities:
        print("\n支持的城市列表：")
        for city in CITY_DATA.keys():
            c = CITY_DATA[city]
            print(f"  {city}  社平工资：{c['avg_wage']:,} 元/月")
        print()
        return

    if args.retirement:
        calc_retirement(
            city=args.city,
            years=args.years,
            avg_index=args.avg_index,
            retire_age=args.retire_age,
            personal_account=args.personal_account
        )
    elif args.type == "flex":
        calc_flexible(city=args.city, base_rate=args.base_rate)
    else:
        if args.salary is None:
            print("❌ 职工社保计算需提供 --salary 参数")
            parser.print_help()
            sys.exit(1)
        calc_employee(city=args.city, salary=args.salary)


if __name__ == "__main__":
    main()
