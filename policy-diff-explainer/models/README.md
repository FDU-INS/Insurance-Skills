# PolicyPulse Models Directory

This directory stores trained machine learning models.

## Files

- `citizen_reaction_model.joblib` - Trained MLPRegressor neural network
- `feature_scaler.joblib` - StandardScaler for feature normalization

## Usage

Models are automatically loaded at application startup if they exist.
Training creates/overwrites these files.

## Note

These files are git-ignored as they are regenerated during training.
Large files should not be committed to version control.
