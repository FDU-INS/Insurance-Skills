"""
PolicyPulse - Reinforcement Learning Trainer

Foundation for reinforcement learning to adapt policy analysis over time.
This allows the system to learn from feedback and improve predictions.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.policy_analyzer import PolicyAnalysis
    from src.data_models import SimulationResult

logger = logging.getLogger("policypulse.rl_trainer")


@dataclass
class PolicyFeedback:
    """
    Feedback on a policy analysis prediction vs actual results.
    Used for reinforcement learning.
    """
    policy_title: str
    policy_description: str
    policy_domain: str
    
    # Predicted impacts (from PolicyAnalysis)
    predicted_low_income_happiness: float
    predicted_middle_income_happiness: float
    predicted_high_income_happiness: float
    predicted_progressive_support: float
    predicted_moderate_support: float
    predicted_conservative_support: float
    
    # Actual results (from simulation)
    actual_low_income_happiness: float
    actual_middle_income_happiness: float
    actual_high_income_happiness: float
    actual_progressive_support: float
    actual_moderate_support: float
    actual_conservative_support: float
    
    # Errors (for learning)
    happiness_error: float  # Mean absolute error
    support_error: float
    
    # Metadata
    confidence: float
    timestamp: str


@dataclass
class LearningMetrics:
    """Tracks learning progress over time."""
    total_feedback_samples: int
    avg_happiness_error: float
    avg_support_error: float
    improvement_rate: float  # Negative = improving


class RLTrainer:
    """
    Reinforcement learning trainer for policy analysis.
    
    Collects feedback from simulations and uses it to improve
    policy analysis predictions over time.
    
    This is a foundation for:
    1. Collecting actual vs predicted data
    2. Computing rewards/penalties
    3. Fine-tuning policy understanding
    4. Adaptive weight learning
    """
    
    def __init__(self, feedback_path: Path | None = None):
        """
        Initialize RL trainer.
        
        Args:
            feedback_path: Path to store feedback data
        """
        self.feedback_path = feedback_path or Path("data/rl_feedback.jsonl")
        self.feedback_path.parent.mkdir(parents=True, exist_ok=True)
        self.feedback_history: list[PolicyFeedback] = []
        self._load_feedback()
    
    def _load_feedback(self):
        """Load existing feedback from disk."""
        if not self.feedback_path.exists():
            return
        
        try:
            with open(self.feedback_path, "r") as f:
                for line in f:
                    data = json.loads(line.strip())
                    feedback = PolicyFeedback(**data)
                    self.feedback_history.append(feedback)
            logger.info(f"Loaded {len(self.feedback_history)} feedback samples")
        except Exception as e:
            logger.warning(f"Failed to load feedback: {e}")
    
    def _save_feedback(self, feedback: PolicyFeedback):
        """Append new feedback to disk."""
        try:
            with open(self.feedback_path, "a") as f:
                f.write(json.dumps(asdict(feedback)) + "\n")
        except Exception as e:
            logger.error(f"Failed to save feedback: {e}")
    
    def collect_feedback(
        self,
        policy_analysis: PolicyAnalysis,
        simulation_result: SimulationResult,
    ) -> PolicyFeedback:
        """
        Collect feedback by comparing prediction vs actual results.
        
        Args:
            policy_analysis: The LLM's predicted impacts
            simulation_result: The actual simulation results
            
        Returns:
            Feedback record with errors calculated
        """
        from datetime import datetime
        from src.data_models import IncomeLevel, PoliticalView
        
        # Get final metrics
        final_metrics = simulation_result.metrics_by_step[-1]
        initial_metrics = simulation_result.metrics_by_step[0]
        
        # Calculate actual changes
        actual_low = (
            final_metrics.happiness_by_income.get(IncomeLevel.LOW, 0) -
            initial_metrics.happiness_by_income.get(IncomeLevel.LOW, 0)
        )
        actual_middle = (
            final_metrics.happiness_by_income.get(IncomeLevel.MIDDLE, 0) -
            initial_metrics.happiness_by_income.get(IncomeLevel.MIDDLE, 0)
        )
        actual_high = (
            final_metrics.happiness_by_income.get(IncomeLevel.HIGH, 0) -
            initial_metrics.happiness_by_income.get(IncomeLevel.HIGH, 0)
        )
        
        actual_prog_support = (
            final_metrics.support_by_political.get(PoliticalView.PROGRESSIVE, 0) -
            initial_metrics.support_by_political.get(PoliticalView.PROGRESSIVE, 0)
        )
        actual_mod_support = (
            final_metrics.support_by_political.get(PoliticalView.MODERATE, 0) -
            initial_metrics.support_by_political.get(PoliticalView.MODERATE, 0)
        )
        actual_cons_support = (
            final_metrics.support_by_political.get(PoliticalView.CONSERVATIVE, 0) -
            initial_metrics.support_by_political.get(PoliticalView.CONSERVATIVE, 0)
        )
        
        # Calculate errors
        happiness_errors = [
            abs(policy_analysis.low_income_happiness_impact - actual_low),
            abs(policy_analysis.middle_income_happiness_impact - actual_middle),
            abs(policy_analysis.high_income_happiness_impact - actual_high),
        ]
        happiness_error = sum(happiness_errors) / len(happiness_errors)
        
        support_errors = [
            abs(policy_analysis.progressive_support - actual_prog_support),
            abs(policy_analysis.moderate_support - actual_mod_support),
            abs(policy_analysis.conservative_support - actual_cons_support),
        ]
        support_error = sum(support_errors) / len(support_errors)
        
        # Create feedback record
        feedback = PolicyFeedback(
            policy_title=simulation_result.policy.title,
            policy_description=simulation_result.policy.description,
            policy_domain=simulation_result.policy.domain.value,
            predicted_low_income_happiness=policy_analysis.low_income_happiness_impact,
            predicted_middle_income_happiness=policy_analysis.middle_income_happiness_impact,
            predicted_high_income_happiness=policy_analysis.high_income_happiness_impact,
            predicted_progressive_support=policy_analysis.progressive_support,
            predicted_moderate_support=policy_analysis.moderate_support,
            predicted_conservative_support=policy_analysis.conservative_support,
            actual_low_income_happiness=actual_low,
            actual_middle_income_happiness=actual_middle,
            actual_high_income_happiness=actual_high,
            actual_progressive_support=actual_prog_support,
            actual_moderate_support=actual_mod_support,
            actual_conservative_support=actual_cons_support,
            happiness_error=happiness_error,
            support_error=support_error,
            confidence=policy_analysis.confidence,
            timestamp=datetime.now().isoformat(),
        )
        
        # Store and save
        self.feedback_history.append(feedback)
        self._save_feedback(feedback)
        
        logger.info(
            f"Collected feedback for '{feedback.policy_title}': "
            f"happiness_error={happiness_error:.3f}, support_error={support_error:.3f}"
        )
        
        return feedback
    
    def get_learning_metrics(self) -> LearningMetrics:
        """
        Calculate current learning metrics.
        
        Returns:
            Metrics showing learning progress
        """
        if len(self.feedback_history) == 0:
            return LearningMetrics(
                total_feedback_samples=0,
                avg_happiness_error=0.0,
                avg_support_error=0.0,
                improvement_rate=0.0,
            )
        
        # Calculate averages
        avg_happiness_error = sum(f.happiness_error for f in self.feedback_history) / len(self.feedback_history)
        avg_support_error = sum(f.support_error for f in self.feedback_history) / len(self.feedback_history)
        
        # Calculate improvement rate (compare recent vs old)
        improvement_rate = 0.0
        if len(self.feedback_history) >= 10:
            recent = self.feedback_history[-5:]
            old = self.feedback_history[:5]
            
            recent_avg = sum(f.happiness_error + f.support_error for f in recent) / len(recent)
            old_avg = sum(f.happiness_error + f.support_error for f in old) / len(old)
            
            if old_avg > 0:
                improvement_rate = (recent_avg - old_avg) / old_avg
        
        return LearningMetrics(
            total_feedback_samples=len(self.feedback_history),
            avg_happiness_error=avg_happiness_error,
            avg_support_error=avg_support_error,
            improvement_rate=improvement_rate,
        )
    
    def generate_improvement_prompt(self) -> str:
        """
        Generate a prompt for LLM to improve its predictions.
        
        This can be used to fine-tune the policy analyzer based on
        collected feedback.
        
        Returns:
            Prompt string with learning examples
        """
        if len(self.feedback_history) < 3:
            return ""
        
        # Get recent feedback with high errors
        recent_errors = sorted(
            self.feedback_history[-20:],
            key=lambda f: f.happiness_error + f.support_error,
            reverse=True,
        )[:5]
        
        prompt = "Based on these past prediction errors, improve your future predictions:\n\n"
        
        for i, feedback in enumerate(recent_errors, 1):
            prompt += f"Example {i}:\n"
            prompt += f"Policy: {feedback.policy_title}\n"
            prompt += f"Description: {feedback.policy_description[:100]}...\n"
            prompt += f"You predicted low-income happiness impact: {feedback.predicted_low_income_happiness:+.3f}\n"
            prompt += f"Actual impact was: {feedback.actual_low_income_happiness:+.3f}\n"
            prompt += f"Error: {abs(feedback.predicted_low_income_happiness - feedback.actual_low_income_happiness):.3f}\n"
            prompt += f"\n"
        
        prompt += "Adjust your predictions to better match actual outcomes.\n"
        
        return prompt
