---
name: guidewire-core-workflow-a
description: |
  Execute Guidewire primary workflow: Policy lifecycle management in PolicyCenter.
  Use when implementing quoting, binding, issuing, endorsing, or renewing policies.
  Trigger with phrases like "policycenter workflow", "create policy",
  "bind submission", "issue policy", "policy endorsement", "quote insurance".
allowed-tools: Read, Write, Edit, Bash(curl:*), Bash(npm:*), Grep
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# Guidewire Core Workflow A: Policy Lifecycle

## Overview

Master the complete policy lifecycle in PolicyCenter: submission creation, quoting, binding, issuance, endorsements, and renewals.

## Prerequisites

- Completed `guidewire-install-auth` and `guidewire-sdk-patterns`
- Understanding of P&C insurance concepts
- Valid API credentials with policy admin permissions

## Policy Lifecycle States

```
Submission → Quote → Bind → Issue → In-Force → Endorsement/Renewal/Cancellation
    |           |       |      |          |
    v           v       v      v          v
 [Draft]    [Quoted] [Bound] [Issued] [Active Policy]
```

## Instructions

### Step 1: Create Account

```typescript
// Create an account before policy submission
interface CreateAccountRequest {
  data: {
    attributes: {
      accountHolder: {
        contactSubtype: 'Person';
        firstName: string;
        lastName: string;
        dateOfBirth: string;
        primaryAddress: {
          addressLine1: string;
          city: string;
          state: { code: string };
          postalCode: string;
          country: { code: string };
        };
      };
      producerCodes: Array<{ id: string }>;
    };
  };
}

async function createAccount(holder: AccountHolderData): Promise<Account> {
  const request: CreateAccountRequest = {
    data: {
      attributes: {
        accountHolder: {
          contactSubtype: 'Person',
          firstName: holder.firstName,
          lastName: holder.lastName,
          dateOfBirth: holder.dateOfBirth,
          primaryAddress: {
            addressLine1: holder.address,
            city: holder.city,
            state: { code: holder.state },
            postalCode: holder.zip,
            country: { code: 'US' }
          }
        },
        producerCodes: [{ id: holder.producerCodeId }]
      }
    }
  };

  const response = await client.request<{ data: Account }>(
    'POST',
    '/account/v1/accounts',
    request
  );

  return response.data;
}
```

### Step 2: Create Submission

```typescript
// Create a new policy submission
interface CreateSubmissionRequest {
  data: {
    attributes: {
      account: { id: string };
      baseState: { code: string };
      effectiveDate: string;
      product: { code: string };
      producerCode: { id: string };
      jobType: { code: 'Submission' };
    };
  };
}

async function createSubmission(
  accountId: string,
  effectiveDate: string,
  productCode: string = 'PersonalAuto'
): Promise<Submission> {
  const request: CreateSubmissionRequest = {
    data: {
      attributes: {
        account: { id: accountId },
        baseState: { code: 'CA' },
        effectiveDate: effectiveDate,
        product: { code: productCode },
        producerCode: { id: 'pc:DefaultProducerCode' },
        jobType: { code: 'Submission' }
      }
    }
  };

  const response = await client.request<{ data: Submission }>(
    'POST',
    '/job/v1/submissions',
    request
  );

  console.log(`Created submission: ${response.data.jobNumber}`);
  return response.data;
}
```

### Step 3: Add Policy Lines and Coverages

