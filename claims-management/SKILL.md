---
name: guidewire-core-workflow-b
description: |
  Execute Guidewire secondary workflow: Claims processing in ClaimCenter.
  Use when implementing FNOL, claim investigation, reserves, payments, and settlement.
  Trigger with phrases like "claimcenter workflow", "create claim", "file fnol",
  "process claim", "claim settlement", "claim payment".
allowed-tools: Read, Write, Edit, Bash(curl:*), Bash(npm:*), Grep
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# Guidewire Core Workflow B: Claims Processing

## Overview

Master the complete claims lifecycle in ClaimCenter: First Notice of Loss (FNOL), claim investigation, reserve setting, payments, and settlement.

## Prerequisites

- Completed `guidewire-install-auth` and `guidewire-core-workflow-a`
- Understanding of claims handling processes
- Valid API credentials with claims admin permissions

## Claims Lifecycle States

```
FNOL → Open → Investigation → Evaluation → Negotiation → Settlement → Closed
  |      |          |              |             |            |          |
  v      v          v              v             v            v          v
[Draft] [Open]  [Reserve]    [Exposure]   [Payment]   [Settle]   [Closed]
```

## Instructions

### Step 1: Create FNOL (First Notice of Loss)

```typescript
// Create a new claim via FNOL
interface FNOLRequest {
  data: {
    attributes: {
      lossDate: string;
      lossTime?: string;
      reportedDate: string;
      lossType: { code: string };
      lossCause: { code: string };
      description: string;
      policyNumber: string;
      lossLocation?: {
        addressLine1: string;
        city: string;
        state: { code: string };
        postalCode: string;
      };
      reporter?: {
        firstName: string;
        lastName: string;
        primaryPhone: string;
        relationship: { code: string };
      };
    };
  };
}

async function createFNOL(fnolData: FNOLData): Promise<Claim> {
  const request: FNOLRequest = {
    data: {
      attributes: {
        lossDate: fnolData.lossDate,
        lossTime: fnolData.lossTime,
        reportedDate: new Date().toISOString().split('T')[0],
        lossType: { code: fnolData.lossType }, // 'AUTO', 'PR', 'GL', 'WC'
        lossCause: { code: fnolData.lossCause },
        description: fnolData.description,
        policyNumber: fnolData.policyNumber,
        lossLocation: {
          addressLine1: fnolData.location.address,
          city: fnolData.location.city,
          state: { code: fnolData.location.state },
          postalCode: fnolData.location.zip
        },
        reporter: {
          firstName: fnolData.reporter.firstName,
          lastName: fnolData.reporter.lastName,
          primaryPhone: fnolData.reporter.phone,
          relationship: { code: 'insured' }
        }
      }
    }
  };

  const response = await claimCenterClient.request<{ data: Claim }>(
    'POST',
    '/fnol/v1/fnol',
    request
  );

  console.log(`Created claim: ${response.data.claimNumber}`);
  return response.data;
}
```

### Step 2: Add Exposures

```typescript
// Add exposures (coverages that may apply)
interface ExposureRequest {
  data: {
    attributes: {
      exposureType: { code: string };
      lossParty: { code: string };
      primaryCoverage: { code: string };
      claimant?: { id: string };
      incident?: { id: string };
    };
  };
}

async function addExposure(
  claimId: string,
  exposureData: ExposureData
): Promise<Exposure> {
  const request: ExposureRequest = {
    data: {
      attributes: {
        exposureType: { code: exposureData.type }, // 'VehicleDamage', 'BodilyInjury', etc.
        lossParty: { code: exposureData.lossParty }, // 'insured', 'claimant'
        primaryCoverage: { code: exposureData.coverageCode },
        claimant: exposureData.claimantId ? { id: exposureData.claimantId } : undefined
      }
    }
  };

  const response = await claimCenterClient.request<{ data: Exposure }>(
    'POST',
    `/claim/v1/claims/${claimId}/exposures`,
    request
  );

  return response.data;
}
```

### Step 3: Add Incidents

```typescript
// Add vehicle incident for auto claims
interface VehicleIncidentRequest {
  data: {
    attributes: {
      severity: { code: string };
      description: string;
      vehicle: {
        vin?: string;
        year: number;
        make: string;
        model: string;
        color?: string;
        licensePlate?: string;
      };
      damageDescription: string;
      airbagDeployed?: boolean;
      vehicleOperable?: boolean;
    };
  };
}

async function addVehicleIncident(
  claimId: string,
  vehicleData: VehicleIncidentData
): Promise<VehicleIncident> {
  const request: VehicleIncidentRequest = {
    data: {
      attributes: {
        severity: { code: vehicleData.severity }, // 'minor', 'moderate', 'major', 'total-loss'
        description: vehicleData.description,
        vehicle: {
          vin: vehicleData.vin,
          year: vehicleData.year,
          make: vehicleData.make,
          model: vehicleData.model,
          licensePlate: vehicleData.licensePlate
        },
        damageDescription: vehicleData.damageDescription,
        airbagDeployed: vehicleData.airbagDeployed,
        vehicleOperable: vehicleData.vehicleOperable
      }
    }
  };

  const response = await claimCenterClient.request<{ data: VehicleIncident }>(
    'POST',
    `/claim/v1/claims/${claimId}/vehicle-incidents`,
    request
  );

  return response.data;
}
```

