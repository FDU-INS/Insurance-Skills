"""
Text Parser Module - Rule-based text extraction
"""
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional


class TextParser:
    def __init__(self, trigger_threshold: float = 0.5, min_table_rows: int = 3):
        self.trigger_threshold = trigger_threshold
        self.min_table_rows = min_table_rows
        self._field_keywords = self._load_field_keywords()
        self._column_patterns = self._load_column_patterns()

    def _get_rules_dir(self) -> Path:
        current_file = Path(__file__).resolve()
        return current_file.parent.parent / "rules"

    def _load_field_keywords(self) -> Dict[str, Any]:
        rules_path = self._get_rules_dir() / "field_keywords.json"
        with open(rules_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_column_patterns(self) -> Dict[str, List[str]]:
        rules_path = self._get_rules_dir() / "column_patterns.json"
        with open(rules_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def parse_markdown_table(self, content: str) -> List[List[str]]:
        lines = content.strip().split("\n")
        tables: List[List[List[str]]] = []
        current_table: List[List[str]] = []
        in_table = False

        for line in lines:
            line = line.strip()
            if not line:
                if current_table:
                    tables.append(current_table)
                    current_table = []
                    in_table = False
                continue

            if re.match(r"^\|.+\|$", line):
                in_table = True
                cells = [cell.strip() for cell in line.split("|")]
                cells = [c for c in cells if c != ""]
                if cells:
                    current_table.append(cells)
            elif in_table and current_table:
                tables.append(current_table)
                current_table = []
                in_table = False

        if current_table:
            tables.append(current_table)

        return tables[0] if tables else []

    def extract_by_regex(self, content: str) -> Dict[str, Any]:
        result = {}

        phone_pattern = r"1[3-9]\d{9}"
        phones = re.findall(phone_pattern, content)
        result["手机号"] = list(set(phones)) if phones else []

        id_pattern = r"\d{17}[\dXx]"
        ids = re.findall(id_pattern, content)
        result["身份证号"] = list(set([id.upper() for id in ids])) if ids else []

        date_pattern = r"\d{4}[-/年]\d{1,2}[-/月]\d{1,2}日?"
        dates = re.findall(date_pattern, content)
        result["日期"] = dates if dates else []

        amount_pattern = r"(?:￥|¥|\$|RMB)?\s*\d+(?:\.\d{1,2})?"
        amounts = re.findall(amount_pattern, content)
        result["金额"] = amounts if amounts else []

        gender_pattern = r"[男女]"
        genders = re.findall(gender_pattern, content)
        result["性别"] = genders if genders else []

        name_pattern = r"[\u4e00-\u9fa5]{2,4}(?=\s*(?:男|女|先生|女士|姐|哥))"
        names = re.findall(name_pattern, content)
        result["姓名"] = names if names else []

        return result

    def extract_from_table(self, table: List[List[str]]) -> Dict[str, Any]:
        if len(table) < 2:
            return {}

        header = table[0]
        data_rows = table[1:] if len(table) > 1 else []

        normalized_header = []
        for col in header:
            col_lower = col.strip().lower()
            field_name = col
            for standard_name, patterns in self._column_patterns.items():
                if col_lower in [p.lower() for p in patterns] or col_lower == standard_name.lower():
                    field_name = standard_name
                    break
            normalized_header.append(field_name)

        result: Dict[str, Any] = {"表格数据": {}}

        for i, header_cell in enumerate(normalized_header):
            col_values = []
            for row in data_rows:
                if i < len(row):
                    col_values.append(row[i].strip())
            if col_values:
                result["表格数据"][header_cell] = col_values

        return result

    def extract_family_members(self, content: str) -> List[Dict[str, str]]:
        members: List[Dict[str, str]] = []
        relationship_keywords = self._field_keywords.get("relationship_keywords", {})

        relationships = "|".join([
            "|".join(kw_list) for kw_list in relationship_keywords.values()
        ])

        pattern = rf"([\u4e00-\u9fa5]{1,5})\s*[:：]?\s*({relationships})"
        matches = re.findall(pattern, content)

        for name, relation in matches:
            member: Dict[str, str] = {"姓名": name.strip(), "关系": relation.strip()}
            if member not in members:
                members.append(member)

        return members

    def should_trigger_llm(self, extracted_info: Dict, content: str) -> Tuple[bool, str]:
        field_keywords = self._field_keywords.get("field_keywords", {})

        matched_fields = 0
        total_fields = len(field_keywords)

        for field, keywords in field_keywords.items():
            for keyword in keywords:
                if keyword in content:
                    matched_fields += 1
                    break

        coverage = matched_fields / total_fields if total_fields > 0 else 0

        table = self.parse_markdown_table(content)
        has_sufficient_table = len(table) >= self.min_table_rows

        regex_info = self.extract_by_regex(content)
        has_sufficient_regex = (
            len(regex_info.get("手机号", [])) > 0 or
            len(regex_info.get("身份证号", [])) > 0 or
            len(regex_info.get("日期", [])) > 0
        )

        if coverage >= self.trigger_threshold and has_sufficient_table:
            return False, "规则提取已覆盖主要内容"
        elif not has_sufficient_regex and not has_sufficient_table:
            return True, "内容信息不足，需要LLM补充提取"
        else:
            return True, "信息完整度一般，建议LLM完善"

    def detect_file_type(self, content: str, filename: str = "") -> str:
        file_type_indicators = self._field_keywords.get("file_type_indicators", {})

        if filename:
            ext = filename.lower()
            if ".xlsx" in ext or ".xls" in ext:
                return "excel"
            elif ".pdf" in ext:
                return "pdf"
            elif ".pptx" in ext or ".ppt" in ext:
                return "pptx"
            elif ".docx" in ext or ".doc" in ext:
                return "docx"
            elif ".png" in ext or ".jpg" in ext or ".jpeg" in ext or ".gif" in ext or ".bmp" in ext:
                return "image"

        for file_type, indicators in file_type_indicators.items():
            for indicator in indicators:
                if indicator in content:
                    return file_type

        return "unknown"

    def rule_extract(self, content: str, filename: str = "") -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "file_type": self.detect_file_type(content, filename),
            "regex_info": self.extract_by_regex(content),
            "tables": [],
            "family_members": [],
            "trigger_llm": True,
            "trigger_reason": ""
        }

        tables = self.parse_markdown_table(content)
        if tables:
            result["tables"].append(tables)
            table_info = self.extract_from_table(tables)
            result.update(table_info)

        family_members = self.extract_family_members(content)
        if family_members:
            result["family_members"] = family_members

        trigger_llm, trigger_reason = self.should_trigger_llm(result, content)
        result["trigger_llm"] = trigger_llm
        result["trigger_reason"] = trigger_reason

        return result
