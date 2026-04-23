# PolicyPulse Data Directory

This directory stores persistent training data.

## Files

- `llm_training_samples.csv` - Training samples collected from LLM reactions

## Format

CSV with columns:
- `feature_0` through `feature_23` - 24-dimensional feature vector
- `delta_happiness` - Change in happiness from LLM reaction
- `delta_support` - Change in policy support
- `delta_income` - Change in income

## Note

This file is git-ignored as it is regenerated during simulation sessions.