### Step 4: Set Reserves

```typescript
// Set reserve on exposure
interface ReserveRequest {
  data: {
    attributes: {
      reserveLine: { code: string };
      costType: { code: string };
      costCategory: { code: string };
      newAmount: { amount: number; currency: string };
      comments: string;
    };
  };
}

async function setReserve(
  claimId: string,
  exposureId: string,
  reserveData: ReserveData
): Promise<Reserve> {
  const request: ReserveRequest = {
    data: {
      attributes: {
        reserveLine: { code: reserveData.reserveLine }, // 'indemnity', 'expenses'
        costType: { code: reserveData.costType },
        costCategory: { code: reserveData.costCategory },
        newAmount: {
          amount: reserveData.amount,
          currency: 'usd'
        },
        comments: reserveData.comments
      }
    }
  };

  const response = await claimCenterClient.request<{ data: Reserve }>(
    'POST',
    `/claim/v1/claims/${claimId}/exposures/${exposureId}/reserves`,
    request
  );

  console.log(`Set reserve: $${reserveData.amount} on exposure ${exposureId}`);
  return response.data;
}
```

### Step 5: Create Payment

```typescript
// Create claim payment
interface PaymentRequest {
  data: {
    attributes: {
      paymentType: { code: string };
      exposure: { id: string };
      payee: {
        payeeType: { code: string };
        claimContact?: { id: string };
        payeeName?: string;
      };
      reserveLine: { code: string };
      costType: { code: string };
      costCategory: { code: string };
      amount: { amount: number; currency: string };
      comments?: string;
      paymentMethod?: { code: string };
    };
  };
}

async function createPayment(
  claimId: string,
  paymentData: PaymentData
): Promise<Payment> {
  const request: PaymentRequest = {
    data: {
      attributes: {
        paymentType: { code: paymentData.paymentType }, // 'partial', 'final'
        exposure: { id: paymentData.exposureId },
        payee: {
          payeeType: { code: paymentData.payeeType },
          claimContact: paymentData.claimContactId
            ? { id: paymentData.claimContactId }
            : undefined
        },
        reserveLine: { code: 'indemnity' },
        costType: { code: paymentData.costType },
        costCategory: { code: paymentData.costCategory },
        amount: { amount: paymentData.amount, currency: 'usd' },
        comments: paymentData.comments,
        paymentMethod: { code: paymentData.method || 'check' }
      }
    }
  };

  const response = await claimCenterClient.request<{ data: Payment }>(
    'POST',
    `/claim/v1/claims/${claimId}/payments`,
    request
  );

  console.log(`Created payment: $${paymentData.amount} - Check #${response.data.checkNumber}`);
  return response.data;
}
```

### Step 6: Close Exposure

```typescript
// Close exposure after settlement
async function closeExposure(
  claimId: string,
  exposureId: string,
  outcome: string
): Promise<Exposure> {
  const response = await claimCenterClient.request<{ data: Exposure }>(
    'POST',
    `/claim/v1/claims/${claimId}/exposures/${exposureId}/close`,
    {
      data: {
        attributes: {
          closedOutcome: { code: outcome } // 'completed', 'denied', 'duplicate'
        }
      }
    }
  );

  return response.data;
}
```

### Step 7: Close Claim

```typescript
// Close claim when all exposures are closed
async function closeClaim(claimId: string): Promise<Claim> {
  const response = await claimCenterClient.request<{ data: Claim }>(
    'POST',
    `/claim/v1/claims/${claimId}/close`,
    {
      data: {
        attributes: {
          closedOutcome: { code: 'completed' }
        }
      }
    }
  );

  console.log(`Closed claim: ${response.data.claimNumber}`);
  return response.data;
}
```

## Gosu Implementation

```gosu
// Complete claims workflow in Gosu
package gw.custom.claim

uses gw.api.util.Logger
uses gw.cc.claim.Claim
uses gw.cc.exposure.Exposure
uses gw.transaction.Transaction

class ClaimWorkflow {
  private static final var LOG = Logger.forCategory("ClaimWorkflow")

  static function createClaim(
    policyNumber : String,
    lossDate : Date,
    lossType : LossType,
    description : String
  ) : Claim {

    return Transaction.runWithNewBundle(\bundle -> {
      // Find policy
      var policy = findPolicy(policyNumber)
      if (policy == null) {
        throw new IllegalArgumentException("Policy not found: ${policyNumber}")
      }

      // Create claim
      var claim = new Claim(bundle)
      claim.Policy = policy
      claim.LossDate = lossDate
      claim.LossType = lossType
      claim.Description = description
      claim.ReportedDate = Date.Today
      claim.LossCause = LossCause.TC_VEHCOLLISION

      // Set claim to open
      claim.open()

      LOG.info("Created claim: ${claim.ClaimNumber}")
      return claim
    })
  }

