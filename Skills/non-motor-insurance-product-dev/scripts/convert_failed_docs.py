# -*- coding: utf-8 -*-
"""
convert_failed_docs.py
使用 Python win32com 直接操作 Word，将损坏的 .doc 文件转换为 .docx 格式
"""

import os
import sys
import win32com.client
import pythoncom

cases_dir = r"C:\Users\庄赫\.workbuddy\skills\non-motor-insurance-product\cases"

# 失败的 .doc 文件列表
failed_docs = [
    "个人贷款保证保险/个人贷款保证保险条款.doc",
    "企业差旅服务应收账款信用保险/企业差旅服务应收账款信用保险费率表.doc",
    "团体旅行意外伤害保险/团体旅行意外伤害保险费率表.doc",
    "国内短期贸易信用保险（B款）/国内短期贸易信用保险（B款）费率表.doc",
    "国内短期贸易信用保险/国内短期贸易信用保险费率表.doc",
    "技术成果竞买履约保证保险/太平科技保险股份有限公司技术成果竞买履约保证保险业务承保风险策略20211124.doc",
    "技术成果竞买履约保证保险/太平科技保险股份有限公司技术成果竞买履约保证保险业务风险策略20211108.doc",
    "技术成果竞买履约保证保险/技术成果竞买履约保证保险条款.doc",
    "概念验证项目费用损失保险/概念验证项目费用损失保险费率表.doc",
    "特种设备第三者责任保险附加操作人员责任保险/特种设备第三者责任保险附加操作人员责任保险费率表.doc",
    "知识产权维权费用及侵权责任保险/知识产权维权费用及侵权责任保险条款_英文版.doc",
    "科技企业申请费用损失保险/科技企业申请费用损失保险费率表.doc",
    "科技企业贷款保证保险/太平科技保险股份有限公司科技企业贷款保证保险费率表.doc",
    "科技成果先用后转履约保证保险/科技成果先用后转履约保证保险条款.doc",
    "航空机票取消保险/航空机票取消保险条款.doc",
    "航空机票取消保险/航空机票取消保险费率表.doc",
    "航空机票取消保险附加扩展原因损失保险/航空机票取消保险附加扩展原因损失保险费率表.doc",
    "诉讼财产保全责任保险/诉讼财产保全责任保险条款.doc",
    "诉讼财产保全责任保险/诉讼财产保全责任保险费率表.doc",
    "高新技术企业贷款保证保险/太平科技保险股份有限公司高新技术企业贷款保证保险费率表.doc",
]

# wdFormatXMLDocument = 16
WD_FORMAT_XML_DOCUMENT = 16

def convert():
    print(f"Converting {len(failed_docs)} .doc files using Word COM...")
    print("=" * 60)

    # 初始化 COM
    pythoncom.CoInitialize()

    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0  # wdAlertsNone

        success = 0
        failed = 0

        import time
        for relative_path in failed_docs:
            source_path = os.path.join(cases_dir, relative_path)
            target_path = os.path.splitext(source_path)[0] + ".docx"

            if not os.path.exists(source_path):
                print(f"[SKIP] {relative_path} - source file not found")
                continue

            if os.path.exists(target_path):
                print(f"[EXIST] {relative_path} - .docx already exists")
                continue

            try:
                time.sleep(1)  # 延迟避免COM服务器过载
                doc = word.Documents.Open(source_path, False, True)
                time.sleep(1)
                doc.SaveAs(target_path, WD_FORMAT_XML_DOCUMENT)
                time.sleep(0.5)
                doc.Close(False)
                print(f"[OK] {relative_path}")
                success += 1
            except Exception as e:
                print(f"[FAIL] {relative_path} - {str(e)}")
                failed += 1
                # 如果Word崩溃，重新启动
                try:
                    word.Quit(0, 0, 0)
                except:
                    pass
                time.sleep(3)
                word = win32com.client.Dispatch("Word.Application")
                word.Visible = False
                word.DisplayAlerts = 0

        # 使用 COM 对象的方法退出
        try:
            word.Quit(0, 0, 0)  # 使用参数调用 Quit
        except:
            pass  # 忽略退出时的错误

    finally:
        pythoncom.CoUninitialize()

    print("=" * 60)
    print(f"Done: {success} succeeded, {failed} failed")
    return success, failed

if __name__ == "__main__":
    convert()
