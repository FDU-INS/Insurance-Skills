# Actuarial Reserving Methods — Reference

## 1. Chain Ladder (Development Factor Method)

The development factor method is the most widely used reserving technique (Friedland Ch. 7, *Estimating Unpaid Claims Using Basic Techniques*). It is referenced throughout ASOP No. 43 as a standard approach. CAS Exam 5 papers by Friedland and by Wiser et al. provide foundational treatment.

### Age-to-Age Factors (Link Ratios)

For each development period transition d → d+1:

**Volume-Weighted Average:**
```
f(d) = Σ C(i, d+1) / Σ C(i, d)
```
where the sum is over all accident periods i with data at both ages d and d+1. Friedland refers to this as the "weighted average" — it gives more weight to larger accident years.

**Simple Average:**
```
f(d) = (1/n) × Σ [C(i, d+1) / C(i, d)]
```

**Medial Average (excluding high/low):**
Remove the highest and lowest individual factor for each development period, then average the rest. See Friedland Ch. 7 for discussion of when medial averages are preferable to simple or volume-weighted.

### Cumulative Development Factors (CDFs)

```
CDF(d) = f(d) × f(d+1) × ... × f(ultimate)
```

### Ultimate Losses

```
Ultimate(i) = C(i, latest_d) × CDF(latest_d → ultimate)
```

### IBNR

```
IBNR(i) = Ultimate(i) - C(i, latest_d)
```

where C(i, latest_d) represents:
- Latest **paid** losses for the paid development method
- Latest **incurred** (paid + case reserves) losses for the incurred development method

### Tail Factor

The tail factor projects development beyond the oldest maturity in the triangle.

**Common approaches:**
- **No tail (1.000)**: Appropriate when triangle is fully developed
- **Inverse power curve fit**: Fit f(d) = 1 + a × d^(-b) and extrapolate
- **Exponential decay**: Fit ln(f(d) - 1) as a linear function of d
- **Industry benchmark**: Use industry LDFs from ISO, NAIC, or AM Best

Tail factor selection is addressed in ASOP No. 43 under Section 3.6.1 (Methods and Models) as part of the overall method selection process. ASOP No. 43 Section 3.6.7 (Changing Conditions) is also relevant, as changes in claim settlement patterns can affect tail behavior. Friedland discusses tail factors within Ch. 7 (Development Technique). The CAS *Statement of Principles Regarding Property and Casualty Loss and Loss Adjustment Expense Reserves* also emphasizes the importance of tail factor selection.

For this quick check, default to exponential decay if the last 3+ known factors show a declining pattern. Otherwise default to 1.000 with a note.

---

## 2. Bornhuetter-Ferguson (BF)

Introduced by Bornhuetter & Ferguson (PCAS 1972). Friedland Ch. 9 provides a thorough walkthrough. The BF method applies credibility concepts (see ASOP No. 25) by weighting between observed development and an a priori expectation.

### Formula

```
Ultimate(i) = C(i, latest_d) + ELR × Premium(i) × [1 - 1/CDF(latest_d)]
```

where:
- `ELR` = Expected (a priori) Loss Ratio
- `Premium(i)` = Earned premium for accident period i
- `CDF` = Cumulative development factor from Chain Ladder
- `[1 - 1/CDF]` = Percent unreported

### Key Properties

- Gives more weight to the a priori for immature accident years
- Converges to Chain Ladder as accident years mature
- Less sensitive to early development volatility than pure chain ladder
- Requires an external ELR assumption

### Selecting the A Priori ELR

The selection of an a priori ELR is a key actuarial judgment. ASOP No. 43 Section 3.6.2 (Assumptions) notes that the actuary should consider the appropriateness of assumptions underlying each method. Werner & Modlin Ch. 6 discusses expected loss ratios in the ratemaking context, which can inform BF assumptions.

If not provided by the user:
1. Use the Chain Ladder ultimate loss ratio for the most mature years (weighted by premium)
2. Or use the overall Chain Ladder indicated loss ratio as a starting point

---

## 3. Cape Cod (Stanard-Bühlmann)

Also known as the Stanard-Bühlmann method (Stanard, PCAS 1985). Friedland Ch. 10 covers this method. It addresses a key limitation of BF by deriving the ELR from the data itself rather than requiring an external assumption.

### Formula

The Cape Cod method is a variant of BF that **derives** the ELR from the data rather than using an external assumption.

```
ELR_cc = Σ C(i, latest_d) / Σ [Premium(i) × (1/CDF(latest_d))]
```

This ELR is the used-up premium weighted average loss ratio.

Then:
```
Ultimate(i) = C(i, latest_d) + ELR_cc × Premium(i) × [1 - 1/CDF(latest_d)]
```

### Key Properties

- Self-calibrating: ELR comes from the data
- More stable than pure Chain Ladder for volatile lines
- Still depends on CDF selection from Chain Ladder

---

## 4. Expected Loss Ratio (ELR) Method

