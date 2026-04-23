#!/usr/bin/env bash
# insurance-advisor — 保险方案顾问
# Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
set -euo pipefail

CMD="${1:-help}"
shift 2>/dev/null || true

show_help() {
  cat <<'EOF'
╔══════════════════════════════════════════════════════════╗
║            🛡️ Insurance Advisor 保险方案顾问             ║
╚══════════════════════════════════════════════════════════╝

Usage: bash insurance.sh <command> [args...]

Commands:
  recommend <age> <income> [family_status]     保险方案推荐
      family_status: single | married | married-with-kids
  compare   <type>                             同类险种对比
      type: medical | critical | life | accident
  calculate <type> <age> <coverage> [term]     估算保费
  claim     <type>                             理赔流程指南
  term      <age> <coverage> <years>           定期寿险方案
  health    <age> [pre_conditions]             健康险推荐
  help                                         显示此帮助

Examples:
  bash insurance.sh recommend 30 20000 married-with-kids
  bash insurance.sh compare critical
  bash insurance.sh calculate life 35 1000000 20
  bash insurance.sh claim medical
  bash insurance.sh term 30 500000 20
  bash insurance.sh health 40 hypertension

  Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
EOF
}

cmd_recommend() {
  local age="${1:?用法: recommend <age> <income> [family_status]}"
  local income="${2:?请提供月收入}"
  local status="${3:-single}"

  local annual_income budget
  annual_income=$(echo "$income * 12" | bc)
  budget=$(echo "$annual_income * 0.07" | bc)  # 7% of annual income

  local status_cn
  case "$status" in
    single) status_cn="单身" ;;
    married) status_cn="已婚无小孩" ;;
    married-with-kids) status_cn="已婚有小孩" ;;
    *) status_cn="$status" ;;
  esac

  cat <<EOF
╔══════════════════════════════════════════════════════════╗
║           🛡️ 保险方案推荐
╚══════════════════════════════════════════════════════════╝

📋 个人信息
────────────────────────────────────────
  年龄:     ${age}岁
  月收入:   ¥$(printf "%'.0f" "$income")
  年收入:   ¥$(printf "%'.0f" "$annual_income")
  家庭状态: ${status_cn}
  建议预算: ¥$(printf "%'.0f" "$budget")/年 (年收入7%)

📊 推荐方案（按优先级排序）
────────────────────────────────────────

  🏥 1. 百万医疗险 [必备]
     保额: 200-400万    保费: ~¥300-800/年
     作用: 覆盖大病住院费用
     优先级: ⭐⭐⭐⭐⭐

  🏥 2. 重疾险 [强烈推荐]
     保额: 30-50万      保费: ~¥3,000-8,000/年
     作用: 确诊即赔，弥补收入损失
     优先级: ⭐⭐⭐⭐⭐
EOF

  if [ "$age" -lt 50 ]; then
    cat <<EOF

  ⚡ 3. 意外险 [推荐]
     保额: 50-100万     保费: ~¥150-300/年
     作用: 意外伤残/身故赔付
     优先级: ⭐⭐⭐⭐
EOF
  fi

  case "$status" in
    married|married-with-kids)
      cat <<EOF

  💀 4. 定期寿险 [家庭支柱必备]
     保额: 年收入x10    保费: ~¥1,000-3,000/年
     作用: 身故后家庭经济保障
     优先级: ⭐⭐⭐⭐⭐
EOF
      ;;
  esac

  if [ "$status" = "married-with-kids" ]; then
    cat <<EOF

  👶 5. 少儿医疗+意外 [为孩子]
     保额: 各100万      保费: ~¥500-1,500/年
     作用: 孩子医疗和意外保障
     优先级: ⭐⭐⭐⭐
EOF
  fi

  cat <<EOF

💡 配置原则
────────────────────────────────────────
  ✅ 先大人后小孩（大人是收入来源）
  ✅ 先保障后理财（先买纯保障型）
  ✅ 保额充足 > 保障全面 > 品牌大小
  ✅ 预算有限先买消费型

