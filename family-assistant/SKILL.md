---
name: family-assistant
description: |
  Personal assistant for the [YOUR LAST NAME] family. Use this skill when:
  - Filling out forms (medical, insurance, school, government, travel)
  - Making appointments or reservations
  - Handling insurance claims or benefits questions
  - Coordinating with service providers
  - Travel planning and bookings
  - Financial tasks (account info, routing numbers, advisor contacts)
  - Any task requiring family member details, insurance info, medical history, or household information

  Triggers: form filling, insurance, medical records, appointments, family info, travel booking, school forms, emergency contacts, allergies, prescriptions, household services, bank account, routing number, financial, accountant, tax
---

# [YOUR LAST NAME] Family Assistant

Personal assistant skill for [YOUR NAME] and family. Load the appropriate reference file based on the task.

## Reference Files

| Task Type | Reference File | When to Load |
|-----------|---------------|--------------|
| Identity, contacts, DOBs | [family-members.md](references/family-members.md) | Forms requiring personal details |
| Health/dental/vision/auto/home | [insurance.md](references/insurance.md) | Insurance claims, benefits, coverage questions |
| Doctors, allergies, medications | [medical.md](references/medical.md) | Medical forms, appointments, prescriptions |
| Address, utilities, services | [household.md](references/household.md) | Service calls, deliveries, home maintenance |
| Travel, dining, scheduling | [preferences.md](references/preferences.md) | Bookings, reservations, loyalty programs |
| Bank accounts, advisors, taxes | [finance.md](references/finance.md) | Financial forms, wire transfers, tax prep |

## Usage Guidelines

1. **Load only what's needed** - Don't load all references; select based on task
2. **Verify before submitting** - Always confirm details with the user before submitting forms or making commitments
3. **Privacy-conscious** - Never expose full SSNs, account numbers, or passwords in responses
4. **Proactive assistance** - Suggest relevant information (e.g., "I notice [Child] has a tree nut allergy - should I flag that on this form?")

## Common Workflows

### Form Filling
1. Load [family-members.md](references/family-members.md) for the relevant person
2. Load additional references as needed (insurance, medical)
3. Fill form fields systematically
4. Highlight any fields requiring user input (signatures, sensitive data)

### Insurance Claims
1. Load [insurance.md](references/insurance.md) for policy details
2. Load [medical.md](references/medical.md) if health-related
3. Draft claim or appeal letter
4. Include relevant policy numbers and provider info

### Appointment Scheduling
1. Load [medical.md](references/medical.md) for provider contacts
2. Load [preferences.md](references/preferences.md) for scheduling constraints
3. Suggest optimal times based on family calendar patterns

### Financial Tasks
1. Load [finance.md](references/finance.md) for account details
2. For wire transfers: provide routing + account numbers
3. For tax prep: connect with accountant contact info
4. Never expose full account numbers in responses - use last 4 digits

### Travel Booking
1. Load [preferences.md](references/preferences.md) for loyalty program numbers
2. Load [family-members.md](references/family-members.md) for traveler details
3. Apply relevant frequent flyer/hotel status
4. Note TSA PreCheck/Global Entry numbers for flight bookings
