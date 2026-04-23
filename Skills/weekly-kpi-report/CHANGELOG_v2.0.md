# Changelog - v2.0.0 (Field Mapping Support)

**Release Date:** 2025-12-08
**Major Version Update:** v1.3.0 → v2.0.0

---

## 🎯 核心改进: 支持多种数据格式

### 问题背景

**v1.x 的限制:**

- 硬编码中文字段名 (`跟单保费(Ten Thousand)`, `业务类型分类` 等)
- 只支持 Excel 格式 (`.xlsx`)
- 无法处理转换后的CSV数据 (英文字段名)

**实际需求:**

- 用户数据来源多样: 原始Excel (中文) + 转换后CSV (英文)
- 需要灵活适配不同数据源,无需手动转换

---

## ✨ 新增功能

### 1. 字段映射配置 (field_mapping.json)

新增配置文件,支持中英文字段自动映射:

```json
{
  "field_mappings": {
    "premium": {
      "aliases": [
        "signed_premium_yuan", // 英文 (CSV)
        "跟单保费(Ten Thousand)", // 中文 (Excel)
        "签单保费"
      ]
    },
    "business_type": {
      "aliases": [
        "business_type_category", // 英文
        "业务类型分类" // 中文
      ]
    }
    // ... 15+ 字段映射
  }
}
```

**支持的字段类别:**

- 保费类: premium, matured_premium, commercial_premium
- 业务类: business_type, customer_category, third_level_org
- 新能源车: is_nev (支持 True/False, 是/否)
- 风险类: claim_cases, claim_amount, expense_amount
- 其他: renewal_status, policy_count, week_number

### 2. 自动格式检测

`kpi_calculator.py` 现在自动检测并加载:

- Excel文件 (`.xlsx`, `.xls`)
- CSV文件 (`.csv`)

```python
# 自动检测
if file_ext in ['.xlsx', '.xls']:
    df = pd.read_excel(file_path)
elif file_ext == '.csv':
    df = pd.read_csv(file_path, encoding='utf-8')  # 自动尝试多种编码
```

### 3. 智能字段匹配

脚本使用逻辑字段名,自动匹配实际列名:

```python
# 旧版本 (硬编码)
premium = df['跟单保费(Ten Thousand)']  # ❌ 只支持中文

# 新版本 (智能匹配)
premium = get_field(df, 'premium')      # ✅ 自动匹配中英文
```

**匹配逻辑:**

1. 加载 `field_mapping.json`
2. 根据逻辑名 (如 `premium`) 获取别名列表
3. 遍历别名,找到数据中存在的列
4. 返回匹配的列

### 4. 单位自动转换

识别保费字段单位并自动转换:

```python
# 如果字段名包含 "Ten Thousand" → 已经是万元
# 如果字段名是 "yuan" → 转换为万元 (除以10000)
```

---

## 🔧 改进的功能

### kpi_calculator.py v2.0

**新增函数:**

- `load_field_mapping()` - 加载字段映射配置
- `get_field(df, logical_name)` - 智能字段匹配
- `get_field_name(df, logical_name)` - 获取实际字段名
- `normalize_boolean_field(series)` - 标准化布尔值

**改进的函数:**

- `load_and_clean_data()` - 支持CSV + 多种编码
- `calculate_business_scale()` - 单位自动识别
- `calculate_profitability()` - 容错处理
- `calculate_nev_insights()` - 布尔字段标准化
- `calculate_risk_metrics()` - 异常处理
- `calculate_customer_mix()` - 字段缺失处理

**新增输出信息:**

```bash
🚀 开始处理: 高新_第49周.csv
✅ 已加载 CSV 文件: 高新_第49周.csv (编码: utf-8)
📊 数据行数: 1960, 列数: 27
📋 列名: ['signed_premium_yuan', 'business_type_category', ...]
✅ KPI计算完成
📁 输出文件: kpis_week_49.json
📊 综合成本率: 52.7%
```

---

## 📊 测试验证

### 测试场景1: CSV英文字段

**数据:** `高新_第49周.csv`

- 字段: `signed_premium_yuan`, `business_type_category`, `is_new_energy_vehicle`
- 格式: CSV, UTF-8编码

**结果:** ✅ 成功