```typescript
// Add Personal Auto line with vehicles and coverages
interface VehicleData {
  vin: string;
  year: number;
  make: string;
  model: string;
  costNew: number;
}

async function addVehicleWithCoverages(
  submissionId: string,
  policyPeriodId: string,
  vehicle: VehicleData
): Promise<void> {
  // Add vehicle
  const vehicleRequest = {
    data: {
      attributes: {
        vin: vehicle.vin,
        year: vehicle.year,
        make: vehicle.make,
        model: vehicle.model,
        costNew: { amount: vehicle.costNew, currency: 'usd' },
        vehicleType: { code: 'PP' } // Private Passenger
      }
    }
  };

  const vehicleResponse = await client.request(
    'POST',
    `/job/v1/submissions/${submissionId}/policy-periods/${policyPeriodId}/vehicles`,
    vehicleRequest
  );

  const vehicleId = vehicleResponse.data.id;

  // Add coverages to vehicle
  const coverages = [
    { code: 'PALiabilityCov', limits: { BI: '100000/300000', PD: '50000' } },
    { code: 'PACollisionCov', deductible: 500 },
    { code: 'PAComprehensiveCov', deductible: 250 },
    { code: 'PAMedPayCov', limit: 5000 }
  ];

  for (const coverage of coverages) {
    await client.request(
      'POST',
      `/job/v1/submissions/${submissionId}/policy-periods/${policyPeriodId}/vehicles/${vehicleId}/coverages`,
      {
        data: {
          attributes: {
            patternCode: coverage.code,
            // Coverage-specific terms would be set here
          }
        }
      }
    );
  }
}
```

### Step 4: Add Drivers

```typescript
// Add drivers to policy
interface DriverData {
  firstName: string;
  lastName: string;
  dateOfBirth: string;
  licenseNumber: string;
  licenseState: string;
}

async function addDriver(
  submissionId: string,
  policyPeriodId: string,
  driver: DriverData
): Promise<PolicyDriver> {
  const request = {
    data: {
      attributes: {
        firstName: driver.firstName,
        lastName: driver.lastName,
        dateOfBirth: driver.dateOfBirth,
        licenseNumber: driver.licenseNumber,
        licenseState: { code: driver.licenseState },
        gender: { code: 'M' },
        maritalStatus: { code: 'S' }
      }
    }
  };

  const response = await client.request<{ data: PolicyDriver }>(
    'POST',
    `/job/v1/submissions/${submissionId}/policy-periods/${policyPeriodId}/drivers`,
    request
  );

  return response.data;
}
```

### Step 5: Quote the Submission

```typescript
// Request a quote
async function quoteSubmission(submissionId: string): Promise<QuoteResult> {
  // Trigger quote calculation
  const quoteResponse = await client.request<{ data: Submission }>(
    'POST',
    `/job/v1/submissions/${submissionId}/quote`,
    {}
  );

  // Get quote details
  const submission = quoteResponse.data;
  const policyPeriod = await client.request<{ data: PolicyPeriod }>(
    'GET',
    `/job/v1/submissions/${submissionId}/policy-periods/${submission.latestPeriod.id}`
  );

  return {
    jobNumber: submission.jobNumber,
    status: submission.status.code,
    totalPremium: policyPeriod.data.totalPremium,
    taxes: policyPeriod.data.taxes,
    effectiveDate: policyPeriod.data.effectiveDate,
    expirationDate: policyPeriod.data.expirationDate
  };
}
```

### Step 6: Bind the Policy

```typescript
// Bind the quoted submission
async function bindSubmission(submissionId: string): Promise<BoundPolicy> {
  const response = await client.request<{ data: Submission }>(
    'POST',
    `/job/v1/submissions/${submissionId}/bind`,
    {}
  );

  if (response.data.status.code !== 'Bound') {
    throw new Error(`Bind failed: ${response.data.status.name}`);
  }

  return {
    jobNumber: response.data.jobNumber,
    policyNumber: response.data.policy.policyNumber,
    status: 'Bound'
  };
}
```

### Step 7: Issue the Policy

```typescript
// Issue bound policy (often automatic)
async function issuePolicy(submissionId: string): Promise<IssuedPolicy> {
  const response = await client.request<{ data: Submission }>(
    'POST',
    `/job/v1/submissions/${submissionId}/issue`,
    {}
  );

  return {
    policyNumber: response.data.policy.policyNumber,
    status: 'Issued',
    effectiveDate: response.data.latestPeriod.effectiveDate
  };
}
```

## Gosu Implementation

