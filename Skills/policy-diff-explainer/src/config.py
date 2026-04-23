"""
PolicyPulse - Configuration Management

Environment variable loading and application configuration.
Reference: TECH_STACK.md Section 11 (Security Considerations)

This module is imported by app.py only.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


# =============================================================================
# Path Configuration
# =============================================================================

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
LOGS_DIR = PROJECT_ROOT / "logs"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# File paths
TRAINING_DATA_PATH = DATA_DIR / "llm_training_samples.csv"
NN_MODEL_PATH = MODELS_DIR / "citizen_reaction_mlp.joblib"
FEATURE_SCALER_PATH = MODELS_DIR / "feature_scaler.joblib"
RL_MODEL_PATH = MODELS_DIR / "rl_agent.pkl"


# =============================================================================
# Environment Configuration
# =============================================================================

@dataclass(frozen=True)
class AppConfig:
    """
    Application configuration loaded from environment variables.
    
    All API keys and sensitive configuration should be loaded here.
    """
    nebius_api_key: str
    nebius_backup_keys: list[str]
    debug: bool
    log_file: Path | None
    default_population_size: int
    default_simulation_steps: int
    nn_min_training_samples: int

    @classmethod
    def from_env(cls) -> "AppConfig":
        """Load configuration from environment variables."""
        load_dotenv()
        
        primary_key = os.getenv("NEBIUS_API_KEY", "")
        
        # Collect backup keys (NEBIUS_API_KEY_2, NEBIUS_API_KEY_3, etc.)
        backup_keys: list[str] = []
        for i in range(2, 10):
            key = os.getenv(f"NEBIUS_API_KEY_{i}")
            if key:
                backup_keys.append(key)
        
        debug = os.getenv("DEBUG", "false").lower() == "true"
        
        # Optional log file
        log_file_str = os.getenv("LOG_FILE", "")
        log_file = Path(log_file_str) if log_file_str else None
        
        # Simulation defaults with environment overrides
        default_pop_size = int(os.getenv("DEFAULT_POPULATION_SIZE", "1000"))
        default_steps = int(os.getenv("DEFAULT_SIMULATION_STEPS", "5"))
        nn_min_samples = int(os.getenv("NN_MIN_TRAINING_SAMPLES", "500"))
        
        return cls(
            nebius_api_key=primary_key,
            nebius_backup_keys=backup_keys,
            debug=debug,
            log_file=log_file,
            default_population_size=default_pop_size,
            default_simulation_steps=default_steps,
            nn_min_training_samples=nn_min_samples,
        )

    @property
    def all_api_keys(self) -> list[str]:
        """Return all available API keys for rotation."""
        keys = []
        if self.nebius_api_key:
            keys.append(self.nebius_api_key)
        keys.extend(self.nebius_backup_keys)
        return keys

    @property
    def has_api_key(self) -> bool:
        """Check if at least one API key is configured."""
        return bool(self.nebius_api_key)

    def mask_key(self, key: str) -> str:
        """Return a masked version of an API key for logging."""
        if len(key) < 12:
            return "***"
        return f"{key[:8]}...{key[-4:]}"


# =============================================================================
# LLM Configuration
# =============================================================================

# Nebius API configuration (OpenAI-compatible endpoint)
# Reference: TECH_STACK.md Section 4
LLM_MIN_REQUEST_INTERVAL = 1.0  # seconds between requests
LLM_MODEL_NAME = "openai/gpt-oss-120b"
LLM_BASE_URL = "https://api.tokenfactory.nebius.com/v1/"

# =============================================================================
# Neural Network Configuration
# =============================================================================

# Reference: TECH_STACK.md Section 5
NN_HIDDEN_LAYERS = (64, 32)
NN_ACTIVATION = "relu"
NN_MAX_ITER = 500
NN_EARLY_STOPPING = True
NN_VALIDATION_FRACTION = 0.1
NN_MIN_SAMPLES = 500  # Minimum samples before training is allowed

# =============================================================================
# Population Configuration Limits
# =============================================================================

# Reference: PRD.md Feature F1
POPULATION_MIN_SIZE = 100
POPULATION_MAX_SIZE = 50_000
SIMULATION_MIN_STEPS = 1
SIMULATION_MAX_STEPS = 10
LLM_SAMPLE_SIZE_DEFAULT = 300


def get_config() -> AppConfig:
    """
    Get the application configuration.
    
    This is the main entry point for accessing configuration.
    Call this once at application startup.
    """
    return AppConfig.from_env()
