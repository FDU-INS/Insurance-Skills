import os

cases_dir = r'C:\Users\庄赫\WorkBuddy\20260416100718\cases'

products = []
for root, dirs, files in os.walk(cases_dir):
    md_files = [f for f in files if f.endswith('.md')]
    if not md_files:
        continue
    rel_root = os.path.relpath(root, cases_dir)
    if rel_root == '.':
        continue

    clause_files = sorted([f for f in md_files if '条款' in f])
    rate_files = sorted([f for f in md_files if ('费率表' in f or f.endswith('费率.md'))])
    report_files = sorted([f for f in md_files if '可行性研究报告' in f or '可研' in f])
    strategy_files = sorted([f for f in md_files if '风险策略' in f or '承保风险' in f])
    other_files = sorted([f for f in md_files if f not in clause_files + rate_files + report_files + strategy_files])

    products.append({
        'category': rel_root,
        'clause_files': clause_files,
        'rate_files': rate_files,
        'report_files': report_files,
        'strategy_files': strategy_files,
        'other_files': other_files,
        'is_addon': '附加' in rel_root,
    })

# 产品险种大类分类体系（基于产品编号.xlsx + 用户调整规则）
# 共12个险类：企财险/货运险/责任险/保证险/意外险/健康险/家财险/工程险/船舶险/信用险/特殊风险/其他
# 分类优先级：特殊风险 > 货运险 > 责任险 > 保证险 > 意外险 > 健康险 > 家财险 > 企财险 > 工程险 > 船舶险 > 信用险 > 其他
def classify(cat):
    # 1. 特殊风险（无人机、机器人、特种设备）
    if any(kw in cat for kw in ['无人机机身', '无人机一切险', '无人机损失', '机器人保险', '具身智能', '特种设备', '航空航天']):
        return '特殊风险'
    
    # 2. 货运险（货物运输类）
    if any(kw in cat for kw in ['货物运输', '陆上运输', '无人机货物运输', '无人机货运', '海洋运输', '航空运输', '水路运输']):
        return '货运险'
    
    # 3. 责任险（法律责任类：包括知识产权侵权责任、产品责任、首台套/首版次的产品质量责任、临床试验责任、雇主责任附加险）
    if any(kw in cat for kw in [
        '责任保险', '执业责任', '产品责任', '产品质量责任', '公众责任', '雇主责任', 
        '电梯责任', '食品安全', '医疗机构', '环境污染', '安全生产', '医疗责任', 
        '校园责任', '食责险', '侵犯专利', '知识产权责任', '知识产权维权', '知识产权交易',
        '首台套', '首台（套）', '首版次', '重大技术装备', '临床试验责任', '药物临床试验责任',
        '附加自动承保新员工', '附加就餐时间', '附加伤残等级赔偿比例', '附加不记名投保'
    ]):
        return '责任险'
    
    # 4. 保证险
    if any(kw in cat for kw in ['保证保险', '履约保证', '投标保证', '预付款保证', '贷款保证', '信用保证', '保证金保险']):
        return '保证险'
    
    # 5. 意外险（人身意外伤害）
    if any(kw in cat for kw in [
        '意外伤害', '团体人身', '航空意外', '公共交通', '旅行意外', '借款人意外', 
        '意外住院', '意外妊娠', '猝死保险', '附加传染病', '附加急性病', '附加救护车', 
        '借款人人身意外', '建设工程施工人员团体意外'
    ]):
        return '意外险'
    
    # 6. 健康险（附加疾病身故、附加住院津贴）
    if any(kw in cat for kw in ['团体医疗', '团体重大疾病', '住院医疗', '健康保险', '药物临床', '医疗器械', '体检机构', '附加疾病身故', '附加住院津贴']):
        return '健康险'
    
    # 7. 家财险（机票取消、航班延误属于家财）
    if any(kw in cat for kw in ['家庭财产', '家庭财产险', '住房保险', '机票取消', '航班延误']):
        return '家财险'
    
    # 8. 企财险（屏幕意外、专利执行险及附加险、流片损失、费用补偿保险属于企财）
    if any(kw in cat for kw in [
        '企业财产', '财产险', '机器损坏', '营业中断', '屏幕意外', '数码产品意外',
        '专利执行', '专利侵权成立', '专利侵权损失', '专利权无效宣告', '专利权评价报告', '指定法律服务机构',
        '流片', '数据安全', '网络虚拟', '著作权侵权', '数据知识产权',
        '概念验证', '创业项目失败', '教育培训机构'
    ]):
        return '企财险'
    
    # 9. 工程险
    if any(kw in cat for kw in ['建筑工程', '安装工程', '工程保险', '工程险', '建筑工程一切险', '安装工程一切险']):
        return '工程险'
    
    # 10. 船舶险
    if any(kw in cat for kw in ['船舶保险', '船舶险', '船体险']):
        return '船舶险'
    
    # 11. 信用险
    if any(kw in cat for kw in ['信用保险', '短期出口信用', '中长期出口信用', '国内贸易信用']):
        return '信用险'
    
    # 12. 其他（费用补偿类：专利申请费用补偿等）
    return '其他'

grouped = {}
for p in products:
    g = classify(p['category'])
    if g not in grouped:
        grouped[g] = []
    grouped[g].append(p)

