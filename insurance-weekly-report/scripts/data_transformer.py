#!/usr/bin/env python3
"""
数据转换模块 - 支持多种数据格式自动识别和转换
符合 Anthropic Skills 最佳实践
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path


class DataTransformer:
    """数据转换器 - 处理字段映射和数据聚合"""

    def __init__(self, mappings_file=None):
        """
        初始化转换器

        Args:
            mappings_file: 字段映射配置文件路径
        """
        if mappings_file is None:
            # 默认路径
            script_dir = Path(__file__).parent
            mappings_file = script_dir.parent / "references" / "field_mappings.json"

        self.mappings = self._load_mappings(mappings_file)

    def _load_mappings(self, mappings_file):
        """加载字段映射配置"""
        try:
            with open(mappings_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠ 未找到映射配置文件: {mappings_file}")
            print("  将使用默认映射规则")
            return self._get_default_mappings()
        except json.JSONDecodeError as e:
            print(f"✗ 映射配置文件格式错误: {e}")
            return self._get_default_mappings()

    def _get_default_mappings(self):
        """返回默认映射配置（当配置文件缺失时使用）"""
        return {
            "预设映射方案": {
                "汇总数据_中文字段": {
                    "触发条件": {
                        "必须包含字段": ["机构", "客户类别", "签单保费"]
                    },
                    "字段映射": {},
                    "需要聚合": False
                }
            }
        }

    def detect_format(self, df):
        """
        自动检测数据格式

        Args:
            df: pandas DataFrame

        Returns:
            (scheme_name, scheme_config) 或 (None, None) 如果未识别
        """
        schemes = self.mappings.get("预设映射方案", {})

        for scheme_name, scheme_config in schemes.items():
            trigger = scheme_config.get("触发条件", {})
            required_fields = trigger.get("必须包含字段", [])

            # 检查是否所有必需字段都存在
            if all(field in df.columns for field in required_fields):
                print(f"✓ 检测到数据格式: {scheme_name}")
                print(f"  描述: {scheme_config.get('描述', 'N/A')}")
                return scheme_name, scheme_config

        return None, None

    def transform(self, df, scheme_name=None):
        """
        转换数据为标准格式

        Args:
            df: 原始数据 DataFrame
            scheme_name: 指定映射方案名称（可选，不指定则自动检测）

        Returns:
            转换后的 DataFrame
        """
        # 自动检测或使用指定方案
        if scheme_name is None:
            scheme_name, scheme_config = self.detect_format(df)
        else:
            schemes = self.mappings.get("预设映射方案", {})
            scheme_config = schemes.get(scheme_name)

        if scheme_config is None:
            print("⚠ 未识别数据格式，假设已为标准格式")
            return df

        # 执行字段映射
        df_mapped = self._apply_field_mapping(df, scheme_config)

        # 如果需要聚合，执行聚合操作
        if scheme_config.get("需要聚合", False):
            print("  执行数据聚合...")
            df_result = self._aggregate_data(df_mapped, scheme_config)
        else:
            df_result = df_mapped

        return df_result

    def _apply_field_mapping(self, df, scheme_config):
        """应用字段映射"""
        field_mappings = scheme_config.get("字段映射", {})

        if not field_mappings:
            return df

        print(f"  应用字段映射 ({len(field_mappings)} 个字段)...")
        return df.rename(columns=field_mappings)

    def _aggregate_data(self, df, scheme_config):
        """
        聚合明细数据为汇总数据

        支持三种聚合维度：
        1. 分机构
        2. 分客户类别
        3. 分机构+客户类别
        """
        agg_config = scheme_config.get("聚合配置", {})
        dimensions = agg_config.get("聚合维度", ["机构", "客户类别"])
        agg_fields = agg_config.get("聚合字段", {})
        calc_metrics = agg_config.get("计算指标", {})
        output_fields = agg_config.get("输出字段", [])

        # 确保数值字段为数值类型
        for target_field, source_field in agg_fields.items():
            if source_field in df.columns:
                df[source_field] = pd.to_numeric(df[source_field], errors='coerce').fillna(0)

        # 准备聚合字典
        agg_dict = {source: 'sum' for source in agg_fields.values() if source in df.columns}

        results = []

        # 1. 分机构聚合
        if "机构" in dimensions:
            org_agg = df.groupby("机构").agg(agg_dict).reset_index()
            # 重命名聚合后的字段
            rename_map = {v: k for k, v in agg_fields.items() if v in org_agg.columns}
            org_agg = org_agg.rename(columns=rename_map)
            org_agg["客户类别"] = "全部"
            results.append(org_agg)

        # 2. 分客户类别聚合
        if "客户类别" in dimensions:
            cust_agg = df.groupby("客户类别").agg(agg_dict).reset_index()
            rename_map = {v: k for k, v in agg_fields.items() if v in cust_agg.columns}
            cust_agg = cust_agg.rename(columns=rename_map)
            cust_agg["机构"] = "全部"
            results.append(cust_agg)

        # 3. 分机构+客户类别聚合
        if "机构" in dimensions and "客户类别" in dimensions:
            org_cust_agg = df.groupby(["机构", "客户类别"]).agg(agg_dict).reset_index()
            rename_map = {v: k for k, v in agg_fields.items() if v in org_cust_agg.columns}
            org_cust_agg = org_cust_agg.rename(columns=rename_map)
            results.append(org_cust_agg)

        # 合并所有聚合结果
        if not results:
            print("  ⚠ 未执行任何聚合操作")
            return df

        result_df = pd.concat(results, ignore_index=True)

        # 计算派生指标
        result_df = self._calculate_metrics(result_df, calc_metrics)

        # 选择输出字段
        if output_fields:
            available_fields = [f for f in output_fields if f in result_df.columns]
            result_df = result_df[available_fields]

        print(f"  ✓ 聚合完成: {len(result_df)} 条记录")
        return result_df

    def _calculate_metrics(self, df, calc_metrics):
        """计算派生指标（如赔付率、费用率等）"""
        for metric_name, metric_config in calc_metrics.items():
            formula = metric_config.get("公式", "")
            decimals = metric_config.get("保留小数", 2)
            error_handling = metric_config.get("异常值处理", "替换为0")

            try:
                # 解析公式并计算
                # 支持的公式格式：字段名 / 字段名 * 100
                df[metric_name] = self._eval_formula(df, formula, decimals)

                # 处理异常值
                if error_handling == "替换为0":
                    df[metric_name] = df[metric_name].replace([np.inf, -np.inf], 0).fillna(0)

            except Exception as e:
                print(f"  ⚠ 计算指标 '{metric_name}' 时出错: {e}")
                df[metric_name] = 0

        return df

    def _eval_formula(self, df, formula, decimals):
        """
        安全地计算公式（增强版）

        支持的操作符：+, -, *, /, ()
        示例公式：
        - "已报告赔款 / 满期保费 * 100"
        - "(出险件数 / 保单件数) * 满期率 / 100"
        - "100 - 变动成本率"
        """
        import re

        # 提取所有字段名和数字
        tokens = re.findall(r'[\u4e00-\u9fa5_a-zA-Z0-9]+', formula)

        # 构建安全的命名空间
        namespace = {}
        for token in tokens:
            if token in df.columns:
                namespace[token] = df[token]
            elif token.replace('.', '').isdigit():  # 数字（支持小数）
                # 不需要添加到namespace，数字会直接在公式中保留
                pass

        # 替换公式中的字段名为命名空间引用
        safe_formula = formula
        # 按字段名长度降序排序，避免短字段名被误替换
        sorted_fields = sorted([f for f in tokens if f in df.columns], key=len, reverse=True)
        for field in sorted_fields:
            safe_formula = safe_formula.replace(field, f"namespace['{field}']")

        # 计算结果
        try:
            result = eval(safe_formula, {"__builtins__": {}}, {"namespace": namespace})
            if isinstance(result, pd.Series):
                return result.round(decimals)
            else:
                # 如果结果是标量，转换为Series
                return pd.Series([result] * len(df)).round(decimals)
        except Exception as e:
            print(f"  ⚠ 公式求值失败: {formula} - {e}")
            return pd.Series([0] * len(df))

    def get_available_schemes(self):
        """获取所有可用的映射方案"""
        schemes = self.mappings.get("预设映射方案", {})
        return {
            name: config.get("描述", "无描述")
            for name, config in schemes.items()
        }

    def validate_output(self, df):
        """
        验证输出数据是否符合标准格式

        Returns:
            (is_valid, missing_fields)
        """
        required_fields = [
            "机构", "客户类别", "签单保费", "满期赔付率",
            "费用率", "变动成本率", "已报告赔款", "出险率", "案均赔款"
        ]

        missing = [field for field in required_fields if field not in df.columns]

        return len(missing) == 0, missing


# 便捷函数
def auto_transform(df, mappings_file=None):
    """
    自动转换数据（一步完成检测+转换）

    Args:
        df: 原始数据 DataFrame
        mappings_file: 映射配置文件路径（可选）

    Returns:
        转换后的 DataFrame
    """
    transformer = DataTransformer(mappings_file)
    return transformer.transform(df)


# 测试代码
if __name__ == "__main__":
    print("=" * 80)
    print("数据转换模块测试")
    print("=" * 80)

    # 创建测试数据（模拟明细数据）
    test_data = {
        'third_level_organization': ['天府', '天府', '高新', '高新'],
        'customer_category_3': ['家用车', '货车', '家用车', '货车'],
        'signed_premium_yuan': [1000000, 500000, 800000, 300000],
        'matured_premium_yuan': [1000000, 500000, 800000, 300000],
        'reported_claim_payment_yuan': [600000, 350000, 480000, 200000],
        'expense_amount_yuan': [150000, 80000, 120000, 50000],
        'policy_count': [100, 50, 80, 30],
        'claim_case_count': [20, 15, 18, 10]
    }

    df_test = pd.DataFrame(test_data)

    print("\n原始数据 (前3行):")
    print(df_test.head(3))

    # 测试转换
    transformer = DataTransformer()
    df_transformed = transformer.transform(df_test)

    print("\n转换后数据:")
    print(df_transformed)

    # 验证输出
    is_valid, missing = transformer.validate_output(df_transformed)
    print(f"\n验证结果: {'✓ 通过' if is_valid else f'✗ 失败 - 缺少字段: {missing}'}")
