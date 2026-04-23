# TravelHealthTracker Schema

旅行健康追踪的完整数据结构定义。

## 字段速查

### 核心字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `trips` | array | 旅行计划 |
| `vaccinations` | array | 疫苗接种记录 |
| `travel_kit` | object | 旅行药箱 |
| `medications` | array | 旅行用药 |
| `insurance` | array | 保险信息 |
| `emergency_contacts` | array | 紧急联系人 |
| `emergency_card` | object | 紧急卡片 |
| `health_checks` | array | 健康检查 |

## trips 数组项

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `trip_id` | string | 旅行ID |
| `destination` | array | 目的地列表 |
| `start_date` | string | 开始日期 |
| `end_date` | string | 结束日期 |
| `duration_days` | integer | 天数 |
| `travel_type` | enum | business/tourism/volunteer/education/family_visit/other |
| `risk_assessment` | object | 风险评估 |
| `status` | enum | planning/in_progress/completed/cancelled |
| `preparedness_score` | integer | 准备度评分 (0-100) |

### risk_assessment 对象

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `overall_risk` | enum | low/medium/high/very_high |
| `vaccinations_needed` | array | 需要的疫苗 |
| `medications_recommended` | array | 推荐药物 |
| `health_advisories` | array | 健康建议 |
| `current_alerts` | array | 当前疫情预警 |

## vaccinations 数组项

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `vaccine_type` | enum | 疫苗类型 |
| `date_administered` | string | 接种日期 |
| `status` | enum | scheduled/completed/missed |
| `next_dose_date` | string | 下剂接种日期 |

### vaccine_type 枚举值

| 疫苗 | 说明 |
|-----|------|
| hepatitis_a | 甲型肝炎疫苗 |
| hepatitis_b | 乙型肝炎疫苗 |
| typhoid | 伤寒疫苗 |
| yellow_fever | 黄热病疫苗 |
| japanese_encephalitis | 日本脑炎疫苗 |
| rabies | 狂犬病疫苗 |
| meningococcal | 脑膜炎球菌疫苗 |
| cholera | 霍乱疫苗 |

## travel_kit 对象

### medications（药品）
| 名称 | 类别 |
|-----|------|
| antidiarrheal | 止泻药 |
| pain_reliever | 退烧止痛药 |
| antihistamine | 抗过敏药 |
| motion_sickness | 晕车药 |
| antacid | 抗酸药 |

### medical_supplies（医疗用品）
| 名称 |
|-----|
| bandages | 绷带 |
| antiseptic_wipes | 消毒纸巾 |
| thermometer | 体温计 |
| tweezers | 镊子子 |
| scissors | 剪刀 |

### protection_items（防护用品）
| 名称 |
|-----|
| sunscreen | 防晒霜 |
| insect_repellent | 驱蚊剂 |
| mosquito_coil | 蚊香 |
| hand_sanitizer | 免洗洗手液 |

## medications 数组项

| 字段 | 说明 |
|-----|------|
| `medication_id` | 药物ID |
| `name` | 药品名称 |
| `dosage` | 剂量 |
| `frequency` | 用法频率 |
| `start_date` | 开始日期 |
| `end_date` | 结束日期 |
| `purpose` | 用途 |
| `trip_id` | 关联旅行ID |

## insurance 数组项

| 字段 | 说明 |
|-----|------|
| `policy_id` | 保单ID |
| `policy_number` | 保单号 |
| `coverage_amount` | 保额 |
| `covers_medical_evacuation` | 是否覆盖医疗转运 |
| `emergency_contact` | 紧急联系电话 |

## emergency_contacts 数组项

| 字段 | 说明 |
|-----|------|
| `name` | 姓名 |
| `relationship` | 关系（配偶、父母等） |
| `phone` | 电话 |
| `email` | 邮箱 |

## emergency_card 对象

| 字段 | 说明 |
|-----|------|
| `languages` | 支持语言（en/zh/ja/ko/fr/es/th/vi） |
| `medical_conditions` | 疾病状况 |
| `allergies` | 过敏 |
| `medications` | 正在用药 |
| `blood_type` | 血型 |
| `emergency_contacts` | 紧急联系人列表 |

## health_checks 数组项

| 字段 | 说明 |
|-----|------|
| `check_type` | pre_trip/post_trip/follow_up |
| `date` | 检查日期 |
| `findings` | 检查发现 |
| `recommendations` | 建议 |

## 数据存储

- 位置: `data/travel-health-tracker.json`