⚠️  以上为通用建议，具体方案请咨询持牌保险经纪人
EOF
}

cmd_compare() {
  local type="${1:?用法: compare <type> (medical|critical|life|accident)}"

  echo "╔══════════════════════════════════════════════════════════╗"
  echo "║           🔄 险种对比: ${type}"
  echo "╚══════════════════════════════════════════════════════════╝"
  echo ""

  case "$type" in
    medical)
      cat <<'EOF'
📊 百万医疗险对比
────────────────────────────────────────
  特征        基础版         中端版         高端版
  ──────────────────────────────────────────────
  保额        200万          400万          800万
  免赔额      1万            5千            0
  门诊        ❌             部分✅          ✅
  特需病房    ❌             ❌             ✅
  海外就医    ❌             ❌             ✅
  保费(30岁)  ~¥300/年      ~¥800/年      ~¥5,000/年
  续保        保证续保       保证续保       视产品而定

💡 建议: 大多数人选基础版就够了，1万免赔额有医保可覆盖
EOF
      ;;
    critical)
      cat <<'EOF'
📊 重疾险对比
────────────────────────────────────────
  特征        消费型         储蓄型         终身型
  ──────────────────────────────────────────────
  保障期限    到60/70岁      到60/70岁      终身
  到期返还    ❌             ✅             ❌(身故赔)
  保费(30岁)  ~¥2,000/年    ~¥4,000/年    ~¥6,000/年
  保额建议    30-50万        30-50万        30-50万
  杠杆率      最高           一般           较低

💡 建议: 预算有限选消费型，保额为年收入的3-5倍
EOF
      ;;
    life)
      cat <<'EOF'
📊 寿险对比
────────────────────────────────────────
  特征        定期寿险       终身寿险       增额终身寿
  ──────────────────────────────────────────────
  保障期限    到60/70岁      终身           终身
  是否返还    ❌             身故赔保额     现金价值增长
  保费(30岁)  ~¥1,000/年    ~¥8,000/年    ~¥15,000/年
  适合人群    家庭支柱       财富传承       资产配置

💡 建议: 普通家庭选定期寿险，保到子女经济独立即可
EOF
      ;;
    accident)
      cat <<'EOF'
📊 意外险对比
────────────────────────────────────────
  特征        基础版         综合版         尊享版
  ──────────────────────────────────────────────
  意外身故    50万           100万          300万
  意外伤残    50万(按比例)   100万(按比例)  300万(按比例)
  意外医疗    1万            5万            10万
  住院津贴    ❌             ✅ 100元/天    ✅ 300元/天
  猝死保障    ❌             ✅             ✅
  保费        ~¥150/年      ~¥300/年      ~¥600/年

💡 建议: 综合版性价比最高，注意选含猝死保障的
EOF
      ;;
    *)
      echo "❌ 未知险种类型: $type"
      echo "支持: medical, critical, life, accident"
      ;;
  esac
}

cmd_calculate() {
  local type="${1:?用法: calculate <type> <age> <coverage> [term]}"
  local age="${2:?请提供年龄}"
  local coverage="${3:?请提供保额}"
  local term="${4:-20}"

  # Simplified premium estimation
  local base_rate premium
  case "$type" in
    medical)  base_rate="0.0004" ;;
    critical) base_rate="0.008" ;;
    life)     base_rate="0.002" ;;
    accident) base_rate="0.003" ;;
    *)        base_rate="0.005" ;;
  esac

  # Age factor
  local age_factor
  if [ "$age" -lt 30 ]; then age_factor="0.8"
  elif [ "$age" -lt 40 ]; then age_factor="1.0"
  elif [ "$age" -lt 50 ]; then age_factor="1.5"
  else age_factor="2.2"; fi

  premium=$(echo "scale=0; $coverage * $base_rate * $age_factor" | bc)

  local type_cn
  case "$type" in
    medical)  type_cn="百万医疗险" ;;
    critical) type_cn="重疾险" ;;
    life)     type_cn="寿险" ;;
    accident) type_cn="意外险" ;;
    *)        type_cn="$type" ;;
  esac

  cat <<EOF
