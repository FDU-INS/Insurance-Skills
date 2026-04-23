---
name: r-coding
description: Solve R-based actuarial exam questions (e.g. CS1B, CS2B) using R scripts
---

# R Coding Skill

You are solving an R-based actuarial exam paper (e.g. CS1B, CS2B). These papers typically provide data files (e.g. `.RData` or `.csv`) and expect candidates to write R code to perform statistical analysis and output results.

## Overview

Your workflow is:
1. **Identify data files** (usually `.RData` or `.csv` in `exams/<SUBJECT>/<SITTING>/`)
2. **Write R scripts** for each question
3. **Run the scripts** (if R is installed) to produce numerical answers
4. **Save outputs** (plots, console output)
5. **Document your code and results** in `attempt.md`

## Step 1 — Identify Data

Check the exam directory `exams/<SUBJECT>/<SITTING>/` for data files.
- `.RData`: Load using `load("path/to/file.RData")`
- `.csv`: Load using `read.csv("path/to/file.csv")`
- `.txt`: Load using `read.table("path/to/file.txt")`

## Step 2 — Write R Scripts

For each question, write a **standalone R script** that:
1. Loads the data
2. Performs the required analysis (summary stats, GLMs, time series, etc.)
3. Prints the results
4. Saves any required plots to `results/<MODEL>/<SUBJECT>/<SITTING>/`

### Template for an R script

```r
# ── Load Data ───────────────────────────────────────────────────
# Adjust path as needed - use absolute paths or relative to execution dict
load("exams/<SUBJECT>/<SITTING>/data.RData")

# ── Perform Analysis ────────────────────────────────────────────
# Example: Linear Model
model <- lm(Y ~ X, data = my_data)
summary(model)

# Example: Plotting
png("results/<MODEL>/<SUBJECT>/<SITTING>/q1_plot.png")
plot(model)
dev.off()

# ── Print Results ───────────────────────────────────────────────
print(summary(model))
# Print specific values if needed
cat("Adj R-squared:", summary(model)$adj.r.squared, "\n")
```

## Step 3 — Run Scripts

Run the script using `Rscript` and capture the output:

```bash
Rscript results/<MODEL>/<SUBJECT>/<SITTING>/q1_solution.R > results/<MODEL>/<SUBJECT>/<SITTING>/q1_output.txt
```

> **Note:** If `Rscript` is not available, you should still write the correct R code in the script file and include it in your attempt, but explicitly state that you could not run it to verify the output.

## Step 4 — Document in attempt.md

In `attempt.md`:
1. **Show the R code** used.
2. **Paste the output** (from the text file or your own analysis if unable to run).
3. **Embed plots** using markdown image syntax: `![Q1 Plot](q1_plot.png)`.
4. **Interpret the results** as required by the question (e.g. "The p-value is < 0.05, so we reject H0...").

## Common R Tasks for Actuarial Exams

- **Linear Regression:** `lm(y ~ x)`
- **GLMs:** `glm(y ~ x, family = poisson)`
- **Time Series:** `arima(x, order = c(1,0,1))`
- **Survival Analysis:** `survfit(Surv(time, event) ~ 1)`
- **Bootstrap:** Use `sample()`
- **Simulation:** `rnorm()`, `rpois()`, etc.
