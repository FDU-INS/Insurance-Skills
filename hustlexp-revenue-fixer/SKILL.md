---
name: hustlexp-revenue-fixer
description: Use when fixing HustleXP revenue collection bugs including Stripe platform fee not being collected (application_fee_amount missing), escrow fee miscalculation using task.price instead of escrow.amount, self-insurance pool never funded, tip platform cut absent, subscription renewal revenue not logged, or XP tax path unreachable. Covers all platform fee issues and financial invariant checks.
---

# HustleXP Revenue Fixer Runbook

## Financial Invariants — Check BEFORE and AFTER every fix

- **INV-1**: Escrow state machine — PENDING → FUNDED → RELEASED/REFUNDED/DISPUTED only. Never skip states.
- **INV-2**: `payouts_enabled` AND `stripe_connect_id` must be verified before any escrow release.
- **INV-3**: `application_fee_amount` must ALWAYS be set on PaymentIntent creation. If it is absent, platform earns $0.
- **INV-4**: Fee calculations must use `escrow.amount` (task price + surge), never bare `task.price`.

---

## Bug Inventory and Fixes (dependency-safe order)

### P0 Bug 1 — application_fee_amount never passed (HIGHEST URGENCY)

**File**: `backend/src/services/StripeService.ts` — line 162 is the fee calculation; the `stripe.paymentIntents.create(...)` call starts at line 164.
**Problem**: Platform fee is stored in PaymentIntent metadata only. `application_fee_amount` is never passed to the Stripe API. Platform earns $0 in platform fees.
**Fix**: Inside the `stripe.paymentIntents.create(...)` params (lines 164–174), add:

```typescript
application_fee_amount: Math.round(amount * (config.stripe.platformFeePercent / 100)),
```

Note: `amount` is already in cents. Fee percent comes from `config.stripe.platformFeePercent`. Do NOT use hardcoded `taskPrice * 0.15 * 100`.
**Verification**: Stripe dashboard → Payments → filter by connected account → confirm platform fee shown on each charge.

---

### P0 Bug 2 — Escrow fee calculation uses wrong amount

**File**: `backend/src/services/EscrowService.ts` line 337
**Problem**: `grossPayoutCents = task.price` — this misses the surge premium. Surge is applied to `escrow.amount`, not base `task.price`.
**Fix**: Change `task.price` to `escrow.amount` on line 337.
**Verification**: Create a surged task; confirm platform fee includes surge premium in the payout record.

---

### P1 Bug 3 — Self-insurance pool never funded

**File**: `backend/src/services/EscrowService.ts` — inside `release()` method
**Problem**: `SelfInsurancePoolService.recordContribution()` exists but is never called. Pool is permanently $0.
**Fix**: Add after every successful escrow release. Actual signature: `recordContribution(taskId: string, hustlerId: string, contributionCents: number, contributionPercentage?: number)`. Contribution rate is 2%:

```typescript
const insuranceContributionCents = Math.round(grossPayoutCents * 0.02);
await SelfInsurancePoolService.recordContribution(
  escrow.task_id,
  workerId,
  insuranceContributionCents,
);
```

**Verification**: Check `insurance_contributions` table after a test escrow release — row must appear.

---

### P1 Bug 4 — Tips earn $0 and cost Stripe fees

**File**: `backend/src/services/TippingService.ts` line 98
**Problem**: Tips have no platform cut. Platform pays Stripe processing fees on tips with zero offsetting revenue.
**Fix**: Add 5–8% platform cut on tips.
**LEGAL REQUIREMENT**: After changing tip fee percentage, update fee disclosure sections in both:

- Poster Agreement
- Hustler Agreement
  Use the `legal-document-manager` skill for those updates. Do NOT ship this fix without the legal doc update.

---

### P1 Bug 5 — Subscription renewal revenue not logged

**File**: `backend/src/jobs/stripe-event-worker.ts`
**Problem**: The `invoice.paid` Stripe webhook event is not handled for recurring subscriptions. Only month-1 revenue is logged; all renewal revenue is silently lost. The switch in `stripe-event-worker.ts` handles `invoice.payment_failed` but NOT `invoice.paid`.
**Fix**: Add a `case 'invoice.paid':` handler in `backend/src/jobs/stripe-event-worker.ts` to log renewal revenue.
**Verification**: Trigger a test subscription renewal via Stripe CLI and confirm revenue row is created.

---

### P1 Bug 6 — XP tax path unreachable

**File**: `backend/src/services/EscrowService.ts` line 336
**Problem**: `paymentMethod` is hardcoded to `'escrow'`, making the XP tax branch unreachable for any other payment method.
**Fix**: Derive `paymentMethod` from task metadata instead of hardcoding.

---

## Fix Order (dependency-safe)

1. StripeService.ts:162 — `application_fee_amount` (P0, zero dependencies, do first)
2. EscrowService.ts:337 — `escrow.amount` vs `task.price` (P0, understand escrow model first)
3. EscrowService.ts release() — self-insurance pool call (additive, low risk)
4. TippingService.ts:98 — tip platform cut + legal docs (requires legal-document-manager skill)
5. `stripe-event-worker.ts` — add `case 'invoice.paid':` handler
6. EscrowService.ts:336 — XP tax path (`paymentMethod` hardcoded)

---

## Test Sequence After All Fixes

```bash
cd /Users/sebastiandysart/Desktop/hustlexp-ai-backend
npx vitest run --coverage 2>&1 | tail -20
```

Must show: **0 failures** and **coverage ≥ 88.88%** (backend testScore threshold to keep ecosystem health at 100/100).

---

## Key Project Paths

- Backend: `/Users/sebastiandysart/Desktop/hustlexp-ai-backend`
- StripeService: `backend/src/services/StripeService.ts`
- EscrowService: `backend/src/services/EscrowService.ts`
- TippingService: `backend/src/services/TippingService.ts`

## Key File Locations

- Stripe webhook ingestion: `backend/src/services/StripeWebhookService.ts`
- Stripe event dispatcher: `backend/src/jobs/stripe-event-worker.ts` (add new handlers here)
- SelfInsurancePoolService: `backend/src/services/SelfInsurancePoolService.ts` (2% contribution rate)