╔══════════════════════════════════════════════════════════╗
║           💰 保费估算: ${type_cn}
╚══════════════════════════════════════════════════════════╝

📋 方案信息
────────────────────────────────────────
  险种:     ${type_cn}
  年龄:     ${age}岁
  保额:     ¥$(printf "%'.0f" "$coverage")
  保障期限: ${term}年

💰 保费估算
────────────────────────────────────────
  年缴保费: ¥$(printf "%'.0f" "$premium")
  月均成本: ¥$(printf "%'.0f" "$(echo "$premium / 12" | bc)")
  缴费总计: ¥$(printf "%'.0f" "$(echo "$premium * $term" | bc)") (${term}年)

📊 保费占收入建议
────────────────────────────────────────
  保费应 ≤ 年收入的 5-7%
  单项保险保费 ≤ 年收入的 2-3%

⚠️  以上为估算值，实际保费以保险公司核保为准
EOF
}

cmd_claim() {
  local type="${1:?用法: claim <type> (medical|critical|life|accident)}"

  echo "╔══════════════════════════════════════════════════════════╗"
  echo "║           📋 理赔流程指南"
  echo "╚══════════════════════════════════════════════════════════╝"
  echo ""

  case "$type" in
    medical)
      cat <<'EOF'
🏥 医疗险理赔流程
────────────────────────────────────────

  Step 1 📞 报案
  ─────────────────
  • 住院后48小时内通知保险公司
  • 拨打保险公司客服电话
  • 告知就诊医院、疾病名称

  Step 2 📋 收集材料
  ─────────────────
  • 身份证复印件
  • 银行卡复印件
  • 诊断证明 / 出院小结
  • 医疗费用清单（加盖医院公章）
  • 发票原件（医保报销后提供分割单）
  • 病历本 / 检查报告

  Step 3 📮 提交理赔
  ─────────────────
  • 线上APP提交 或 邮寄纸质材料
  • 保留所有材料复印件

  Step 4 ⏳ 等待审核
  ─────────────────
  • 通常5-30个工作日
  • 复杂案件可能需要调查

  Step 5 💰 赔付到账
  ─────────────────
  • 审核通过后打款到指定银行卡

⚠️ 注意事项
  • 就医选择二级及以上公立医院
  • 保留所有票据原件
  • 先用医保报销，再用商业保险
EOF
      ;;
    critical)
      cat <<'EOF'
🏥 重疾险理赔流程
────────────────────────────────────────

  Step 1 📞 确诊后立即报案
  Step 2 📋 提供确诊报告+病理报告
  Step 3 📮 提交理赔申请+材料
  Step 4 ⏳ 保险公司审核 (通常5-15天)
  Step 5 💰 确诊即赔，一次性给付

💡 重疾险是"给付型"，赔的钱自由支配
EOF
      ;;
    life|accident)
      cat <<'EOF'
💀 寿险/意外险理赔流程
────────────────────────────────────────

  Step 1 📞 出险后及时报案
  Step 2 📋 提供相关证明材料
        (死亡证明/伤残鉴定/事故证明等)
  Step 3 📮 受益人提交理赔申请
  Step 4 ⏳ 保险公司审核调查
  Step 5 💰 赔付到受益人账户
EOF
      ;;
    *)
      echo "❌ 未知险种: $type (支持: medical, critical, life, accident)"
      ;;
  esac
}