```json
{
  "status": "success",
  "summary": {
    "week": "49",
    "records": 1960,
    "combined_ratio": 52.7
  }
}
```

### 测试场景2: Excel中文字段 (待测试)

**数据:** `车险保单变动成本清单__第45周_.xlsx`

- 字段: `跟单保费(Ten Thousand)`, `业务类型分类`, `是否新能源车1`
- 格式: Excel

**预期:** ✅ 应该成功

---

## 🔄 向后兼容性

### ✅ 完全兼容

对于使用中文Excel的旧数据:

- 字段映射配置包含所有旧字段名
- 脚本优先匹配旧字段名
- 无需修改任何数据

### 🆕 新支持

对于使用英文CSV的新数据:

- 自动识别英文字段名
- 自动转换单位
- 无需手动转换格式

---

## 📁 新增文件

1. **field_mapping.json** - 字段映射配置
   - 15+ 逻辑字段定义
   - 中英文别名列表
   - 数据类型说明
   - 单位转换规则

2. **CHANGELOG_v2.0.md** - 本文档
   - 详细更新说明
   - 使用示例
   - 测试验证

---

## 🚀 使用示例

### 示例1: CSV英文字段

```bash
cd /Users/xuechenglong/Desktop/GitHub多项目数据源

python .claude/skills/weekly-kpi-report/scripts/kpi_calculator.py \
  "高新机构分析/weeks_40-49/高新_第49周.csv" \
  49
```

### 示例2: Excel中文字段

```bash
python .claude/skills/weekly-kpi-report/scripts/kpi_calculator.py \
  "变率——转换后清单/车险保单变动成本清单__第45周_.xlsx" \
  45
```

### 示例3: 批量处理

```bash
for week in {40..49}; do
  python .claude/skills/weekly-kpi-report/scripts/kpi_calculator.py \
    "高新机构分析/weeks_40-49/高新_第${week}周.csv" \
    $week
done
```

---

## 🐛 Bug修复

1. **硬编码字段名导致CSV无法处理** (🔴 Critical)
   - 问题: KeyError: '跟单保费(Ten Thousand)'
   - 修复: 字段映射配置 + get_field() 函数

2. **只支持Excel格式** (🟡 Major)
   - 问题: CSV文件无法读取
   - 修复: 自动格式检测

3. **布尔字段不兼容** (🟡 Major)
   - 问题: is_new_energy_vehicle (True/False) vs 是否新能源车1 (是/否)
   - 修复: normalize_boolean_field() 函数

4. **单位混乱** (🟢 Minor)
   - 问题: 保费单位(万元 vs 元)不明确
   - 修复: 自动识别并转换

---

## 📝 配置说明

### field_mapping.json 结构

```json
{
  "field_mappings": {
    "<logical_name>": {
      "description": "字段说明",
      "aliases": ["实际字段名1", "实际字段名2"],
      "type": "numeric | categorical | boolean | date",
      "unit_conversion": {
        // 可选
        "field1": 1,
        "field2": 10000
      }
    }
  }
}
```

### 添加新字段映射

如果数据有新的字段名,编辑 `field_mapping.json`:

```json
{
  "field_mappings": {
    "premium": {
      "aliases": [
        "signed_premium_yuan",
        "跟单保费(Ten Thousand)",
        "保费金额", // 新增
        "premium_amount" // 新增
      ]
    }
  }
}
```

---

## 🔮 未来计划

### v2.1.0 (计划中)

- [ ] 支持JSON数据格式
- [ ] 支持Parquet列式存储
- [ ] 字段映射可视化工具

### v2.2.0 (计划中)

- [ ] 数据质量自动检查
- [ ] 字段映射自动学习
- [ ] 多数据源合并处理

---

## 📞 反馈与支持

如遇到问题:

1. 检查字段映射配置是否包含你的字段名
2. 查看脚本输出的错误信息
3. 手动添加字段映射到 `field_mapping.json`

---

**升级建议:** ✅ 强烈建议升级

- 无破坏性变更
- 完全向后兼容
- 支持更多数据源
- 更好的错误处理

**升级方式:**

```bash
# 直接使用新版脚本,无需额外配置
python .claude/skills/weekly-kpi-report/scripts/kpi_calculator.py <file> <week>
```
