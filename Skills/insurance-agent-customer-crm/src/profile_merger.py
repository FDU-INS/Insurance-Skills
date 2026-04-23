from typing import Dict, List, Any
import re
from datetime import datetime


class ProfileMerger:
    def __init__(self):
        self.stats = {
            'total_profiles_processed': 0,
            'total_policies_merged': 0,
            'total_family_members_merged': 0,
            'conflicts_resolved': 0
        }

    def parse_profile(self, content: str, source: str) -> Dict[str, Any]:
        lines = content.strip().split('\n')
        info = {
            'name': '',
            'basic_info': {},
            'policies': [],
            'family_members': [],
            'health_info': {},
            'important_dates': {},
            'financial_info': {},
            'notes': '',
            'special_notes': '',
            'data_sources': []
        }

        if source:
            info['data_sources'].append(source)

        self._parse_basic_info(lines, info)
        self._parse_policies(lines, info)
        self._parse_family_members(lines, info)
        self._parse_health_info(lines, info)
        self._parse_important_dates(lines, info)
        self._parse_financial_info(lines, info)
        self._parse_notes(lines, info)
        self._parse_special_notes(lines, info)

        self.stats['total_profiles_processed'] += 1
        return info

    def _parse_basic_info(self, lines, info):
        in_basic_section = False
        current_section = []

        for line in lines:
            line = line.strip()
            if line.startswith('## 基本信息'):
                in_basic_section = True
                continue
            elif line.startswith('##') and in_basic_section:
                in_basic_section = False
                break
            elif in_basic_section and line.startswith('- **'):
                current_section.append(line)

        for item in current_section:
            match = re.match(r'- \*\*([^:]+)\*\*:\s*(.+)', item)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                info['basic_info'][key] = value
                if key == '姓名' or key == '客户姓名':
                    info['name'] = value

    def _parse_policies(self, lines, info):
        current_policy = None
        in_policy_section = False

        for line in lines:
            line = line.strip()

            if line.startswith('## 保单信息'):
                in_policy_section = True
                continue
            elif line.startswith('##') and in_policy_section:
                break

            if in_policy_section:
                policy_match = re.match(r'### 保单 \d+', line)
                if policy_match:
                    if current_policy:
                        info['policies'].append(current_policy)
                    current_policy = {}

                elif line.startswith('- **'):
                    match = re.match(r'- \*\*([^:]+)\*\*:\s*(.*)', line)
                    if match and current_policy is not None:
                        key = match.group(1).strip()
                        value = match.group(2).strip()
                        current_policy[key] = value

        if current_policy:
            info['policies'].append(current_policy)
            self.stats['total_policies_merged'] += len(info['policies'])

    def _parse_family_members(self, lines, info):
        in_family_section = False
        headers = []
        member_data = []

        for i, line in enumerate(lines):
            line = line.strip()

            if line.startswith('## 家庭成员'):
                in_family_section = True
                continue
            elif line.startswith('##') and in_family_section:
                break

            if in_family_section:
                if '|' in line and line.startswith('|'):
                    if not headers:
                        parts = [p.strip() for p in line.split('|')]
                        headers = [p for p in parts if p and p != '------']
                    else:
                        parts = [p.strip() for p in line.split('|')]
                        member = {}
                        for j, header in enumerate(headers):
                            if j + 1 < len(parts):
                                member[header] = parts[j + 1]
                        if member:
                            member_data.append(member)

        info['family_members'] = member_data
        self.stats['total_family_members_merged'] += len(member_data)

    def _parse_health_info(self, lines, info):
        in_health_section = False
        health_items = []

        for line in lines:
            line = line.strip()
            if line.startswith('## 健康信息'):
                in_health_section = True
                continue
            elif line.startswith('##') and in_health_section:
                break
            elif in_health_section and line.startswith('- **'):
                health_items.append(line)

        for item in health_items:
            match = re.match(r'- \*\*([^:]+)\*\*:\s*(.+)', item)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                info['health_info'][key] = value

    def _parse_important_dates(self, lines, info):
        in_dates_section = False
        date_items = []

        for line in lines:
            line = line.strip()
            if line.startswith('## 重要日期'):
                in_dates_section = True
                continue
            elif line.startswith('##') and in_dates_section:
                break
            elif in_dates_section and line.startswith('- **'):
                date_items.append(line)

        for item in date_items:
            match = re.match(r'- \*\*([^:]+)\*\*:\s*(.*)', item)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                info['important_dates'][key] = value

    def _parse_financial_info(self, lines, info):
        in_financial_section = False
        financial_items = []

        for line in lines:
            line = line.strip()
            if line.startswith('## 财务信息'):
                in_financial_section = True
                continue
            elif line.startswith('##') and in_financial_section:
                break
            elif in_financial_section and line.startswith('- **'):
                financial_items.append(line)

        for item in financial_items:
            match = re.match(r'- \*\*([^:]+)\*\*:\s*(.*)', item)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                info['financial_info'][key] = value

    def _parse_notes(self, lines, info):
        in_notes_section = False

        for line in lines:
            line = line.strip()
            if line.startswith('## 情况说明'):
                in_notes_section = True
                continue
            elif line.startswith('##') and in_notes_section:
                break
            elif in_notes_section and line.startswith('- '):
                if info['notes']:
                    info['notes'] += '\n' + line[2:].strip()
                else:
                    info['notes'] = line[2:].strip()

    def _parse_special_notes(self, lines, info):
        in_special_section = False
        notes = []

        for line in lines:
            line = line.strip()
            if line.startswith('## 特殊备注'):
                in_special_section = True
                continue
            elif line.startswith('##') and in_special_section:
                break
            elif in_special_section and line.startswith('- '):
                notes.append(line[2:].strip())

        if notes:
            info['special_notes'] = '\n'.join(notes)

    def _correct_gender(self, name: str, current_gender: str) -> str:
        if current_gender and current_gender not in ['男', '女', '待确认']:
            common_male_markers = ['先生', '男士', '男']
            common_female_markers = ['女士', '小姐', '太太', '女']

            for marker in common_female_markers:
                if marker in name:
                    return '女'
            for marker in common_male_markers:
                if marker in name:
                    return '男'

        return current_gender

    def merge_profiles(self, name: str, sources: List[Dict]) -> str:
        merged: Dict[str, Any] = {
            'name': name,
            'basic_info': {},
            'policies': [],
            'family_members': [],
            'health_info': {},
            'important_dates': {},
            'financial_info': {},
            'notes': '',
            'special_notes': '',
            'data_sources': []
        }

        seen_policies = set()
        seen_family_members = set()

        for source in sources:
            if 'basic_info' in source:
                for key, value in source['basic_info'].items():
                    if value and value not in ['待确认', '待补充', '待了解', '待评估']:
                        if key not in merged['basic_info'] or merged['basic_info'][key] in ['待确认', '待补充', '待了解', '待评估']:
                            merged['basic_info'][key] = value
                            self.stats['conflicts_resolved'] += 1
                        elif merged['basic_info'][key] != value:
                            self.stats['conflicts_resolved'] += 1

            if 'policies' in source:
                for policy in source['policies']:
                    policy_key = self._get_policy_key(policy)
                    if policy_key and policy_key not in seen_policies:
                        seen_policies.add(policy_key)
                        merged['policies'].append(policy)

            if 'family_members' in source:
                for member in source['family_members']:
                    member_key = self._get_member_key(member)
                    if member_key and member_key not in seen_family_members:
                        seen_family_members.add(member_key)
                        merged['family_members'].append(member)

            for section in ['health_info', 'important_dates', 'financial_info']:
                if section in source:
                    for key, value in source[section].items():
                        if value and value not in ['待确认', '待补充', '待了解', '待评估']:
                            if key not in merged[section] or merged[section][key] in ['待确认', '待补充', '待了解', '待评估']:
                                merged[section][key] = value

            if source.get('notes'):
                if merged['notes']:
                    merged['notes'] += '\n' + source['notes']
                else:
                    merged['notes'] = source['notes']

            if source.get('special_notes'):
                if merged['special_notes']:
                    merged['special_notes'] += '\n' + source['special_notes']
                else:
                    merged['special_notes'] = source['special_notes']

            if source.get('data_sources'):
                merged['data_sources'].extend(source['data_sources'])

        if '性别' in merged['basic_info']:
            merged['basic_info']['性别'] = self._correct_gender(
                name,
                merged['basic_info']['性别']
            )

        return self._generate_markdown(merged)

    def _get_policy_key(self, policy: Dict) -> str:
        company = policy.get('保险公司', '')
        product = policy.get('产品名称', '')
        policy_num = policy.get('保单号', '')
        return f"{company}|{product}|{policy_num}"

    def _get_member_key(self, member: Dict) -> str:
        name = member.get('姓名', '')
        relation = member.get('关系', '')
        birth = member.get('出生日期', '')
        return f"{name}|{relation}|{birth}"

    def _generate_markdown(self, info: Dict) -> str:
        lines = []

        name = info.get('name', '')
        if not name:
            name = '未命名客户'

        lines.append(f"# {name}\n")

        lines.append("## 基本信息")
        basic_fields = [
            '性别', '出生日期', '年龄', '手机号', '邮箱', '身份证号',
            '住址', '职业', '工作单位', '婚姻状况', '与投保人关系'
        ]

        for field in basic_fields:
            value = info['basic_info'].get(field, '待确认')
            if not value:
                value = '待确认'
            lines.append(f"- **{field}**: {value}")

        lines.append("\n## 家庭成员")
        if info['family_members']:
            lines.append("| 姓名 | 关系 | 出生日期 | 性别 | 手机 | 备注 |")
            lines.append("|------|------|----------|------|------|------|")
            for member in info['family_members']:
                name_val = member.get('姓名', '')
                relation_val = member.get('关系', '')
                birth_val = member.get('出生日期', '')
                gender_val = member.get('性别', '')
                phone_val = member.get('手机', '')
                notes_val = member.get('备注', '')
                lines.append(f"| {name_val} | {relation_val} | {birth_val} | {gender_val} | {phone_val} | {notes_val} |")
        else:
            lines.append("暂无家庭成员信息")

        lines.append("\n## 保单信息")
        if info['policies']:
            for i, policy in enumerate(info['policies'], 1):
                lines.append(f"### 保单 {i}")
                policy_fields = [
                    '保险公司', '产品名称', '保单号', '投保人', '被保险人',
                    '受益人', '保额', '保费', '缴费年限', '生效日期',
                    '保险期间', '保单状态'
                ]
                for field in policy_fields:
                    value = policy.get(field, '')
                    if not value:
                        value = '待补充'
                    lines.append(f"- **{field}**: {value}")
                lines.append("")
        else:
            lines.append("暂无保单信息")

        lines.append("## 健康信息")
        health_fields = ['既往病史', '体检记录', '健康状况']
        for field in health_fields:
            value = info['health_info'].get(field, '待了解')
            if not value:
                value = '待了解'
            lines.append(f"- **{field}**: {value}")

        lines.append("\n## 重要日期")
        date_fields = ['生日', '保单周年', '续费日期', '下次跟进日期']
        for field in date_fields:
            value = info['important_dates'].get(field, '')
            if not value:
                value = ''
            lines.append(f"- **{field}**: {value}")

        lines.append("\n## 财务信息")
        financial_fields = ['年收入', '主要诉求']
        for field in financial_fields:
            value = info['financial_info'].get(field, '待评估')
            if not value:
                value = '待评估'
            lines.append(f"- **{field}**: {value}")

        lines.append("\n## 情况说明")
        notes = info.get('notes', '')
        if notes:
            lines.append(f"- {notes}")
        else:
            lines.append("- （暂无情况说明）")

        lines.append("\n## 特殊备注")
        special_notes = info.get('special_notes', '')
        if special_notes:
            lines.append(f"- {special_notes}")
        else:
            lines.append("- ")

        lines.append("\n## 数据来源")
        data_sources = info.get('data_sources', [])
        if data_sources:
            for source in data_sources:
                lines.append(f"- {source}")
        else:
            lines.append("- ")

        today = datetime.now().strftime('%Y-%m-%d')
        lines.append("\n---")
        lines.append(f"> 创建时间：{today}")
        lines.append(f"> 最后更新：{today}")

        return '\n'.join(lines)

    def get_statistics(self) -> Dict[str, int]:
        return self.stats.copy()
