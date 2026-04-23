"""
PolicyPulse - Reinforcement Learning Agent

Real-time learning agent that improves prediction accuracy through experience.
The agent learns from actual citizen reactions and adjusts predictions to maximize reward.

Architecture:
- Experience replay buffer for stable learning
- Q-learning with function approximation
- Continuous learning during simulation
- Reward based on prediction accuracy

Reference: NN_IMPLEMENTATION.md Section "RL Integration"
"""

from __future__ import annotations

import logging
import pickle
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

if TYPE_CHECKING:
    from src.data_models import Citizen, CitizenState, Policy

logger = logging.getLogger("policypulse.rl_agent")


# =============================================================================
# Experience and Replay Buffer
# =============================================================================

@dataclass
class Experience:
    """
    Single experience tuple for RL training.
    
    Stores the state, action (prediction), reward, and next state.
    """
    state_features: np.ndarray  # Input features (24-dim)
    predicted_deltas: np.ndarray  # Predicted [happiness, support, income] changes
    actual_deltas: np.ndarray  # Actual observed changes
    reward: float  # Reward for this prediction
    policy_features: np.ndarray  # Policy context for better learning


class ReplayBuffer:
    """
    Experience replay buffer for stable RL training.
    
    Stores past experiences and samples them randomly for training,
    which breaks correlation and improves learning stability.
    """
    
    def __init__(self, max_size: int = 10000):
        """
        Initialize replay buffer.
        
        Args:
            max_size: Maximum number of experiences to store
        """
        self.buffer: deque[Experience] = deque(maxlen=max_size)
        self.max_size = max_size
    
    def add(self, experience: Experience) -> None:
        """Add an experience to the buffer."""
        self.buffer.append(experience)
    
    def sample(self, batch_size: int) -> list[Experience]:
        """
        Sample random batch of experiences.
        
        Args:
            batch_size: Number of experiences to sample
            
        Returns:
            List of randomly sampled experiences
        """
        if len(self.buffer) < batch_size:
            return list(self.buffer)
        
        indices = np.random.choice(len(self.buffer), batch_size, replace=False)
        return [self.buffer[i] for i in indices]
    
    def size(self) -> int:
        """Get current buffer size."""
        return len(self.buffer)
    
    def clear(self) -> None:
        """Clear all experiences."""
        self.buffer.clear()


# =============================================================================
# Reinforcement Learning Agent
# =============================================================================

