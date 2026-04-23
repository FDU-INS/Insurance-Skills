# 非车险产品开发技能 (Non-Motor Insurance Product Development Skill)

> 🛡️ 面向 AI Agent 的非车险产品开发全流程知识库与工具集

[![Skill](https://img.shields.io/badge/WorkBuddy_Skill-🛡️-blue)](https://github.com/your-org/non-motor-insurance-product-dev)
[![Coverage](https://img.shields.io/badge/险种覆盖-30%2B-green)](#)
[![Cases](https://img.shields.io/badge/真实案例-6-orange)](#)

## 📖 简介

本技能是面向 AI Agent（如 WorkBuddy、Claude Code、Cursor 等）的非车险产品开发知识库。覆盖从保险标的识别、责任设计、可行性报告撰写、条款编制、费率定价到 Word 文档输出的**完整 7 步开发流程**。

### 适用范围

**传统非车险**：
- 财产保险（企业财产险、机器损坏险、营业中断险）
- 责任保险（公众责任险、产品责任险、雇主责任险、职业责任险）
- 工程保险（建工险、安工险）
- 信用保证保险

**新兴领域保险**：
- 🌐 网络安全保险
- 🌿 绿色保险（碳汇保险、清洁能源保险、环境污染责任险）
- 🚁 低空经济保险（无人机机身险、第三者责任险、eVTOL运营险）
- 💡 知识产权保险（专利执行险、专利被侵权损失险）
- 🔬 科技保险（科技成果转化险、中试费用损失险、科研仪器共享险）
- 💊 生物医药保险
- 📊 数据资产保险

## 📂 目录结构

```
non-motor-insurance-product-dev/
├── SKILL.md                          # 技能定义文件（入口）
├── references/                       # 核心知识库
│   ├── insurance_products.md         # 产品类型体系（30+险种）
│   ├── underwriting_rules.md         # 核保规则与风险评估
│   ├── regulations.md                # 监管政策与合规要求
│   ├── pricing_models.md             # 定价模型与精算方法
│   ├── development_checklist.md      # 产品开发检查清单（7步骤）
│   └── major_insurers_clauses_index.md  # 四大财险公司条款索引
├── templates/                        # 文档模板
│   ├── product_proposal_template.md  # 产品方案模板（12板块）
│   └── underwriting_checklist.md     # 核保检查清单（50+项）
├── cases/                            # 案例库
│   ├── cases_index.md                # 案例总索引
│   ├── typical_products.md           # 典型产品案例（10个）
│   └── 太平科技保险×6产品/            # 真实产品模板
├── scripts/                          # 自动化脚本
│   ├── step1_insured_subject.py
│   ├── step2_policyholder.py
│   ├── step3_coverage.py
│   ├── step4_feasibility_report.py
│   ├── step5_policy_clause.py
│   ├── step6_pricing.py
│   └── step7_word_export.py
└── data_interfaces/                  # 外部数据接口
    ├── industry_data_api.py
    ├── credit_rating_api.py
    └── disaster_risk_api.py
```

## 🚀 使用方式

### 在 WorkBuddy 中安装

将本目录放置到 WorkBuddy 技能目录下：
```bash
# 用户级技能
~/.workbuddy/skills/non-motor-insurance-product-dev/

# 或项目级技能
<workspace>/.workbuddy/skills/non-motor-insurance-product-dev/
```

### 触发词

以下关键词会自动触发本技能：

```
保险产品开发、非车险开发、保险条款、保险定价、费率表、保险标的、
核保规则、可行性报告、保险责任、责任免除、保险产品设计、产品开发流程、
网络安全保险、绿色保险、碳汇保险、低空经济、无人机保险、eVTOL、
知识产权保险、专利保险、数据资产保险、科技保险、中试保险、
生物医药保险、信用保证险
```

### 开发流程

```
步骤1: 确定保险标的 → 步骤2: 明确投被保人 → 步骤3: 保险责任设计
       ↓                                              ↓
步骤4: 可行性报告 ← ──────────────────────────────────┘
       ↓
步骤5: 条款撰写 → 步骤6: 产品定价 → 步骤7: Word输出
```

## 📋 核心知识亮点

| 知识点 | 内容 |
|--------|------|
| **监管三段式** | 金发〔2025〕36号 + 银保监会令2021年第10号 + 保监发〔2016〕115号 |
| **可研报告8章节** | 标准化结构，从监管依据到总体结论 |
| **条款13章节** | 行业标准条款模板，通用条款可直接引用 |
| **除外责任矩阵** | 8种险种×12种除外项交叉表 |
| **风险因子体系** | 财产险/责任险/科技险/网络安全险/绿色保险 5套因子 |
| **行业费率参考** | 财产险/责任险/科技保险/信保证险 4类基准费率 |
| **448个附加险** | 行业协会财产险151 + 公众责任险117 + 工程险180 |
| **6个真实案例** | 太平科技保险存量产品，条款 |

## 📊 案例库

基于太平科技保险真实产品模板：

| # | 产品 | 类型 | 费率参考 |
|---|------|------|---------|
| 1 | 科技成果转化费用损失保险 | 费用损失险 | — |
| 2 | 科技企业专利执行保险 | 知识产权维权险 | — |
| 3 | 科研仪器共享使用损坏补偿保险 | 设备损坏险 | — |
| 4 | 中试项目费用损失保险 | 费用损失险 | — |
| 5 | 自动控制系统责任保险 | 技术责任险 | — |
| 6 | 无人机机身一切险及第三者责任险 | 综合险 | — |

## 🔧 依赖

```bash
pip install pandas python-docx requests
```

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 🙏 致谢

- 太平科技保险股份有限公司 - 提供真实产品模板
- 中国保险行业协会 - 行业标准条款和附加险清单
- 国家金融监督管理总局 - 监管政策依据