### Formula

```
Ultimate(i) = ELR × Premium(i)
IBNR(i) = Ultimate(i) - C(i, latest_d)
```

### When to Use

Friedland Ch. 8 discusses the ELR method as a benchmark. Per ASOP No. 25, when observed data has low credibility, greater weight should be given to the expected value — making the ELR method appropriate for the most immature accident periods.

- Very immature accident years with little credible development data
- As a benchmark/floor for other methods
- When the user provides a specific ELR target

---

## 5. Diagnostic Tests

ASOP No. 43 Section 3.7.1 (Reasonableness) requires the actuary to assess the reasonableness of results. These diagnostic tests support that assessment. See also Friedland Ch. 6 (Development Triangle as Diagnostic Tool) and Ch. 15 (Evaluation of Techniques) for discussion of diagnostic techniques.

### Calendar Year Development Test

This test relates to ASOP No. 43 Section 3.6.2 (Assumptions) and 3.6.7 (Changing Conditions), which address the assumption of consistent development patterns and how changes over time can affect estimates.

Sum losses along each calendar year diagonal and compute year-over-year development. Consistent development suggests stable reserving practices. Patterns to flag:

- **Consistently positive**: May indicate under-reserving
- **Consistently negative**: May indicate over-reserving or strengthening
- **Sudden shift**: May indicate change in claims practices or reserve policy

### Outlier Detection in Age-to-Age Factors

Per ASOP No. 23 Section 3.3 (Review of Data), the actuary should review data for reasonableness and consider whether outliers reflect data errors or genuine changes in the loss process.

For each development period column, compute mean and standard deviation of individual factors. Flag any factor where:
```
|factor - mean| > 2 × std_dev
```

### Paid-to-Incurred Ratio Analysis

Friedland Ch. 6 discusses the paid-to-incurred ratio as a key diagnostic. Divergence patterns may signal issues with case reserve adequacy that warrant investigation per ASOP No. 43 Section 3.5 (Nature of Unpaid Claims).

If both paid and incurred triangles are available:
```
P/I Ratio(i, d) = Paid(i, d) / Incurred(i, d)
```

Expected pattern: P/I ratio should increase with maturity (approaching 1.0). Deviations suggest:
- **P/I falling with maturity**: Case reserves being added faster than payments — possible adverse development
- **P/I > 1.0**: Salvage/subrogation or case reserve takedowns

### Tail Factor Sensitivity

Recompute ultimates with tail factors at ±10% and ±25% of selected:
```
Tail_low_25  = 1 + (tail - 1) × 0.75
Tail_low_10  = 1 + (tail - 1) × 0.90
Tail_high_10 = 1 + (tail - 1) × 1.10
Tail_high_25 = 1 + (tail - 1) × 1.25
```

Report the range of total IBNR under each scenario.

---

## References

### Actuarial Standards of Practice (ASOPs)

- **ASOP No. 23** — *Data Quality*. Actuarial Standards Board. Guidance on selecting, reviewing, and relying on data in actuarial analyses.
- **ASOP No. 25** — *Credibility Procedures*. Actuarial Standards Board. Standards for applying credibility theory, including when to weight observed experience vs. a priori expectations.
- **ASOP No. 36** — *Statements of Actuarial Opinion Regarding Property/Casualty Loss, Loss Adjustment Expense, or Other Reserves*. Actuarial Standards Board. Requirements for issuing formal actuarial opinions on reserves.
- **ASOP No. 43** — *Property/Casualty Unpaid Claim Estimates*. Actuarial Standards Board. The core standard governing the estimation of unpaid claims, including method selection, data considerations, assumptions, and reasonableness assessment.

### Textbooks and CAS Materials

- **Friedland, J.** *Estimating Unpaid Claims Using Basic Techniques*. Casualty Actuarial Society, Version 3 (2010). The foundational reference for loss reserving methods. Key chapters: Ch. 6 (Development Triangle as Diagnostic Tool), Ch. 7 (Development Technique), Ch. 8 (Expected Claims Technique), Ch. 9 (Bornhuetter-Ferguson Technique), Ch. 10 (Cape Cod Technique), Ch. 15 (Evaluation of Techniques).
- **Werner, G. & Modlin, C.** *Basic Ratemaking*. Casualty Actuarial Society. Covers loss development in the pricing context, including expected loss ratio selection and credibility.
- **Bornhuetter, R.L. & Ferguson, R.E.** "The Actuary and IBNR." *Proceedings of the Casualty Actuarial Society*, 1972. Original paper introducing the BF method.
- **Stanard, J.N.** "A Simulation Test of Prediction Errors of Loss Reserve Estimation Techniques." *Proceedings of the Casualty Actuarial Society*, 1985. Introduces the Cape Cod / Stanard-Bühlmann method.
- **Wiser, R.F. et al.** "Loss Reserving." *Foundations of Casualty Actuarial Science*, CAS. Overview of reserving principles and methods used in CAS examination syllabus.