class RLAgent:
    """
    Reinforcement Learning agent for real-time policy prediction learning.
    
    Features:
    - Continuous learning during simulation
    - Experience replay for stability
    - Multi-objective reward (accuracy on happiness, support, income)
    - Exploration vs exploitation via epsilon-greedy
    - Model persistence for knowledge retention
    
    The agent learns to predict citizen reactions more accurately over time
    by observing actual outcomes and adjusting its predictions.
    """
    
    def __init__(
        self,
        learning_rate: float = 0.001,
        discount_factor: float = 0.95,
        epsilon: float = 0.1,
        epsilon_decay: float = 0.995,
        epsilon_min: float = 0.01,
        batch_size: int = 32,
        update_frequency: int = 10,
        buffer_size: int = 10000,
    ):
        """
        Initialize RL agent.
        
        Args:
            learning_rate: Learning rate for neural network updates
            discount_factor: Discount factor for future rewards (not used in immediate reward setting)
            epsilon: Initial exploration rate (probability of random exploration)
            epsilon_decay: Decay rate for epsilon after each update
            epsilon_min: Minimum epsilon value
            batch_size: Number of experiences to sample for each training batch
            update_frequency: Train model every N experiences
            buffer_size: Maximum replay buffer size
        """
        # Hyperparameters
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.batch_size = batch_size
        self.update_frequency = update_frequency
        
        # Experience replay
        self.replay_buffer = ReplayBuffer(max_size=buffer_size)
        self.experiences_since_update = 0
        
        # Learning model (Q-function approximator)
        self.model = MLPRegressor(
            hidden_layer_sizes=(128, 64, 32),
            activation='relu',
            solver='adam',
            learning_rate_init=learning_rate,
            max_iter=1,  # We do incremental learning
            warm_start=True,  # Keep weights between .fit() calls
            random_state=42,
        )
        
        # Feature scaling
        self.scaler = StandardScaler()
        
        # Training state
        self.is_trained = False
        self.total_experiences = 0
        self.total_updates = 0
        self.cumulative_reward = 0.0
        
        # Performance tracking
        self.recent_rewards: deque[float] = deque(maxlen=100)
        self.prediction_errors: deque[float] = deque(maxlen=100)
        
        logger.info(
            f"RL Agent initialized: lr={learning_rate}, epsilon={epsilon}, "
            f"batch_size={batch_size}, buffer={buffer_size}"
        )
    
    def predict(
        self,
        state_features: np.ndarray,
        use_exploration: bool = True,
    ) -> tuple[float, float, float]:
        """
        Predict citizen reaction deltas with optional exploration.
        
        Args:
            state_features: 24-dimensional feature vector
            use_exploration: If True, occasionally explore random predictions
            
        Returns:
            Tuple of (delta_happiness, delta_support, delta_income_pct)
        """
        # Exploration: random prediction with probability epsilon
        if use_exploration and np.random.random() < self.epsilon:
            return self._explore_random()
        
        # Exploitation: use learned model
        if not self.is_trained:
            # Not trained yet, use heuristic baseline
            return self._heuristic_baseline(state_features)
        
        try:
            # Scale features and predict
            features_scaled = self.scaler.transform(state_features.reshape(1, -1))
            prediction = self.model.predict(features_scaled)[0]
            
            # Clamp to valid ranges
            delta_happiness = np.clip(prediction[0], -0.3, 0.3)
            delta_support = np.clip(prediction[1], -0.4, 0.4)
            delta_income_pct = np.clip(prediction[2], -0.1, 0.1)
            
            return (delta_happiness, delta_support, delta_income_pct)
            
        except Exception as e:
            logger.warning(f"RL prediction failed: {e}, using heuristic")
            return self._heuristic_baseline(state_features)
    
    def _explore_random(self) -> tuple[float, float, float]:
        """Generate random prediction for exploration."""
        delta_happiness = np.random.uniform(-0.3, 0.3)
        delta_support = np.random.uniform(-0.4, 0.4)
        delta_income_pct = np.random.uniform(-0.1, 0.1)
        return (delta_happiness, delta_support, delta_income_pct)
    
    def _heuristic_baseline(self, state_features: np.ndarray) -> tuple[float, float, float]:
        """
        Heuristic baseline when model not trained.
        
        Uses simple rules based on feature values.
        """
        # Extract some key features (assuming standard feature order)
        # age_norm = state_features[0]
        # income features at [1:4]
        income_low = state_features[1] if len(state_features) > 1 else 0
        # political features at [8:11]
        progressive = state_features[8] if len(state_features) > 8 else 0
        # personality traits at [11:13]
        openness = state_features[12] if len(state_features) > 12 else 0.5
        
        # Simple heuristic
        base_happiness = 0.05 if progressive > 0.5 else -0.02
        base_support = 0.1 if openness > 0.6 else -0.05
        base_income = 0.02 if income_low > 0.5 else 0.01
        
        # Add noise
        delta_happiness = np.clip(base_happiness + np.random.normal(0, 0.05), -0.3, 0.3)
        delta_support = np.clip(base_support + np.random.normal(0, 0.08), -0.4, 0.4)
        delta_income_pct = np.clip(base_income + np.random.normal(0, 0.02), -0.1, 0.1)
        
        return (delta_happiness, delta_support, delta_income_pct)
    
    def calculate_reward(
        self,
        predicted_deltas: np.ndarray,
        actual_deltas: np.ndarray,
    ) -> float:
        """
        Calculate reward based on prediction accuracy.
        
        Reward components:
        1. Negative mean squared error (closer predictions = higher reward)
        2. Bonus for correct direction (same sign as actual)
        3. Penalty for large errors
        
        Args:
            predicted_deltas: [delta_happiness, delta_support, delta_income_pct]
            actual_deltas: [actual_happiness_change, actual_support_change, actual_income_change]
            
        Returns:
            Reward value (higher is better)
        """
        # Ensure arrays
        predicted = np.array(predicted_deltas)
        actual = np.array(actual_deltas)
        
        # Component 1: Negative MSE (scaled)
        mse = np.mean((predicted - actual) ** 2)
        accuracy_reward = -mse * 10.0  # Scale to reasonable range
        
        # Component 2: Direction bonus
        direction_matches = np.sum(np.sign(predicted) == np.sign(actual))
        direction_bonus = direction_matches * 0.5  # Max +1.5 for all correct
        
        # Component 3: Magnitude penalty for very wrong predictions
        abs_errors = np.abs(predicted - actual)
        large_error_penalty = -np.sum(abs_errors > 0.2) * 0.5
        
        # Total reward
        reward = accuracy_reward + direction_bonus + large_error_penalty
        
        return float(reward)
    
    def store_experience(
        self,
        state_features: np.ndarray,
        predicted_deltas: tuple[float, float, float],
        actual_deltas: tuple[float, float, float],
        policy_features: np.ndarray,
    ) -> float:
        """
        Store an experience and trigger learning if needed.
        
        Args:
            state_features: Input features used for prediction
            predicted_deltas: What the model predicted
            actual_deltas: What actually happened
            policy_features: Policy context features
            
        Returns:
            The reward for this experience
        """
        # Calculate reward
        reward = self.calculate_reward(
            np.array(predicted_deltas),
            np.array(actual_deltas),
        )
        
        # Create experience
        experience = Experience(
            state_features=state_features,
            predicted_deltas=np.array(predicted_deltas),
            actual_deltas=np.array(actual_deltas),
            reward=reward,
            policy_features=policy_features,
        )
        
        # Store in replay buffer
        self.replay_buffer.add(experience)
        self.total_experiences += 1
        self.experiences_since_update += 1
        self.cumulative_reward += reward
        self.recent_rewards.append(reward)
        
        # Track prediction error
        error = np.mean(np.abs(np.array(predicted_deltas) - np.array(actual_deltas)))
        self.prediction_errors.append(error)
        
        # Trigger learning if enough experiences accumulated
        if self.experiences_since_update >= self.update_frequency:
            self._update_model()
            self.experiences_since_update = 0
        
        return reward
    
    def _update_model(self) -> None:
        """
        Update the RL model using experience replay.
        
        Samples a batch from replay buffer and performs one gradient step.
        """
        if self.replay_buffer.size() < self.batch_size:
            logger.debug(f"Not enough experiences yet: {self.replay_buffer.size()}/{self.batch_size}")
            return
        
        # Sample batch
        batch = self.replay_buffer.sample(self.batch_size)
        
        # Prepare training data
        X = np.array([exp.state_features for exp in batch])
        y = np.array([exp.actual_deltas for exp in batch])
        
        # Weight samples by reward (focus on good experiences)
        sample_weights = np.array([max(0.1, exp.reward + 1.0) for exp in batch])
        sample_weights = sample_weights / sample_weights.sum()
        
        try:
            # Fit scaler if first update
            if not self.is_trained:
                self.scaler.fit(X)
            
            # Scale features
            X_scaled = self.scaler.transform(X)
            
            # Update model
            self.model.partial_fit(X_scaled, y)
            
            self.is_trained = True
            self.total_updates += 1
            
            # Decay exploration rate
            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
            
            # Log progress
            if self.total_updates % 10 == 0:
                avg_reward = np.mean(list(self.recent_rewards)) if self.recent_rewards else 0
                avg_error = np.mean(list(self.prediction_errors)) if self.prediction_errors else 0
                logger.info(
                    f"RL Update #{self.total_updates}: "
                    f"avg_reward={avg_reward:.4f}, "
                    f"avg_error={avg_error:.4f}, "
                    f"epsilon={self.epsilon:.4f}, "
                    f"buffer={self.replay_buffer.size()}"
                )
        
        except Exception as e:
            logger.error(f"Failed to update RL model: {e}")
    
    def get_stats(self) -> dict:
        """
        Get current RL agent statistics.
        
        Returns:
            Dictionary with performance metrics
        """
        return {
            "total_experiences": self.total_experiences,
            "total_updates": self.total_updates,
            "buffer_size": self.replay_buffer.size(),
            "is_trained": self.is_trained,
            "epsilon": self.epsilon,
            "avg_recent_reward": np.mean(list(self.recent_rewards)) if self.recent_rewards else 0.0,
            "avg_recent_error": np.mean(list(self.prediction_errors)) if self.prediction_errors else 0.0,
            "cumulative_reward": self.cumulative_reward,
        }
    
    def save(self, filepath: Path) -> None:
        """
        Save RL agent state to disk.
        
        Args:
            filepath: Path to save file
        """
        try:
            state = {
                "model": self.model,
                "scaler": self.scaler,
                "epsilon": self.epsilon,
                "is_trained": self.is_trained,
                "total_experiences": self.total_experiences,
                "total_updates": self.total_updates,
                "cumulative_reward": self.cumulative_reward,
            }
            
            with open(filepath, "wb") as f:
                pickle.dump(state, f)
            
            logger.info(f"RL agent saved to {filepath}")
        
        except Exception as e:
            logger.error(f"Failed to save RL agent: {e}")
    
    def load(self, filepath: Path) -> bool:
        """
        Load RL agent state from disk.
        
        Args:
            filepath: Path to load file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not filepath.exists():
                logger.warning(f"RL agent file not found: {filepath}")
                return False
            
            with open(filepath, "rb") as f:
                state = pickle.load(f)
            
            self.model = state["model"]
            self.scaler = state["scaler"]
            self.epsilon = state["epsilon"]
            self.is_trained = state["is_trained"]
            self.total_experiences = state["total_experiences"]
            self.total_updates = state["total_updates"]
            self.cumulative_reward = state["cumulative_reward"]
            
            logger.info(
                f"RL agent loaded: {self.total_experiences} experiences, "
                f"{self.total_updates} updates"
            )
            return True
        
        except Exception as e:
            logger.error(f"Failed to load RL agent: {e}")
            return False
    
    def reset(self) -> None:
        """Reset agent to initial state (clears learning but keeps hyperparameters)."""
        self.replay_buffer.clear()
        self.experiences_since_update = 0
        self.total_experiences = 0
        self.total_updates = 0
        self.cumulative_reward = 0.0
        self.recent_rewards.clear()
        self.prediction_errors.clear()
        self.is_trained = False
        self.epsilon = 0.1  # Reset exploration rate
        
        # Reinitialize model
        self.model = MLPRegressor(
            hidden_layer_sizes=(128, 64, 32),
            activation='relu',
            solver='adam',
            learning_rate_init=self.learning_rate,
            max_iter=1,
            warm_start=True,
            random_state=42,
        )
        
        logger.info("RL agent reset to initial state")


# =============================================================================
# Factory Function
# =============================================================================

def create_rl_agent(
    learning_rate: float = 0.001,
    epsilon: float = 0.1,
    batch_size: int = 32,
    model_path: Path | None = None,
) -> RLAgent:
    """
    Factory function to create and optionally load an RL agent.
    
    Args:
        learning_rate: Learning rate for training
        epsilon: Initial exploration rate
        batch_size: Batch size for training
        model_path: Optional path to load saved model
        
    Returns:
        Initialized RLAgent
    """
    agent = RLAgent(
        learning_rate=learning_rate,
        epsilon=epsilon,
        batch_size=batch_size,
    )
    
    if model_path and model_path.exists():
        agent.load(model_path)
    
    return agent
