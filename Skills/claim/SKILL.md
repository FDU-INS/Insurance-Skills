---
name: claim
description: "Complete insurance and legal claims intelligence system. Trigger whenever someone needs to file, manage, negotiate, or dispute any type of claim: insurance claims, warranty claims, compensation claims, workers compensation, personal injury, property damage, or consumer rights disputes. Also triggers on phrases like \"file a claim\", \"my insurer denied me\", \"how do I get compensated\", \"they won't pay\", \"what am I entitled to\", or any scenario where someone has suffered a loss and needs to recover it."
---

# Claim — Complete Claims Intelligence System

## What This Skill Does

A claim is a demand for what you are owed. Most people leave money on the table not because
their claim is invalid but because they do not know the process, do not document correctly,
accept the first offer, or give up when they hit resistance.

Insurers, employers, and corporations have professional claims handlers whose job is to minimize
what they pay. This skill levels the playing field.

---

## Core Principle

Every claim is a negotiation. The opening offer is almost never the final offer. Documentation
is the only leverage you have. The person who documents thoroughly, responds correctly, and
understands the escalation path recovers significantly more than the person who does not.

---

## Workflow

### Step 1: Classify the Claim
```
CLAIM_TYPES = {
  "insurance": {
    "subtypes": ["home", "auto", "health", "life", "travel", "business", "liability"],
    "key_documents": ["policy", "incident_report", "photos", "receipts", "medical_records"],
    "typical_timeline": "30-45 days for standard claims, 90+ for complex"
  },
  "warranty": {
    "subtypes": ["manufacturer", "extended", "consumer_law_guarantee"],
    "key_documents": ["proof_of_purchase", "product_details", "fault_description", "repair_attempts"],
    "typical_timeline": "7-30 days depending on retailer"
  },
  "workers_compensation": {
    "subtypes": ["workplace_injury", "occupational_disease", "psychological_injury"],
    "key_documents": ["incident_report", "medical_certificates", "employer_notification", "witness_statements"],
    "typical_timeline": "7 days to lodge, weeks to months to resolve"
  },
  "personal_injury": {
    "subtypes": ["motor_vehicle", "public_liability", "medical_negligence", "slip_and_fall"],
    "key_documents": ["police_report", "medical_records", "photos", "witness_details", "income_evidence"],
    "typical_timeline": "Months to years depending on severity"
  },
  "consumer": {
    "subtypes": ["faulty_product", "service_failure", "false_advertising", "non_delivery"],
    "key_documents": ["purchase_receipt", "correspondence", "product_evidence", "loss_calculation"],
    "typical_timeline": "Days to weeks for straightforward cases"
  },
  "property_damage": {
    "subtypes": ["neighbour_damage", "contractor_damage", "vehicle_damage", "rental_damage"],
    "key_documents": ["photos", "repair_quotes", "ownership_evidence", "incident_record"],
    "typical_timeline": "14-30 days"
  }
}
```

### Step 2: Documentation Framework

Documentation is the foundation of every successful claim. Built before the claim is filed,
it determines the outcome.
```
DOCUMENTATION_SYSTEM = {
  "immediate_actions": {
    "within_24_hours": [
      "Photograph everything — damage, scene, injuries, contributing factors",
      "Write a factual account of exactly what happened while memory is fresh",
      "Collect names and contact details of all witnesses",
      "Preserve all physical evidence — damaged items, defective products",
      "Seek medical attention if injury involved — creates official record"
    ],
    "principle": "Evidence degrades. Memory fades. Document now, not later."
  },

  "evidence_quality_rules": [
    "Photographs: multiple angles, include reference objects for scale",
    "Written account: factual only, no speculation, no admission of fault",
    "Receipts: for damaged items, medical costs, repair costs, alternative accommodation",
    "Correspondence: keep every email, letter, and text. Screenshot chat messages.",
    "Timeline: chronological record of every contact with insurer/company"
  ],

  "what_not_to_say": [
    "Never say: 'I think it was my fault' — even partial statements affect outcomes",
    "Never say: 'I feel fine' — injuries often manifest hours or days later",
    "Never say: 'It was only minor' — minimizing language is used against you",
    "Never give recorded statements without understanding your rights first"
  ]
}
```

