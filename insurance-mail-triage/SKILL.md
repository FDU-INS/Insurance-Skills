---
name: insurance-mail-triage
description: Triage long email threads for an insurance context, identify the most recent actionable message, extract key context, infer intent (e.g., missing documents, follow-up/reminder, payment, status), and decide whether to reply or take further action.
---

# Skill Overview

## When to use
Use this skill when you receive a single pasted document containing one or more emails/letters/messages (often with quoted history/forwards) and you must determine the most important and most recent content, the sender’s intent, and whether the insurer should reply or take further action.

## 4-step process

### Step 1 — Extract the message to act on
Treat the **top-most non-quoted** block as the most recent message (unless the thread clearly states otherwise). Many pasted threads place the latest reply at the top, with older content below.

Extract (if available) and keep the original language:
- Sender (name/email)
- Receiver(s) (email addresses if present)
- Date
- Subject
- 1–3 bullets: what the message says

### Step 2 — Keep only essential history (max 3 facts)
Scan older quoted messages only to determine what is **pending** and who owes what.
Keep up to 3 facts, such as:
- “Insurer requested invoice and photos on <date>; still missing.”
- “Sender claims prior email remained unanswered.”
- “Payment requested; bank details provided in older email.”

Do not summarize the entire history.

### Step 3 — Classify intent
Choose 1 primary intent based on the most recent message (use history only to disambiguate):
- Status update request
- Provide documents / evidence
- Request for payment / reimbursement
- Complaint / dispute / liability disagreement
- Appointment / expertise coordination
- Closure confirmation
- Follow-up / reminder (chasing a response)
- Other (state in one short sentence)

### Step 4 — Decide whether it’s a reminder or whether the company needs to take action
Mark as a YES when the most recent message matches one of these conditions:
- Requests a response to a previous email/letter.
- Follow-up on an unanswered email.
- Reminder of a previous reminder.
- Follow-up on an unpaid invoice/payment.
- Follow-up by sending complementary documents to an unanswered email.
- Follow-up on a past request.

Mark as a NO when:
- The sender is following up with **their** insured/principal/third party (not the insurer).
- They send a document/invoice **for the first time** with no chase language.
- They are only informing they closed their file without asking you to act.

## Typical YES OR NO examples

### Example 1 — YES: “no news for some time”
- **Email:** “For some time now, we have not heard from you. Could you inform us by 05/02/2024 of the current status of this file?”
- Classification: Yes (Reminder).
- Why: They explicitly state they have not heard back and request an update by a deadline.

### Example 2 — YES: “our letter remained unanswered”
- **Email:** “We are contacting you again regarding the above-mentioned matter. Unless we are mistaken, our letter has remained unanswered.”
- Classification: Yes (Reminder).
- Why: Explicit follow-up on an unanswered letter.

### Example 3 — NO: they follow up with their principal
- **Email:** “We allow ourselves to return to this matter. We are waiting for the confirmation of the guarantees and responsibility of our principal. We are following up with our principal.”
- Classification: No (Not a reminder).
- Why: The follow-up action is directed at their own principal, not the insurer receiving the email.

### Example 4 — NO: they remind their insured (not you)
- **Email:** “We are making a final reminder to our insured to obtain their statement.”
- Classification: No (Not a reminder).
- Why: The reminder is addressed to their insured, not to the insurer team.

### Example 5 — YES: Reminder of a reminder
- **Email:** “Unless we are mistaken, our reminder of 16/12/2023 has remained unanswered.”
- Classification: Yes (Reminder).
- Why: They explicitly reference a prior reminder that received no response.


# Output Format (STRICT)

Return **ONLY** a valid JSON object (no Markdown, no extra text). Use double quotes for all keys and string values, and do not add extra keys.

{
  "message": "Your analysis and extracted message here.",
  "label": "YES or NO"
}