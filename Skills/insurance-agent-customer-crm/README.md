# 客户档案管理 Skill

> 专为保险代理人设计的客户资料整理工具，支持多格式文档提取、结构化档案生成和智能查询。

## 功能特点

- **多格式支持**：Excel、PDF、DOCX、PPTX、图片
- **智能提取**：规则预提取 + LLM 智能补全
- **结构化输出**：统一 Markdown 格式
- **档案合并**：多来源智能合并
- **自然语言查询**：用自然语言查询客户信息
- **到期提醒**：自动计算续费日期并生成提醒

## 安装

### 前置要求

- Python 3.8+
- API Key（MiniMax 或 OpenAI）

### 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

```python
import sys
sys.path.insert(0, '.')

from src.config import SkillConfig
from src.tools import extract_single_document, query_customer_profile

config = SkillConfig(
    api_key="your-api-key",
    base_url="https://api.minimax.chat/v1",
    model="MiniMax-M2.7"
)

result = extract_single_document("客户保单.xlsx", config)
print(result)

result = query_customer_profile(
    profiles_dir="./客户档案",
    query="这个客户有哪些保单？",
    config=config
)
```

## API 参考

### 配置

```python
from src.config import SkillConfig

config = SkillConfig(
    api_key="your-api-key",
    base_url="https://api.minimax.chat/v1",
    model="MiniMax-M2.7"
)
```

### 工具函数

| 函数 | 说明 |
|------|------|
| `extract_single_document(file_path, config)` | 提取单个文档 |
| `extract_customer_folder(folder_path, config)` | 批量提取文件夹 |
| `merge_customer_profiles(name, profiles)` | 合并档案 |
| `query_customer_profile(profiles_dir, query, config)` | 查询客户 |
| `update_customer_profile(profile_path, updates)` | 更新档案 |
| `generate_customer_report(customer_name, profiles_dir, config)` | 生成报告 |
| `generate_reminder_list(profiles_dir, days_ahead)` | 生成续费提醒 |

## 支持的文件格式

| 格式 | 扩展名 | 提取内容 |
|------|--------|----------|
| Excel | .xlsx, .xls | 表格数据、工作表信息 |
| PDF | .pdf | 文本内容、页数 |
| PowerPoint | .pptx | 幻灯片文本 |
| Word | .docx | 段落、表格 |
| 文本 | .txt, .md | 直接读取内容 |

## 项目结构

```
customer-profile-management/
├── src/
│   ├── __init__.py
│   ├── config.py           # 配置管理
│   ├── llm_client.py       # LLM 调用
│   ├── text_parser.py      # 文本解析
│   ├── document_extractor.py # 文档提取
│   ├── profile_merger.py   # 档案合并
│   └── tools.py            # 工具函数
├── prompts/
│   ├── extract_prompt.md   # 提取提示词
│   ├── merge_prompt.md     # 合并提示词
│   └── query_prompt.md     # 查询提示词
├── rules/
│   ├── column_patterns.json  # 列名映射
│   ├── field_keywords.json   # 字段关键词
│   └── data_template.md      # 数据模板
├── tests/                  # 测试文件
├── skill.yaml              # Clawhub 平台配置
├── requirements.txt        # Python 依赖
└── README.md
```

## 安全说明

- API Key 仅本地使用，不会上传到任何服务器
- 请勿将 .env 文件提交到公共仓库
- 客户资料仅本地处理

## License

MIT License
