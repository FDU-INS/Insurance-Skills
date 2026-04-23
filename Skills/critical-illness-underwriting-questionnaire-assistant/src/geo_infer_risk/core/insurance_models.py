"""
Insurance Models for Risk Assessment

This module provides insurance modeling capabilities for risk assessment
and pricing in the GEO-INFER framework.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union, Any
from dataclasses import dataclass, field
import logging
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

@dataclass
class InsuranceConfig:
    """Configuration for insurance models."""
    
    # General parameters
    currency: str = 'USD'
    risk_free_rate: float = 0.02
    inflation_rate: float = 0.025
    
    # Pricing parameters
    profit_margin: float = 0.15
    expense_ratio: float = 0.25
    loss_ratio_target: float = 0.65
    
    # Risk parameters
    confidence_level: float = 0.95
    max_retention: float = 1000000.0
    
    # Reinsurance parameters
    reinsurance_attachment: float = 500000.0
    reinsurance_limit: float = 5000000.0
    reinsurance_rate: float = 0.10

class InsuranceModel(ABC):
    """Abstract base class for insurance models."""
    
    def __init__(self, config: Optional[InsuranceConfig] = None):
        """
        Initialize insurance model.
        
        Args:
            config: Insurance configuration
        """
        self.config = config or InsuranceConfig()
        self.is_fitted = False
        self.historical_data = None
    
    @abstractmethod
    def fit(self, historical_data: pd.DataFrame) -> 'InsuranceModel':
        """Fit the model to historical data."""
        pass
    
    @abstractmethod
    def calculate_premium(self, risk_profile: Dict[str, Any]) -> float:
        """Calculate insurance premium."""
        pass
    
    @abstractmethod
    def estimate_losses(self, risk_profile: Dict[str, Any]) -> Dict[str, float]:
        """Estimate potential losses."""
        pass

class PropertyInsuranceModel(InsuranceModel):
    """Property insurance model."""
    
    def __init__(self, config: Optional[InsuranceConfig] = None):
        super().__init__(config)
        self.risk_factors = {}
        self.base_rates = {}
    
    def fit(self, historical_data: pd.DataFrame) -> 'PropertyInsuranceModel':
        """Fit property insurance model to historical data."""
        logger.info("Fitting property insurance model...")
        
        self.historical_data = historical_data.copy()
        
        # Calculate base rates by property type
        if 'property_type' in historical_data.columns:
            type_stats = historical_data.groupby('property_type').agg({
                'loss_amount': ['mean', 'std', 'count'],
                'premium': 'mean'
            }).to_dict()
            self.base_rates = type_stats
        
        # Calculate risk factors
        self._calculate_risk_factors()
        
        self.is_fitted = True
        logger.info("Property insurance model fitted successfully")
        return self
    
    def _calculate_risk_factors(self):
        """Calculate risk factors from historical data."""
        if self.historical_data is None:
            return
        
        # Location risk factors
        if 'location' in self.historical_data.columns:
            location_stats = self.historical_data.groupby('location').agg({
                'loss_amount': 'mean',
                'claim_frequency': 'mean'
            })
            self.risk_factors['location'] = location_stats.to_dict()
        
        # Construction type risk factors
        if 'construction_type' in self.historical_data.columns:
            construction_stats = self.historical_data.groupby('construction_type').agg({
                'loss_amount': 'mean',
                'claim_frequency': 'mean'
            })
            self.risk_factors['construction'] = construction_stats.to_dict()
    
    def calculate_premium(self, risk_profile: Dict[str, Any]) -> float:
        """Calculate property insurance premium."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before premium calculation")
        
        # Base premium calculation
        property_value = risk_profile.get('property_value', 200000)
        property_type = risk_profile.get('property_type', 'residential')
        
        # Base rate (per $1000 of coverage)
        base_rate = self.base_rates.get(property_type, {}).get(('premium', 'mean'), 0.005)
        base_premium = property_value * base_rate
        
        # Apply risk factors
        location_factor = self._get_location_factor(risk_profile.get('location', 'unknown'))
        construction_factor = self._get_construction_factor(risk_profile.get('construction_type', 'frame'))
        age_factor = self._get_age_factor(risk_profile.get('property_age', 20))
        safety_factor = self._get_safety_factor(risk_profile.get('safety_features', []))
        
        # Calculate final premium
        premium = base_premium * location_factor * construction_factor * age_factor * safety_factor
        
        # Apply expense and profit loading
        premium = premium * (1 + self.config.expense_ratio + self.config.profit_margin)
        
        return premium
    
    def estimate_losses(self, risk_profile: Dict[str, Any]) -> Dict[str, float]:
        """Estimate potential property losses."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before loss estimation")
        
        property_value = risk_profile.get('property_value', 200000)
        property_type = risk_profile.get('property_type', 'residential')
        
        # Base loss estimates
        base_loss_rate = self.base_rates.get(property_type, {}).get(('loss_amount', 'mean'), 0.02)
        base_loss = property_value * base_loss_rate
        
        # Apply risk factors
        location_factor = self._get_location_factor(risk_profile.get('location', 'unknown'))
        construction_factor = self._get_construction_factor(risk_profile.get('construction_type', 'frame'))
        
        expected_loss = base_loss * location_factor * construction_factor
        
        # Calculate loss distribution
        loss_std = self.base_rates.get(property_type, {}).get(('loss_amount', 'std'), expected_loss * 0.5)
        
        # Calculate VaR and CVaR
        var_95 = expected_loss + 1.645 * loss_std
        cvar_95 = expected_loss + 2.063 * loss_std
        
        return {
            'expected_loss': expected_loss,
            'var_95': var_95,
            'cvar_95': cvar_95,
            'max_loss': property_value
        }
    
    def _get_location_factor(self, location: str) -> float:
        """Get location risk factor."""
        location_factors = {
            'low_risk': 0.8,
            'medium_risk': 1.0,
            'high_risk': 1.5,
            'coastal': 1.8,
            'wildfire_prone': 2.0,
            'flood_zone': 2.5
        }
        return location_factors.get(location, 1.0)
    
    def _get_construction_factor(self, construction_type: str) -> float:
        """Get construction type risk factor."""
        construction_factors = {
            'fire_resistive': 0.7,
            'non_combustible': 0.8,
            'ordinary': 1.0,
            'heavy_timber': 1.2,
            'frame': 1.5
        }
        return construction_factors.get(construction_type, 1.0)
    
    def _get_age_factor(self, age: int) -> float:
        """Get property age risk factor."""
        if age < 5:
            return 0.9
        elif age < 20:
            return 1.0
        elif age < 50:
            return 1.2
        else:
            return 1.5
    
    def _get_safety_factor(self, safety_features: List[str]) -> float:
        """Get safety features discount factor."""
        base_factor = 1.0
        
        for feature in safety_features:
            if feature == 'sprinkler_system':
                base_factor *= 0.9
            elif feature == 'alarm_system':
                base_factor *= 0.95
            elif feature == 'fire_extinguishers':
                base_factor *= 0.98
            elif feature == 'security_system':
                base_factor *= 0.97
        
        return base_factor

class LiabilityInsuranceModel(InsuranceModel):
    """Liability insurance model."""
    
    def __init__(self, config: Optional[InsuranceConfig] = None):
        super().__init__(config)
        self.liability_limits = {}
        self.claim_frequencies = {}
    
    def fit(self, historical_data: pd.DataFrame) -> 'LiabilityInsuranceModel':
        """Fit liability insurance model to historical data."""
        logger.info("Fitting liability insurance model...")
        
        self.historical_data = historical_data.copy()
        
        # Calculate claim frequencies by business type
        if 'business_type' in historical_data.columns:
            business_stats = historical_data.groupby('business_type').agg({
                'claim_frequency': 'mean',
                'claim_severity': 'mean',
                'premium': 'mean'
            }).to_dict()
            self.claim_frequencies = business_stats
        
        self.is_fitted = True
        logger.info("Liability insurance model fitted successfully")
        return self
    
    def calculate_premium(self, risk_profile: Dict[str, Any]) -> float:
        """Calculate liability insurance premium."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before premium calculation")
        
        # Base premium calculation
        liability_limit = risk_profile.get('liability_limit', 1000000)
        business_type = risk_profile.get('business_type', 'general')
        annual_revenue = risk_profile.get('annual_revenue', 1000000)
        
        # Base rate per $1000 of coverage
        base_rate = self.claim_frequencies.get(business_type, {}).get(('premium', 'mean'), 0.001)
        base_premium = liability_limit * base_rate
        
        # Apply business factors
        revenue_factor = self._get_revenue_factor(annual_revenue)
        experience_factor = self._get_experience_factor(risk_profile.get('claims_history', []))
        safety_factor = self._get_safety_factor(risk_profile.get('safety_programs', []))
        
        # Calculate final premium
        premium = base_premium * revenue_factor * experience_factor * safety_factor
        
        # Apply expense and profit loading
        premium = premium * (1 + self.config.expense_ratio + self.config.profit_margin)
        
        return premium
    
    def estimate_losses(self, risk_profile: Dict[str, Any]) -> Dict[str, float]:
        """Estimate potential liability losses."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before loss estimation")
        
        liability_limit = risk_profile.get('liability_limit', 1000000)
        business_type = risk_profile.get('business_type', 'general')
        
        # Base loss estimates
        claim_frequency = self.claim_frequencies.get(business_type, {}).get(('claim_frequency', 'mean'), 0.01)
        claim_severity = self.claim_frequencies.get(business_type, {}).get(('claim_severity', 'mean'), 50000)
        
        expected_loss = claim_frequency * claim_severity
        
        # Calculate loss distribution
        loss_std = claim_severity * 0.8  # Assume 80% coefficient of variation
        
        # Calculate VaR and CVaR
        var_95 = expected_loss + 1.645 * loss_std
        cvar_95 = expected_loss + 2.063 * loss_std
        
        return {
            'expected_loss': expected_loss,
            'var_95': var_95,
            'cvar_95': cvar_95,
            'max_loss': liability_limit
        }
    
    def _get_revenue_factor(self, annual_revenue: float) -> float:
        """Get revenue-based risk factor."""
        if annual_revenue < 100000:
            return 0.8
        elif annual_revenue < 1000000:
            return 1.0
        elif annual_revenue < 10000000:
            return 1.2
        else:
            return 1.5
    
    def _get_experience_factor(self, claims_history: List[Dict[str, Any]]) -> float:
        """Get claims experience factor."""
        if not claims_history:
            return 1.0
        
        # Calculate experience modifier
        total_claims = len(claims_history)
        total_losses = sum(claim.get('amount', 0) for claim in claims_history)
        
        if total_claims == 0:
            return 0.9  # No claims discount
        
        avg_loss = total_losses / total_claims
        
        # Experience modifier based on loss ratio
        expected_loss_ratio = 0.6
        actual_loss_ratio = total_losses / (1000000 * 0.01)  # Assume $1M premium
        
        if actual_loss_ratio < expected_loss_ratio * 0.8:
            return 0.8  # Good experience discount
        elif actual_loss_ratio > expected_loss_ratio * 1.2:
            return 1.3  # Poor experience surcharge
        else:
            return 1.0
    
    def _get_safety_factor(self, safety_programs: List[str]) -> float:
        """Get safety program discount factor."""
        base_factor = 1.0
        
        for program in safety_programs:
            if program == 'safety_training':
                base_factor *= 0.95
            elif program == 'risk_management':
                base_factor *= 0.92
            elif program == 'safety_audits':
                base_factor *= 0.94
            elif program == 'incident_investigation':
                base_factor *= 0.96
        
        return base_factor

class CatastropheInsuranceModel(InsuranceModel):
    """Catastrophe insurance model."""
    
    def __init__(self, config: Optional[InsuranceConfig] = None):
        super().__init__(config)
        self.catastrophe_models = {}
        self.exposure_data = {}
    
    def fit(self, historical_data: pd.DataFrame) -> 'CatastropheInsuranceModel':
        """Fit catastrophe insurance model to historical data."""
        logger.info("Fitting catastrophe insurance model...")
        
        self.historical_data = historical_data.copy()
        
        # Initialize catastrophe models
        self.catastrophe_models = {
            'hurricane': self._hurricane_model,
            'earthquake': self._earthquake_model,
            'flood': self._flood_model,
            'wildfire': self._wildfire_model
        }
        
        self.is_fitted = True
        logger.info("Catastrophe insurance model fitted successfully")
        return self
    
    def calculate_premium(self, risk_profile: Dict[str, Any]) -> float:
        """Calculate catastrophe insurance premium."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before premium calculation")
        
        # Base premium calculation
        coverage_limit = risk_profile.get('coverage_limit', 1000000)
        location = risk_profile.get('location', {'lat': 0, 'lon': 0})
        catastrophe_types = risk_profile.get('catastrophe_types', ['hurricane'])
        
        total_premium = 0
        
        for cat_type in catastrophe_types:
            if cat_type in self.catastrophe_models:
                cat_premium = self.catastrophe_models[cat_type](coverage_limit, location)
                total_premium += cat_premium
        
        # Apply reinsurance costs
        reinsurance_cost = self._calculate_reinsurance_cost(total_premium, coverage_limit)
        total_premium += reinsurance_cost
        
        # Apply expense and profit loading
        total_premium = total_premium * (1 + self.config.expense_ratio + self.config.profit_margin)
        
        return total_premium
    
    def estimate_losses(self, risk_profile: Dict[str, Any]) -> Dict[str, float]:
        """Estimate potential catastrophe losses."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before loss estimation")
        
        coverage_limit = risk_profile.get('coverage_limit', 1000000)
        location = risk_profile.get('location', {'lat': 0, 'lon': 0})
        catastrophe_types = risk_profile.get('catastrophe_types', ['hurricane'])
        
        total_expected_loss = 0
        max_loss = 0
        
        for cat_type in catastrophe_types:
            if cat_type in self.catastrophe_models:
                cat_loss = self._estimate_catastrophe_loss(cat_type, coverage_limit, location)
                total_expected_loss += cat_loss['expected_loss']
                max_loss = max(max_loss, cat_loss['max_loss'])
        
        return {
            'expected_loss': total_expected_loss,
            'var_95': total_expected_loss * 2.0,  # Simplified VaR
            'cvar_95': total_expected_loss * 3.0,  # Simplified CVaR
            'max_loss': max_loss
        }
    
    def _hurricane_model(self, coverage_limit: float, location: Dict[str, float]) -> float:
        """Hurricane catastrophe model."""
        # Simplified hurricane model
        lat = location.get('lat', 0)
        
        # Hurricane risk by latitude
        if 25 <= lat <= 35:  # High risk zone
            base_rate = 0.02
        elif 20 <= lat <= 40:  # Medium risk zone
            base_rate = 0.01
        else:  # Low risk zone
            base_rate = 0.005
        
        return coverage_limit * base_rate
    
    def _earthquake_model(self, coverage_limit: float, location: Dict[str, float]) -> float:
        """Earthquake catastrophe model."""
        # Simplified earthquake model
        lat = location.get('lat', 0)
        lon = location.get('lon', 0)
        
        # Earthquake risk by location (simplified)
        if abs(lat) < 30:  # Tropical/subtropical regions
            base_rate = 0.015
        elif abs(lat) < 60:  # Temperate regions
            base_rate = 0.01
        else:  # Polar regions
            base_rate = 0.005
        
        return coverage_limit * base_rate
    
    def _flood_model(self, coverage_limit: float, location: Dict[str, float]) -> float:
        """Flood catastrophe model."""
        # Simplified flood model
        lat = location.get('lat', 0)
        
        # Flood risk by elevation (simplified by latitude)
        if abs(lat) < 30:  # Coastal/low elevation
            base_rate = 0.025
        elif abs(lat) < 60:  # Mid-latitudes
            base_rate = 0.015
        else:  # High latitudes
            base_rate = 0.005
        
        return coverage_limit * base_rate
    
    def _wildfire_model(self, coverage_limit: float, location: Dict[str, float]) -> float:
        """Wildfire catastrophe model."""
        # Simplified wildfire model
        lat = location.get('lat', 0)
        
        # Wildfire risk by climate zone
        if 30 <= abs(lat) <= 45:  # Mediterranean climate
            base_rate = 0.02
        elif 45 <= abs(lat) <= 60:  # Boreal forest
            base_rate = 0.015
        else:  # Other regions
            base_rate = 0.005
        
        return coverage_limit * base_rate
    
    def _estimate_catastrophe_loss(self, 
                                 cat_type: str,
                                 coverage_limit: float,
                                 location: Dict[str, float]) -> Dict[str, float]:
        """Estimate loss for a specific catastrophe type."""
        if cat_type == 'hurricane':
            expected_loss = coverage_limit * 0.01
        elif cat_type == 'earthquake':
            expected_loss = coverage_limit * 0.008
        elif cat_type == 'flood':
            expected_loss = coverage_limit * 0.012
        elif cat_type == 'wildfire':
            expected_loss = coverage_limit * 0.015
        else:
            expected_loss = coverage_limit * 0.01
        
        return {
            'expected_loss': expected_loss,
            'max_loss': coverage_limit
        }
    
    def _calculate_reinsurance_cost(self, base_premium: float, coverage_limit: float) -> float:
        """Calculate reinsurance cost."""
        if coverage_limit <= self.config.reinsurance_attachment:
            return 0.0
        
        reinsurance_coverage = min(coverage_limit - self.config.reinsurance_attachment, 
                                 self.config.reinsurance_limit)
        
        return reinsurance_coverage * self.config.reinsurance_rate

class InsuranceManager:
    """Manager for multiple insurance models."""
    
    def __init__(self, config: Optional[InsuranceConfig] = None):
        """
        Initialize insurance manager.
        
        Args:
            config: Configuration for insurance models
        """
        self.config = config or InsuranceConfig()
        self.models = {}
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize all insurance models."""
        self.models = {
            'property': PropertyInsuranceModel(self.config),
            'liability': LiabilityInsuranceModel(self.config),
            'catastrophe': CatastropheInsuranceModel(self.config)
        }
        
        logger.info(f"Initialized {len(self.models)} insurance models")
    
    def fit_model(self, model_type: str, historical_data: pd.DataFrame) -> bool:
        """
        Fit a specific insurance model.
        
        Args:
            model_type: Type of insurance model
            historical_data: Historical insurance data
            
        Returns:
            True if fitting was successful
        """
        if model_type not in self.models:
            logger.error(f"Unknown model type: {model_type}")
            return False
        
        try:
            self.models[model_type].fit(historical_data)
            return True
        except Exception as e:
            logger.error(f"Failed to fit {model_type} model: {e}")
            return False
    
    def calculate_premium(self, 
                         model_type: str,
                         risk_profile: Dict[str, Any]) -> float:
        """
        Calculate insurance premium.
        
        Args:
            model_type: Type of insurance model
            risk_profile: Risk profile information
            
        Returns:
            Calculated premium
        """
        if model_type not in self.models:
            raise ValueError(f"Unknown model type: {model_type}")
        
        model = self.models[model_type]
        if not model.is_fitted:
            raise ValueError(f"{model_type} model must be fitted before premium calculation")
        
        return model.calculate_premium(risk_profile)
    
    def estimate_losses(self, 
                       model_type: str,
                       risk_profile: Dict[str, Any]) -> Dict[str, float]:
        """
        Estimate potential losses.
        
        Args:
            model_type: Type of insurance model
            risk_profile: Risk profile information
            
        Returns:
            Loss estimates
        """
        if model_type not in self.models:
            raise ValueError(f"Unknown model type: {model_type}")
        
        model = self.models[model_type]
        if not model.is_fitted:
            raise ValueError(f"{model_type} model must be fitted before loss estimation")
        
        return model.estimate_losses(risk_profile)
    
    def generate_quote(self, 
                      risk_profile: Dict[str, Any],
                      coverage_types: List[str]) -> Dict[str, Any]:
        """
        Generate comprehensive insurance quote.
        
        Args:
            risk_profile: Risk profile information
            coverage_types: Types of coverage requested
            
        Returns:
            Insurance quote
        """
        quote = {
            'risk_profile': risk_profile,
            'coverage_types': coverage_types,
            'premiums': {},
            'loss_estimates': {},
            'total_premium': 0.0
        }
        
        for coverage_type in coverage_types:
            if coverage_type in self.models:
                try:
                    premium = self.calculate_premium(coverage_type, risk_profile)
                    losses = self.estimate_losses(coverage_type, risk_profile)
                    
                    quote['premiums'][coverage_type] = premium
                    quote['loss_estimates'][coverage_type] = losses
                    quote['total_premium'] += premium
                    
                except Exception as e:
                    logger.error(f"Failed to calculate {coverage_type} premium: {e}")
                    quote['premiums'][coverage_type] = 0.0
                    quote['loss_estimates'][coverage_type] = {}
        
        return quote

# Convenience functions
def create_insurance_manager(config: Optional[InsuranceConfig] = None) -> InsuranceManager:
    """Create a new insurance manager."""
    return InsuranceManager(config)

def calculate_property_premium(property_value: float,
                             property_type: str = 'residential',
                             location: str = 'medium_risk') -> float:
    """Calculate property insurance premium."""
    config = InsuranceConfig()
    manager = InsuranceManager(config)
    
    # Create dummy historical data for fitting
    historical_data = pd.DataFrame({
        'property_type': [property_type],
        'property_value': [property_value],
        'loss_amount': [property_value * 0.02],
        'premium': [property_value * 0.005],
        'location': [location],
        'claim_frequency': [0.01]
    })
    
    manager.fit_model('property', historical_data)
    
    risk_profile = {
        'property_value': property_value,
        'property_type': property_type,
        'location': location
    }
    
    return manager.calculate_premium('property', risk_profile) 