lines = []
lines.append('# 非车险产品案例库 — 统一检索索引')
lines.append('')
lines.append('| 项目 | 数值 |')
lines.append('|------|------|')
lines.append('| 产品总数 | %d |' % len(products))
lines.append('| 条款文件 | %d |' % sum(len(p['clause_files']) for p in products))
lines.append('| 费率表文件 | %d |' % sum(len(p['rate_files']) for p in products))
lines.append('| 可研报告 | %d |' % sum(len(p['report_files']) for p in products))
lines.append('| 风险策略 | %d |' % sum(len(p['strategy_files']) for p in products))
lines.append('')
lines.append('> **更新时间**: 2026-04-16  **版本**: v2.0 整理版')
lines.append('')
lines.append('---')
lines.append('')
lines.append('## 文档层级说明')
lines.append('')
lines.append('| 层级 | 类型 | 说明 |')
lines.append('|------|------|------|')
lines.append('| 主险 | 独立投保的保险产品 | 条款为主险主条款 |')
lines.append('| 附加险 | 依附主险，须与主险同时投保 | 通常名称含"附加" |')
lines.append('| 费率表 | 保费计算依据 | 主险/附加险均可能有 |')
lines.append('| 可研报告 | 完整产品开发文档 | 含背景/风险/条款/费率 |')
lines.append('| 风险策略 | 核保指引文件 | 承保风险管控策略 |')
lines.append('')
lines.append('---')

for group in ['企财险','货运险','责任险','保证险','意外险','健康险','家财险','工程险','船舶险','信用险','特殊风险','其他']:
    prods = grouped.get(group, [])
    if not prods:
        continue

    main = sorted([x for x in prods if not x['is_addon']], key=lambda x: x['category'])
    addon = sorted([x for x in prods if x['is_addon']], key=lambda x: x['category'])

    lines.append('')
    lines.append('## ' + group)
    lines.append('')
    lines.append('> 主险 %d 个，附加险 %d 个' % (len(main), len(addon)))
    lines.append('')

    if main:
        lines.append('### 主险产品')
        lines.append('')
        lines.append('| # | 产品名称 | 条款 | 费率表 | 可研 | 风险策略 |')
        lines.append('|---|---------|------|-------|------|---------|')
        for i, p in enumerate(main, 1):
            cat = p['category']
            clause_count = len(p['clause_files'])
            rate_count = len(p['rate_files'])
            has_report = '有' if p['report_files'] else '—'
            has_strategy = '有' if p['strategy_files'] else '—'
            lines.append('| %d | %s | %s×%d | %s×%d | %s | %s |' % (
                i, cat,
                '有' if clause_count else '—', clause_count,
                '有' if rate_count else '—', rate_count,
                has_report, has_strategy
            ))
        lines.append('')
        lines.append('**文件详情**')
        lines.append('')
        for p in main:
            lines.append('**' + p['category'] + '**')
            if p['clause_files']:
                lines.append('  - 条款: ' + ' / '.join(p['clause_files']))
            if p['rate_files']:
                lines.append('  - 费率表: ' + ' / '.join(p['rate_files']))
            if p['report_files']:
                lines.append('  - 可研报告: ' + ' / '.join(p['report_files']))
            if p['strategy_files']:
                lines.append('  - 风险策略: ' + ' / '.join(p['strategy_files']))
            lines.append('')

    if addon:
        lines.append('### 附加险产品')
        lines.append('')
        lines.append('| # | 附加险名称 | 条款 | 费率表 |')
        lines.append('|---|---------|------|-------|')
        for i, p in enumerate(addon, 1):
            lines.append('| %d | %s | %s×%d | %s×%d |' % (
                i, p['category'],
                '有' if p['clause_files'] else '—', len(p['clause_files']),
                '有' if p['rate_files'] else '—', len(p['rate_files'])
            ))
        lines.append('')
        lines.append('**文件详情**')
        lines.append('')
        for p in addon:
            lines.append('**' + p['category'] + '**')
            if p['clause_files']:
                lines.append('  - 条款: ' + ' / '.join(p['clause_files']))
            if p['rate_files']:
                lines.append('  - 费率表: ' + ' / '.join(p['rate_files']))
            lines.append('')

    lines.append('---')

lines.append('')
lines.append('## 深度案例索引')
lines.append('')
lines.append('以下产品具有完整文档，可直接用于产品开发参考：')
lines.append('')
lines.append('| # | 产品 | 公司 | 文档完整性 |')
lines.append('|---|------|------|-----------|')
deep_cases = [
    ('太平科技保险股份有限公司无人机机身一切险及第三者责任保险', '太平科技保险', '条款 + 费率表 + 可研报告 + 风险策略'),
    ('技术成果竞买履约保证保险', '太平科技保险', '条款 + 费率表 + 2x风险策略'),
    ('知识产权维权费用及侵权责任保险', '太平科技保险', '条款(中+英) + 费率表'),
    ('科技项目研发失败费用损失保险', '太平科技保险', '条款 + 费率表 + 风险策略'),
    ('专精特新企业综合保险', '太平科技保险', '条款 + 费率表'),
    ('首台（套）重大技术装备保险（中央型，示范条款）', '多家', '条款 + 费率表'),
    ('具身智能机器人保险（紫金/苏州东吴）', '紫金/苏州东吴', '条款 + 费率表'),
    ('无人机货物运输保险（太平洋/人保）', '太平洋/人保', '主险条款 + 附加险条款 + 费率表'),
]
for i, (name, company, docs) in enumerate(deep_cases, 1):
    lines.append('| %d | %s | %s | %s |' % (i, name, company, docs))

content = '\n'.join(lines)
idx_path = os.path.join(cases_dir, 'product_index.md')
with open(idx_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Done! %d lines written' % len(lines))