```gosu
// Complete policy submission workflow in Gosu
package gw.custom.submission

uses gw.api.productmodel.Product
uses gw.api.util.Logger
uses gw.transaction.Transaction

class SubmissionWorkflow {
  private static final var LOG = Logger.forCategory("SubmissionWorkflow")

  static function createAndQuoteSubmission(
    account : Account,
    product : Product,
    effectiveDate : Date
  ) : Submission {

    return Transaction.runWithNewBundle(\bundle -> {
      var account = bundle.add(account)

      // Create submission
      var submission = new Submission(bundle)
      submission.Account = account
      submission.Product = product
      submission.EffectiveDate = effectiveDate
      submission.ProducerCodeOfRecord = account.ProducerCodes.first()

      // Initialize policy period
      submission.initializePeriod()
      var period = submission.LatestPeriod

      // Add line of business
      if (product.Code == "PersonalAuto") {
        initializePersonalAutoLine(period)
      }

      LOG.info("Created submission: ${submission.JobNumber}")
      return submission
    })
  }

  private static function initializePersonalAutoLine(period : PolicyPeriod) {
    var paLine = new PersonalAutoLine(period.Bundle)
    paLine.PolicyPeriod = period

    // Set state-specific coverages
    paLine.initializeCoverages()
  }

  static function quoteSubmission(submission : Submission) : PolicyPeriod {
    return Transaction.runWithNewBundle(\bundle -> {
      var sub = bundle.add(submission)

      // Validate before quoting
      var validationResult = sub.LatestPeriod.validateForQuote()
      if (validationResult.hasErrors()) {
        throw new ValidationException(validationResult.AllMessages.join(", "))
      }

      // Request quote
      sub.requestQuote()

      // Wait for async rating if needed
      if (sub.LatestPeriod.Status == PolicyPeriodStatus.TC_QUOTING) {
        sub.LatestPeriod.awaitQuoteComplete()
      }

      LOG.info("Quoted submission ${sub.JobNumber}: ${sub.LatestPeriod.TotalPremiumRPT}")
      return sub.LatestPeriod
    })
  }

  static function bindAndIssue(submission : Submission) : Policy {
    return Transaction.runWithNewBundle(\bundle -> {
      var sub = bundle.add(submission)

      // Bind
      sub.requestBind()
      if (!sub.LatestPeriod.canIssue()) {
        throw new IllegalStateException("Cannot issue: ${sub.LatestPeriod.Status}")
      }

      // Issue
      sub.requestIssue()

      LOG.info("Issued policy: ${sub.Policy.PolicyNumber}")
      return sub.Policy
    })
  }
}
```

## Output

- Created account with account holder details
- Submission with unique job number
- Quote with premium breakdown
- Bound and issued policy with policy number

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Validation failed` | Missing required data | Check all required fields |
| `Cannot quote` | Invalid policy configuration | Review coverages and limits |
| `Cannot bind` | Outstanding issues | Resolve all validation errors |
| `UW hold` | Requires underwriting approval | Process UW referrals |
| `Rating error` | Rating engine failure | Check rate tables and factors |

## Common Validation Issues

```typescript
// Handle validation errors
interface ValidationError {
  field: string;
  message: string;
  code: string;
}

function handleValidationErrors(errors: ValidationError[]): void {
  const grouped = errors.reduce((acc, err) => {
    acc[err.field] = acc[err.field] || [];
    acc[err.field].push(err.message);
    return acc;
  }, {} as Record<string, string[]>);

  console.log('Validation Errors:');
  Object.entries(grouped).forEach(([field, messages]) => {
    console.log(`  ${field}:`);
    messages.forEach(msg => console.log(`    - ${msg}`));
  });
}
```

## Resources

- [PolicyCenter Cloud API](https://docs.guidewire.com/cloud/pc/202503/apiref/)
- [Submission Workflow Guide](https://docs.guidewire.com/cloud/pc/202503/cloudapica/)
- [Policy Lifecycle Documentation](https://docs.guidewire.com/education/)

## Next Steps

For claims processing workflow, see `guidewire-core-workflow-b`.