cmd_term() {
  local age="${1:?用法: term <age> <coverage> <years>}"
  local coverage="${2:?请提供保额}"
  local years="${3:?请提供保障年限}"

  local age_factor premium
  if [ "$age" -lt 30 ]; then age_factor="0.8"
  elif [ "$age" -lt 40 ]; then age_factor="1.0"
  elif [ "$age" -lt 50 ]; then age_factor="1.5"
  else age_factor="2.5"; fi

  premium=$(echo "scale=0; $coverage * 0.0015 * $age_factor" | bc)
  local total
  total=$(echo "$premium * $years" | bc)

  cat <<EOF
╔══════════════════════════════════════════════════════════╗
║           💀 定期寿险方案分析
╚══════════════════════════════════════════════════════════╝

📋 方案详情
────────────────────────────────────────
  投保年龄:   ${age}岁
  保障金额:   ¥$(printf "%'.0f" "$coverage")
  保障期限:   ${years}年 (到${age}+${years}=$((age+years))岁)
  预估年保费: ¥$(printf "%'.0f" "$premium")
  缴费总计:   ¥$(printf "%'.0f" "$total")
  杠杆比:     1:$(echo "scale=0; $coverage / $total" | bc)

📊 保额建议
────────────────────────────────────────
  保额 = 年收入 × 10 + 负债总额 - 已有资产
  至少覆盖:
    • 房贷/车贷剩余金额
    • 子女教育费用 (至大学毕业)
    • 父母赡养费用 (5-10年)
    • 家庭3-5年生活费

💡 建议
  保障到子女经济独立即可 (一般到60-65岁)
  夫妻双方都应配置
  纯消费型性价比最高

⚠️  保费为估算值，实际以保险公司核保为准
EOF
}

cmd_health() {
  local age="${1:?用法: health <age> [pre_conditions]}"
  local conditions="${2:-none}"

  cat <<EOF
╔══════════════════════════════════════════════════════════╗
║           🏥 健康险方案推荐
╚══════════════════════════════════════════════════════════╝

📋 个人信息
────────────────────────────────────────
  年龄:       ${age}岁
  既往症:     $([ "$conditions" = "none" ] && echo "无" || echo "$conditions")
EOF

  if [ "$conditions" != "none" ]; then
    cat <<EOF

⚠️ 既往症影响
────────────────────────────────────────
  既往症: ${conditions}
  可能影响:
    • 百万医疗险: 可能除外承保或加费
    • 重疾险: 可能除外相关疾病或拒保
    • 意外险: 通常不受影响

  💡 建议:
    • 如实告知，不要隐瞒
    • 多家投保尝试（核保标准不同）
    • 考虑防癌医疗险（核保宽松）
    • 税优健康险（可带病投保）
EOF
  fi

  cat <<EOF

📊 推荐方案
────────────────────────────────────────

  🥇 百万医疗险 (首选)
     保额: 200万+    免赔: 1万
     保费: ~¥$(if [ "$age" -lt 30 ]; then echo "300"; elif [ "$age" -lt 40 ]; then echo "500"; elif [ "$age" -lt 50 ]; then echo "800"; else echo "1,500"; fi)/年
     特点: 住院医疗费用报销

  🥈 重疾险 (强烈推荐)
     保额: 30-50万
     保费: ~¥$(if [ "$age" -lt 30 ]; then echo "3,000"; elif [ "$age" -lt 40 ]; then echo "5,000"; elif [ "$age" -lt 50 ]; then echo "8,000"; else echo "12,000"; fi)/年
     特点: 确诊重大疾病一次性赔付

  🥉 门诊补充 (可选)
     保额: 1-2万
     保费: ~¥500-1,000/年
     特点: 覆盖门诊费用

💡 健康险购买建议
  ✅ 越早买越便宜，且核保容易通过
  ✅ 百万医疗+重疾搭配最佳
  ✅ 注意等待期（通常90-180天）
  ✅ 确认保证续保条款

⚠️  以上为通用建议，具体请咨询持牌保险经纪人
EOF
}

case "$CMD" in
  recommend) cmd_recommend "$@" ;;
  compare)   cmd_compare "$@" ;;
  calculate) cmd_calculate "$@" ;;
  claim)     cmd_claim "$@" ;;
  term)      cmd_term "$@" ;;
  health)    cmd_health "$@" ;;
  help)      show_help ;;
  *)
    echo "❌ 未知命令: $CMD"
    echo "运行 'bash insurance.sh help' 查看帮助"
    exit 1
    ;;
esac
