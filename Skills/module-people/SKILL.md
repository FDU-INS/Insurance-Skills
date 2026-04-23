---
name: module-people
description: >-
  Mega-Skill for HR, Payroll & Recruitment ERP module. Employee management,
  attendance tracking, salary calculation, social insurance, PIT, and Vietnam labor law.
metadata:
  author: VCT Platform
  version: "1.0.0"
  type: "Mega-Skill"
  locale: vi-VN
---

# MODULE-PEOPLE — MEGA-SKILL

> Domain expertise cho module Nhân sự, Chấm công & Tuyển dụng.

---

## 🔹 NĂNG LỰC: HR MANAGEMENT

### Employee Lifecycle
```
Recruitment → Onboarding → Active → [Promotion/Transfer] → Offboarding → Alumni

Data Model:
├── employees: Core info (name, DOB, ID card, tax code)
├── departments: Org structure
├── positions: Job titles, grades
├── employment_contracts: Contract type, dates, salary
├── employee_documents: ID, certs, degrees
└── employee_history: Position changes, salary adjustments
```

### Organization Structure
```
VCT Group
├── Ban Giám đốc
├── Phòng Kỹ thuật (Engineering)
├── Phòng Kinh doanh (Sales)
├── Phòng Marketing
├── Phòng Tài chính - Kế toán
├── Phòng Nhân sự
└── Phòng Hành chính
```

### Vietnam Labor Law Compliance
```
├── Hợp đồng lao động: Thử việc / Xác định thời hạn / Không xác định
├── Thời gian làm việc: 8h/ngày, 48h/tuần (tiêu chuẩn)
├── Nghỉ phép: 12 ngày/năm (tối thiểu), +1 ngày/5 năm
├── Nghỉ lễ: 11 ngày/năm (theo quy định)
├── Thai sản: 6 tháng (nữ), 5-14 ngày (nam)
├── Thử việc: 60 ngày (ĐH+), 30 ngày (CĐ/TC), 6 ngày (khác)
└── Thông báo nghỉ việc: 45 ngày (HĐKXĐTH), 30 ngày (HĐXĐTH)
```

---

## 🔹 NĂNG LỰC: PAYROLL & ATTENDANCE

### Attendance Tracking
```
Data Model:
├── attendance_records: date, check_in, check_out, status
├── leave_requests: type, dates, status, approver
├── overtime_records: date, hours, type, approval
└── work_schedules: shift patterns, flexible hours

Status: present | absent | late | leave | holiday | overtime
Leave types: annual | sick | maternity | bereavement | unpaid
```

### Salary Calculation (Vietnam)
```
Gross Salary Structure:
├── Lương cơ bản (Base salary)
├── Phụ cấp (Allowances)
│   ├── Phụ cấp ăn trưa
│   ├── Phụ cấp xăng xe
│   ├── Phụ cấp điện thoại
│   └── Phụ cấp chức vụ
├── Thưởng (Bonus)
├── Làm thêm giờ (Overtime)
│   ├── Ngày thường: 150%
│   ├── Ngày nghỉ: 200%
│   └── Ngày lễ: 300%
└── Các khoản khác

Deductions:
├── BHXH (Social Insurance): 8% (employee) + 17.5% (employer)
├── BHYT (Health Insurance): 1.5% (employee) + 3% (employer)
├── BHTN (Unemployment Insurance): 1% (employee) + 1% (employer)
├── KPCĐ (Union fee): 1% (employee) + 2% (employer)
└── Thuế TNCN (PIT)

Net Salary = Gross - BHXH - BHYT - BHTN - KPCĐ - PIT
```

### Personal Income Tax (PIT) Calculation
```
Thuế TNCN theo biểu lũy tiến:
Thu nhập chịu thuế = Gross - BHXH - BHYT - BHTN - Giảm trừ

Giảm trừ:
├── Bản thân: 11.000.000 VND/tháng
└── Người phụ thuộc: 4.400.000 VND/người/tháng

Biểu thuế lũy tiến:
| Bậc | Thu nhập chịu thuế (triệu) | Thuế suất |
|-----|---------------------------|----------|
| 1   | ≤ 5                       | 5%       |
| 2   | 5 - 10                    | 10%      |
| 3   | 10 - 18                   | 15%      |
| 4   | 18 - 32                   | 20%      |
| 5   | 32 - 52                   | 25%      |
| 6   | 52 - 80                   | 30%      |
| 7   | > 80                      | 35%      |
```

### Payroll → Finance Integration
```
Bút toán lương tháng:
Nợ 6421 (CP nhân viên QL)     [Gross + Employer contributions]
    Có 334 (Phải trả NLĐ)                [Net salary]
    Có 3383 (BHXH phải nộp)              [BHXH employee + employer]
    Có 3384 (BHYT phải nộp)              [BHYT employee + employer]
    Có 3386 (BHTN phải nộp)              [BHTN employee + employer]
    Có 3335 (Thuế TNCN)                  [PIT amount]

→ Creates journal_entry via Finance module API
```

---

## 🔹 NĂNG LỰC: RECRUITMENT

### Recruitment Pipeline
```
Stages:
├── 1. Job Opening (approved by manager)
├── 2. Job Posting (internal + external channels)
├── 3. Application Receipt (CV screening)
├── 4. Phone Screen (HR initial filter)
├── 5. Technical Interview (hiring manager)
├── 6. Culture Fit Interview (team)
├── 7. Offer (salary negotiation)
├── 8. Acceptance → Onboarding
└── 9. Rejection → Candidate pool

Data Model:
├── job_openings: department, position, requirements, status
├── candidates: name, contact, resume_url, source
├── applications: candidate + opening + stage + feedback
├── interviews: schedule, interviewers, scores, notes
└── offers: salary, start_date, status
```

### Onboarding Checklist
```
Day 0 (Before start):
├── [ ] Employment contract signed
├── [ ] IT equipment prepared
├── [ ] Email/accounts created
├── [ ] Desk/workspace ready
└── [ ] Welcome kit prepared

Week 1:
├── [ ] Company orientation
├── [ ] Team introduction
├── [ ] System access setup
├── [ ] Initial training plan
└── [ ] Buddy assigned

Month 1-3 (Probation):
├── [ ] 30-day check-in
├── [ ] 60-day review
├── [ ] Probation evaluation
└── [ ] Confirmation or extension
```

---

## Trigger Patterns

- "nhân sự", "HR", "employee", "nhân viên"
- "lương", "payroll", "salary", "chấm công"
- "tuyển dụng", "recruitment", "hiring"
- "nghỉ phép", "leave", "attendance"
- "BHXH", "bảo hiểm", "thuế TNCN", "PIT"

## [V11 SINGULARITY] (Ultimate Capability Upgrades)
- **P2P_SYNC:** Upon completing any API/DB change, you MUST emit a JSON schema to `d:\VCT PLATFORM\api-contracts\` so other agents can RAG it.
- **SELF_HEALING (3-STRIKES):** If `vct.cmd complete` (Docker Test) fails 3 times, you MUST run `git reset --hard`, mark the task as "FAILED", and cease execution. Do NOT loop infinitely.
- **TELEMETRY_SCHEMA:** You must push your thought logs to `d:\VCT PLATFORM\vct-dashboard\public\.telemetry.json` strictly as a JSON Object `{ "agent": "name", "action": "...", "status": "..." }`.
