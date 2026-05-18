"""
PolicyPulse - Neural Network Model

Scikit-learn MLP for approximating LLM citizen reactions.
Reference: TECH_STACK.md Section 5 (ML Framework: Scikit-learn)

Dependencies: scikit-learn, joblib, numpy, data_models, config
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING
import logging

import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import joblib

if TYPE_CHECKING:
    from src.data_models import (
        Citizen,
        CitizenState,
        Policy,
    )

logger = logging.getLogger("policypulse.nn_model")


# =============================================================================
# Neural Network Model Class
# =============================================================================

class NeuralNetworkModel:
    """
    MLP model for predicting citizen reactions.
    
    Learns to approximate LLM-generated reactions from training samples.
    Uses knowledge distillation pattern: LLM (teacher) → NN (student).
    
    Reference: TECH_STACK.md Section 5 (Neural Network Architecture)
    """

    def __init__(self) -> None:
        """Initialize the neural network model (untrained state)."""
        self._model = MLPRegressor(
            hidden_layer_sizes=(64, 32),
            activation='relu',
            solver='adam',
            alpha=0.0001,
            batch_size='auto',
            learning_rate='adaptive',
            learning_rate_init=0.001,
            max_iter=500,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1,
            n_iter_no_change=10,
            verbose=False
        )
        self._scaler = StandardScaler()
        self._is_trained = False

    @property
    def is_trained(self) -> bool:
        """Check if the model has been trained."""
        return self._is_trained

    def predict(
        self,
        citizen: "Citizen",
        current_state: "CitizenState",
        policy: "Policy",
    ) -> tuple[float, float, float]:
        """
        Predict citizen reaction using the trained model or simple heuristics.
        
        Args:
            citizen: The citizen's static attributes
            current_state: The citizen's current state
            policy: The policy being simulated
            
        Returns:
            Tuple of (delta_happiness, delta_support, delta_income_pct)
        """
        # Build feature vector
        features = build_feature_vector(citizen, current_state, policy)
        
        if self._is_trained:
            try:
                # Scale features
                features_scaled = self._scaler.transform(features.reshape(1, -1))
                
                # Run inference
                predictions = self._model.predict(features_scaled)[0]
                
                # Extract predictions (3 outputs: happiness, support, income_pct)
                delta_happiness = np.clip(predictions[0], -0.3, 0.3)
                delta_support = np.clip(predictions[1], -0.4, 0.4)
                delta_income_pct = np.clip(predictions[2], -0.1, 0.1)
                
                return float(delta_happiness), float(delta_support), float(delta_income_pct)
            except Exception as e:
                logger.warning(f"NN prediction failed, using heuristics: {e}")
        
        # Fallback: Use simple heuristics based on citizen attributes
        return self._predict_with_heuristics(citizen, current_state, policy)
    
    def _predict_with_heuristics(
        self,
        citizen: "Citizen",
        current_state: "CitizenState",
        policy: "Policy",
    ) -> tuple[float, float, float]:
        """Simple heuristic-based prediction when model not trained."""
        from src.data_models import IncomeLevel, PolicyDomain, PoliticalView
        
        # Base effects by policy domain
        domain_effects = {
            PolicyDomain.ECONOMY: (0.01, 0.0, 0.02),
            PolicyDomain.EDUCATION: (0.03, 0.05, 0.01),
            PolicyDomain.SOCIAL: (0.04, 0.03, 0.005),
            PolicyDomain.BUSINESS: (0.01, -0.02, 0.025),
        }
        base_h, base_s, base_i = domain_effects.get(policy.domain, (0.02, 0.0, 0.01))
        
        # Modify by income level
        if citizen.income_level == IncomeLevel.LOW:
            if policy.domain in [PolicyDomain.EDUCATION, PolicyDomain.SOCIAL]:
                base_h += 0.03
                base_s += 0.05
                base_i += 0.01
            elif policy.domain == PolicyDomain.ECONOMY:
                base_h -= 0.02
        elif citizen.income_level == IncomeLevel.HIGH:
            if policy.domain in [PolicyDomain.ECONOMY, PolicyDomain.BUSINESS]:
                base_h += 0.04
                base_s += 0.06
                base_i += 0.02
        
        # Modify by political view
        if citizen.political_view == PoliticalView.PROGRESSIVE:
            if policy.domain in [PolicyDomain.EDUCATION, PolicyDomain.SOCIAL]:
                base_s += 0.08
            elif policy.domain == PolicyDomain.ECONOMY:
                base_s -= 0.03
        elif citizen.political_view == PoliticalView.CONSERVATIVE:
            if policy.domain in [PolicyDomain.ECONOMY, PolicyDomain.BUSINESS]:
                base_s += 0.08
            elif policy.domain == PolicyDomain.SOCIAL:
                base_s -= 0.05
        
        # Add personality influence
        base_h += (citizen.openness_to_change - 0.5) * 0.05
        base_s += (citizen.openness_to_change - 0.5) * 0.1
        
        # Add small random noise for variability
        noise = np.random.normal(0, 0.01, 3)
        
        return (
            float(np.clip(base_h + noise[0], -0.3, 0.3)),
            float(np.clip(base_s + noise[1], -0.4, 0.4)),
            float(np.clip(base_i + noise[2], -0.1, 0.1))
        )

    def save(self, model_path: Path, scaler_path: Path) -> None:
        """Save the trained model and scaler to disk."""
        if not self._is_trained:
            logger.warning("Attempting to save untrained model")
            return
        
        try:
            joblib.dump(self._model, model_path)
            joblib.dump(self._scaler, scaler_path)
            logger.info(f"Model saved to {model_path}")
        except Exception as e:
            logger.error(f"Failed to save model: {e}")

    def load(self, model_path: Path, scaler_path: Path) -> bool:
        """Load a trained model and scaler from disk."""
        try:
            if model_path.exists() and scaler_path.exists():
                self._model = joblib.load(model_path)
                self._scaler = joblib.load(scaler_path)
                self._is_trained = True
                logger.info(f"Model loaded from {model_path}")
                return True
        except Exception as e:
            logger.warning(f"Failed to load model: {e}")
        
        return False


def build_feature_vector(
    citizen: "Citizen",
    current_state: "CitizenState",
    policy: "Policy",
) -> np.ndarray:
    """
    Build a 24-dimensional feature vector for a citizen.
    
    Reference: TECH_STACK.md Section 5 (Feature Engineering)
    
    Features include:
    - Normalized age
    - One-hot encoded income level (3)
    - One-hot encoded city zone (4)
    - One-hot encoded political view (3)
    - Personality traits (risk_tolerance, openness_to_change)
    - Normalized family size
    - Previous state values (happiness, support, log income)
    - One-hot encoded policy domain (4)
    """
    from src.data_models import IncomeLevel, CityZone, PoliticalView, PolicyDomain
    
    features = []
    
    # Normalized age (0-1, assuming max age ~100)
    features.append(citizen.age / 100.0)
    
    # One-hot: income level (3 features)
    features.append(1.0 if citizen.income_level == IncomeLevel.LOW else 0.0)
    features.append(1.0 if citizen.income_level == IncomeLevel.MIDDLE else 0.0)
    features.append(1.0 if citizen.income_level == IncomeLevel.HIGH else 0.0)
    
    # One-hot: city zone (4 features)
    features.append(1.0 if citizen.city_zone == CityZone.DOWNTOWN else 0.0)
    features.append(1.0 if citizen.city_zone == CityZone.INDUSTRIAL else 0.0)
    features.append(1.0 if citizen.city_zone == CityZone.SUBURBAN else 0.0)
    features.append(1.0 if citizen.city_zone == CityZone.RURAL else 0.0)
    
    # One-hot: political view (3 features)
    features.append(1.0 if citizen.political_view == PoliticalView.PROGRESSIVE else 0.0)
    features.append(1.0 if citizen.political_view == PoliticalView.MODERATE else 0.0)
    features.append(1.0 if citizen.political_view == PoliticalView.CONSERVATIVE else 0.0)
    
    # Personality traits (2 features)
    features.append(citizen.risk_tolerance)
    features.append(citizen.openness_to_change)
    
    # Normalized family size (0-1, assuming max ~10)
    features.append(citizen.family_size / 10.0)
    
    # Previous state values (3 features)
    features.append(current_state.happiness)  # Already 0-1
    features.append((current_state.policy_support + 1.0) / 2.0)  # -1 to 1 → 0 to 1
    features.append(np.log1p(current_state.income) / 15.0)  # Log normalized
    
    # One-hot: policy domain (4 features)
    features.append(1.0 if policy.domain == PolicyDomain.ECONOMY else 0.0)
    features.append(1.0 if policy.domain == PolicyDomain.EDUCATION else 0.0)
    features.append(1.0 if policy.domain == PolicyDomain.SOCIAL else 0.0)
    features.append(1.0 if policy.domain == PolicyDomain.BUSINESS else 0.0)
    
    return np.array(features, dtype=np.float32)


class ModelNotTrainedError(Exception):
    """Raised when prediction is attempted on an untrained model."""
    pass


class InsufficientSamplesError(Exception):
    """Raised when training is attempted with too few samples."""
    pass