### Step 3: Filing the Claim
```
CLAIM_FILING_FRAMEWORK = {
  "before_filing": {
    "checklist": [
      "Read your policy or warranty terms — know exactly what is covered",
      "Calculate your total loss including consequential costs",
      "Organize all documentation",
      "Understand the deadline — claims have strict time limits",
      "Know your excess/deductible amount"
    ]
  },

  "claim_letter_structure": {
    "opening":     "State the nature of claim, date of incident, policy/order number",
    "facts":       "Factual chronological account of what happened",
    "loss":        "Specific itemized list of losses with dollar amounts and evidence",
    "entitlement": "Reference to specific policy clause or consumer law that entitles you",
    "demand":      "Specific amount or remedy requested with deadline for response",
    "closing":     "Contact details and statement of next steps if unresolved"
  },

  "claim_letter_template": {
    "subject": "Formal Claim — [Policy/Order Number] — [Date of Incident]",
    "body": [
      "I am writing to lodge a formal claim under [policy number / consumer guarantee law].",
      "On [date], [factual description of incident].",
      "As a result, I have suffered the following losses: [itemized list with amounts].",
      "Under [specific clause / statutory right], I am entitled to [remedy].",
      "I request [specific resolution] by [date 14 days from now].",
      "I have attached supporting documentation including [list evidence].",
      "If this matter is not resolved by [date], I will escalate to [regulator/tribunal]."
    ]
  }
}
```

### Step 4: Negotiating the Settlement
```
NEGOTIATION_SYSTEM = {
  "opening_offer_rules": {
    "principle":   "The first offer is almost never the best offer",
    "response":    "Never accept or reject immediately. Ask for the basis of the calculation.",
    "ask":         "Please provide a written explanation of how this figure was calculated",
    "counter":     "Base counter on documented evidence, not emotion"
  },

  "negotiation_tactics": {
    "anchoring":        "State your full documented loss first before any offer is made",
    "silence":          "After stating your position, stop talking. Silence creates pressure.",
    "written_record":   "Confirm every offer and counter-offer in writing via email",
    "deadline":         "Set reasonable deadlines — open-ended negotiations stall indefinitely",
    "splitting":        "When offered a split, calculate whether splitting from your number or theirs"
  },

  "lowball_response_script": {
    "situation": "Insurer offers significantly less than claimed",
    "response":  "Thank you for your response. I have reviewed the offer and it does not
                  reflect my documented losses. My claim is based on [specific evidence].
                  The replacement cost of [item] is [amount] as evidenced by [quote/receipt].
                  I am prepared to accept [counter amount] in full settlement. Please confirm
                  your position in writing by [date]."
  }
}
```

### Step 5: Escalation Path
```
ESCALATION_LADDER = {
  "level_1": {
    "action":    "Formal written complaint to company complaints department",
    "timeline":  "Allow 14 days for response",
    "output":    "Written record of complaint and company's response"
  },
  "level_2": {
    "action":    "External dispute resolution — ombudsman, insurance regulator, consumer tribunal",
    "when":      "Company has rejected claim or failed to respond within reasonable time",
    "cost":      "Usually free for consumers",
    "leverage":  "Companies settle more readily when external body is involved"
  },
  "level_3": {
    "action":    "Legal proceedings — small claims tribunal, civil court",
    "when":      "Amount justifies legal cost and external resolution failed",
    "threshold": "Most small claims tribunals handle amounts up to $10,000-$25,000"
  },

  "escalation_letter_trigger": "I note that my claim has not been resolved. If I do not
    receive a satisfactory response by [date], I will lodge a complaint with [regulator name]
    and pursue the matter through [tribunal name] without further notice."
}
```

---

## Claim-Specific Guidance

### Insurance Claim Specifics
```
INSURANCE_RULES = {
  "report_promptly":    "Most policies require notification within specific timeframes",
  "mitigate_loss":      "Take reasonable steps to prevent further damage — document everything you do",
  "independent_quote":  "Get your own repair quotes — do not rely solely on insurer's assessors",
  "total_loss":         "If item is totaled, research replacement cost not depreciated value",
  "denied_claim":       "Request denial in writing with specific policy clause cited"
}
```

### Workers Compensation Specifics
```
WORKERS_COMP_RULES = {
  "report_immediately": "Notify employer in writing on the day of injury or as soon as possible",
  "medical_certificate": "Obtain WorkCover/workers comp certificate from treating doctor",
  "suitable_duties":    "Understand your right to suitable duties during recovery",
  "weekly_payments":    "You are entitled to a percentage of pre-injury earnings during incapacity",
  "common_law":         "Serious injuries may entitle you to common law damages — seek legal advice"
}
```

---

## Quality Check Before Delivering

- [ ] Claim type correctly identified
- [ ] Time limits flagged — claims expire
- [ ] Documentation checklist provided for this specific claim type
- [ ] Escalation path clear
- [ ] Jurisdiction noted — claim processes vary by location
- [ ] Legal advice recommended for complex, high-value, or injury claims
