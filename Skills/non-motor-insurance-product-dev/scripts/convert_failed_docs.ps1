# convert_failed_docs.ps1
# Convert broken .doc files to .docx using Word COM

$casesDir = "C:\Users\庄赫\.workbuddy\skills\non-motor-insurance-product\cases"

$failedDocs = @(
    "个人贷款保证保险\个人贷款保证保险条款.doc",
    "企业差旅服务应收账款信用保险\企业差旅服务应收账款信用保险费率表.doc",
    "团体旅行意外伤害保险\团体旅行意外伤害保险费率表.doc",
    "国内短期贸易信用保险（B款）\国内短期贸易信用保险（B款）费率表.doc",
    "国内短期贸易信用保险\国内短期贸易信用保险费率表.doc",
    "技术成果竞买履约保证保险\太平科技保险股份有限公司技术成果竞买履约保证保险业务承保风险策略20211124.doc",
    "技术成果竞买履约保证保险\太平科技保险股份有限公司技术成果竞买履约保证保险业务风险策略20211108.doc",
    "技术成果竞买履约保证保险\技术成果竞买履约保证保险条款.doc",
    "概念验证项目费用损失保险\概念验证项目费用损失保险费率表.doc",
    "特种设备第三者责任保险附加操作人员责任保险\特种设备第三者责任保险附加操作人员责任保险费率表.doc",
    "知识产权维权费用及侵权责任保险\知识产权维权费用及侵权责任保险条款_英文版.doc",
    "科技企业申请费用损失保险\科技企业申请费用损失保险费率表.doc",
    "科技企业贷款保证保险\太平科技保险股份有限公司科技企业贷款保证保险费率表.doc",
    "科技成果先用后转履约保证保险\科技成果先用后转履约保证保险条款.doc",
    "航空机票取消保险\航空机票取消保险条款.doc",
    "航空机票取消保险\航空机票取消保险费率表.doc",
    "航空机票取消保险附加扩展原因损失保险\航空机票取消保险附加扩展原因损失保险费率表.doc",
    "诉讼财产保全责任保险\诉讼财产保全责任保险条款.doc",
    "诉讼财产保全责任保险\诉讼财产保全责任保险费率表.doc",
    "高新技术企业贷款保证保险\太平科技保险股份有限公司高新技术企业贷款保证保险费率表.doc"
)

Write-Output "Converting $($failedDocs.Count) .doc files..."
Write-Output "=========================================="

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = $false

$success = 0
$failed = 0

foreach ($relativePath in $failedDocs) {
    $sourcePath = Join-Path $casesDir $relativePath
    $targetPath = [System.IO.Path]::ChangeExtension($sourcePath, ".docx")

    if (Test-Path $sourcePath) {
        try {
            $doc = $word.Documents.Open($sourcePath, $false, $true)
            $doc.SaveAs([ref]$targetPath, [ref]16)
            $doc.Close($false)
            Write-Output "[OK] $relativePath"
            $success++
        } catch {
            Write-Output "[FAIL] $relativePath - $($_.Exception.Message)"
            $failed++
        }
    } else {
        Write-Output "[SKIP] $relativePath - file not found"
    }
}

$word.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null

Write-Output "=========================================="
Write-Output "Done: $success succeeded, $failed failed"