  static function addVehicleExposure(
    claim : Claim,
    vehicle : Vehicle,
    coverageCode : String
  ) : Exposure {

    return Transaction.runWithNewBundle(\bundle -> {
      var claim = bundle.add(claim)

      // Create vehicle incident
      var incident = new VehicleIncident(bundle)
      incident.Claim = claim
      incident.Vehicle = vehicle
      incident.Description = "Vehicle damage from ${claim.LossCause.DisplayName}"

      // Create exposure
      var exposure = new Exposure(bundle)
      exposure.Claim = claim
      exposure.ExposureType = ExposureType.TC_VEHICLEDAMAGE
      exposure.LossParty = LossPartyType.TC_INSURED
      exposure.PrimaryCoverage = CoverageType.get(coverageCode)
      exposure.VehicleIncident = incident

      LOG.info("Created exposure: ${exposure.ExposureType.DisplayName}")
      return exposure
    })
  }

  static function setExposureReserve(
    exposure : Exposure,
    amount : java.math.BigDecimal,
    reserveLine : ReserveLine
  ) {
    Transaction.runWithNewBundle(\bundle -> {
      var exp = bundle.add(exposure)

      var reserve = new Reserve(bundle)
      reserve.Exposure = exp
      reserve.ReserveLine = reserveLine
      reserve.CostType = CostType.TC_CLAIMCOST
      reserve.CostCategory = CostCategory.TC_BODY
      reserve.NewAmount = new gw.api.financials.CurrencyAmount(amount, Currency.TC_USD)
      reserve.Comments = "Initial reserve set"

      LOG.info("Set reserve: ${amount} on ${exp.ExposureType.DisplayName}")
    })
  }

  static function createPayment(
    exposure : Exposure,
    amount : java.math.BigDecimal,
    payee : Contact,
    paymentType : PaymentType
  ) : Payment {

    return Transaction.runWithNewBundle(\bundle -> {
      var exp = bundle.add(exposure)

      var payment = new Payment(bundle)
      payment.Exposure = exp
      payment.Claim = exp.Claim
      payment.PaymentType = paymentType
      payment.ReserveLine = ReserveLine.TC_INDEMNITY
      payment.CostType = CostType.TC_CLAIMCOST
      payment.CostCategory = CostCategory.TC_BODY
      payment.Payee = payee
      payment.GrossAmount = new gw.api.financials.CurrencyAmount(amount, Currency.TC_USD)

      // Submit for approval
      payment.submit()

      LOG.info("Created payment: ${amount} to ${payee.DisplayName}")
      return payment
    })
  }

  static function closeClaim(claim : Claim, outcome : CloseOutcome) {
    Transaction.runWithNewBundle(\bundle -> {
      var c = bundle.add(claim)

      // Close all open exposures first
      c.Exposures
        .where(\e -> e.State == ExposureState.TC_OPEN)
        .each(\e -> {
          e.close(outcome)
        })

      // Close claim
      c.close(outcome)
      LOG.info("Closed claim: ${c.ClaimNumber}")
    })
  }
}
```

## Output

- FNOL claim with claim number
- Exposures linked to coverages
- Reserves set on exposures
- Payments processed
- Claim closed with outcome

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Policy not found` | Invalid policy number | Verify policy number and status |
| `Coverage not applicable` | Wrong coverage type | Check policy coverages |
| `Reserve exceeds limit` | Over policy limit | Adjust to policy limits |
| `Payment validation` | Missing required fields | Check payee and amount |
| `Cannot close` | Open activities/exposures | Complete pending items |

## Claim Types and Loss Causes

```typescript
// Common loss types
const lossTypes = {
  AUTO: ['vehcollision', 'vehglass', 'vehtheft', 'vehvandalism'],
  PROPERTY: ['fire', 'water', 'theft', 'weather'],
  LIABILITY: ['bodily_injury', 'property_damage', 'personal_injury'],
  WORKERS_COMP: ['injury', 'illness', 'death']
};

// Map loss cause to exposures
function getDefaultExposures(lossType: string, lossCause: string): string[] {
  if (lossType === 'AUTO' && lossCause === 'vehcollision') {
    return ['VehicleDamage', 'BodilyInjury', 'PropertyDamage'];
  }
  // Additional mappings...
  return [];
}
```

## Resources

- [ClaimCenter Cloud API](https://docs.guidewire.com/cloud/cc/202503/apiref/)
- [Claims Workflow Guide](https://docs.guidewire.com/cloud/cc/202503/cloudapica/)
- [Exposure Types Reference](https://docs.guidewire.com/education/)

## Next Steps

For error handling patterns, see `guidewire-common-errors`.
