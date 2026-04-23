"""Skill Registry for automatic skill resolution.

This module provides automatic mapping between clinical conditions/domains
and the skills that provide their clinical codes and parameters.

Instead of explicitly referencing skills in every journey event:

    "parameters": {"skill_ref": {"skill": "diabetes-management", ...}}

Journey templates can simply specify a condition:

    "condition": "diabetes"

The SkillRegistry automatically finds the appropriate skill and resolves
the needed parameters based on the event type.

Usage:
    from healthsim.generation.skill_registry import (
        SkillRegistry,
        get_skill_registry,
        auto_resolve_parameters,
    )
    
    # Auto-resolve based on event type and condition
    params = auto_resolve_parameters(
        event_type="diagnosis",
        condition="diabetes",
        entity={"control_status": "moderate"}
    )
    # Returns: {"icd10": "E11.9", "description": "Type 2 diabetes..."}
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


# =============================================================================
# Skill Capability Declarations
# =============================================================================

class SkillCapability(str, Enum):
    """What a skill can provide for event resolution."""
    
    DIAGNOSIS = "diagnosis"           # ICD-10 codes
    MEDICATION = "medication"         # RxNorm codes  
    LAB_ORDER = "lab_order"          # LOINC codes
    PROCEDURE = "procedure"          # CPT/HCPCS codes
    ENCOUNTER = "encounter"          # Encounter parameters
    REFERRAL = "referral"            # Referral parameters


class SkillCapabilityDeclaration(BaseModel):
    """Declaration of what a skill provides."""
    
    capability: SkillCapability
    lookup_key: str = ""  # Key to use when resolving (e.g., "diagnosis_code")
    description: str = ""


class SkillRegistration(BaseModel):
    """A skill's registration in the registry."""
    
    skill_name: str
    conditions: list[str] = Field(default_factory=list)  # Trigger conditions
    aliases: list[str] = Field(default_factory=list)     # Alternative names
    capabilities: list[SkillCapabilityDeclaration] = Field(default_factory=list)
    products: list[str] = Field(default_factory=list)    # Applicable products
    priority: int = 0  # Higher priority wins if multiple skills match


# =============================================================================
# Default Skill Registrations
# =============================================================================

# These map conditions to skills and declare what each skill provides
DEFAULT_REGISTRATIONS: list[dict[str, Any]] = [
    # Diabetes
    {
        "skill_name": "diabetes-management",
        "conditions": ["diabetes", "t2dm", "type 2 diabetes", "diabetic", "dm2"],
        "aliases": ["diabetes", "t2dm"],
        "capabilities": [
            {"capability": "diagnosis", "lookup_key": "diagnosis_code"},
            {"capability": "medication", "lookup_key": "first_line_medication"},
            {"capability": "lab_order", "lookup_key": "lab_order"},
        ],
        "products": ["patientsim", "membersim", "rxmembersim"],
        "priority": 10,
    },
    # Chronic Kidney Disease
    {
        "skill_name": "chronic-kidney-disease",
        "conditions": ["ckd", "chronic kidney disease", "renal disease", "kidney disease"],
        "aliases": ["ckd", "renal"],
        "capabilities": [
            {"capability": "diagnosis", "lookup_key": "diagnosis_code"},
            {"capability": "medication", "lookup_key": "medication"},
            {"capability": "lab_order", "lookup_key": "lab_order"},
        ],
        "products": ["patientsim", "membersim"],
        "priority": 10,
    },
    # Heart Failure
    {
        "skill_name": "heart-failure",
        "conditions": ["heart failure", "hf", "chf", "congestive heart failure", "hfref", "hfpef"],
        "aliases": ["heart-failure", "chf"],
        "capabilities": [
            {"capability": "diagnosis", "lookup_key": "diagnosis_code"},
            {"capability": "medication", "lookup_key": "first_line_medication"},
            {"capability": "lab_order", "lookup_key": "lab_order"},
            {"capability": "procedure", "lookup_key": "procedure"},
        ],
        "products": ["patientsim", "membersim"],
        "priority": 10,
    },
    # Hypertension
    {
        "skill_name": "hypertension",
        "conditions": ["hypertension", "htn", "high blood pressure", "elevated bp"],
        "aliases": ["hypertension", "htn"],
        "capabilities": [
            {"capability": "diagnosis", "lookup_key": "diagnosis_code"},
            {"capability": "medication", "lookup_key": "medication"},
        ],
        "products": ["patientsim", "membersim", "rxmembersim"],
        "priority": 10,
    },
    # COPD
    {
        "skill_name": "copd",
        "conditions": ["copd", "chronic obstructive pulmonary disease", "emphysema", "chronic bronchitis"],
        "aliases": ["copd", "lung-disease"],
        "capabilities": [
            {"capability": "diagnosis", "lookup_key": "diagnosis_code"},
            {"capability": "medication", "lookup_key": "medication"},
        ],
        "products": ["patientsim", "membersim"],
        "priority": 10,
    },
    # Asthma
    {
        "skill_name": "asthma",
        "conditions": ["asthma", "reactive airway", "bronchospasm"],
        "aliases": ["asthma"],
        "capabilities": [
            {"capability": "diagnosis", "lookup_key": "diagnosis_code"},
            {"capability": "medication", "lookup_key": "medication"},
        ],
        "products": ["patientsim", "membersim", "rxmembersim"],
        "priority": 10,
    },
    # Depression
    {
        "skill_name": "depression",
        "conditions": ["depression", "mdd", "major depressive disorder", "depressive episode"],
        "aliases": ["depression", "mdd"],
        "capabilities": [
            {"capability": "diagnosis", "lookup_key": "diagnosis_code"},
            {"capability": "medication", "lookup_key": "medication"},
        ],
        "products": ["patientsim", "membersim"],
        "priority": 10,
    },
    # Anxiety
    {
        "skill_name": "anxiety",
        "conditions": ["anxiety", "gad", "generalized anxiety", "panic disorder"],
        "aliases": ["anxiety", "gad"],
        "capabilities": [
            {"capability": "diagnosis", "lookup_key": "diagnosis_code"},
            {"capability": "medication", "lookup_key": "medication"},
        ],
        "products": ["patientsim", "membersim"],
        "priority": 10,
    },
    # Preventive Care (wellness visits, screenings)
    {
        "skill_name": "preventive-care",
        "conditions": ["wellness", "preventive", "screening", "annual physical", "checkup"],
        "aliases": ["wellness", "preventive"],
        "capabilities": [
            {"capability": "encounter", "lookup_key": "encounter_type"},
            {"capability": "procedure", "lookup_key": "screening"},
        ],
        "products": ["patientsim", "membersim"],
        "priority": 5,
    },
    # Clinical Trial (TrialSim specific)
    {
        "skill_name": "clinical-trial-protocol",
        "conditions": ["clinical trial", "study", "protocol", "phase 3", "phase 2", "pivotal"],
        "aliases": ["trial", "study"],
        "capabilities": [
            {"capability": "encounter", "lookup_key": "visit_schedule"},
            {"capability": "procedure", "lookup_key": "study_procedure"},
            {"capability": "lab_order", "lookup_key": "study_labs"},
        ],
        "products": ["trialsim"],
        "priority": 10,
    },
]


# =============================================================================
# Skill Registry
# =============================================================================

class SkillRegistry:
    """Registry mapping conditions to skills for auto-resolution.
    
    The registry maintains a mapping of clinical conditions to the skills
    that can resolve their parameters. When a journey event specifies a
    condition, the registry finds the appropriate skill and resolves
    parameters based on the event type.
    
    Example:
        >>> registry = SkillRegistry()
        >>> skill = registry.find_skill_for_condition("diabetes")
        >>> print(skill.skill_name)
        'diabetes-management'
        
        >>> params = registry.resolve_for_event(
        ...     event_type="diagnosis",
        ...     condition="diabetes",
        ...     entity={"control_status": "moderate"}
        ... )
        >>> print(params)
        {'icd10': 'E11.9', 'description': 'Type 2 diabetes...'}
    """
    
    def __init__(self) -> None:
        """Initialize the registry with default registrations."""
        self._registrations: dict[str, SkillRegistration] = {}
        self._condition_index: dict[str, list[str]] = {}  # condition -> skill_names
        self._skill_resolver = None  # Lazy loaded
        
        # Load default registrations
        for reg_dict in DEFAULT_REGISTRATIONS:
            self.register(SkillRegistration(**reg_dict))
    
    def register(self, registration: SkillRegistration) -> None:
        """Register a skill with its conditions and capabilities.
        
        Args:
            registration: The skill registration
        """
        self._registrations[registration.skill_name] = registration
        
        # Index by conditions
        for condition in registration.conditions:
            normalized = self._normalize_condition(condition)
            if normalized not in self._condition_index:
                self._condition_index[normalized] = []
            if registration.skill_name not in self._condition_index[normalized]:
                self._condition_index[normalized].append(registration.skill_name)
        
        # Index by aliases
        for alias in registration.aliases:
            normalized = self._normalize_condition(alias)
            if normalized not in self._condition_index:
                self._condition_index[normalized] = []
            if registration.skill_name not in self._condition_index[normalized]:
                self._condition_index[normalized].append(registration.skill_name)
    
    def _normalize_condition(self, condition: str) -> str:
        """Normalize a condition string for matching."""
        return condition.lower().strip().replace("-", " ").replace("_", " ")
    
    def find_skill_for_condition(
        self,
        condition: str,
        product: str | None = None,
    ) -> SkillRegistration | None:
        """Find the best skill for a given condition.
        
        Args:
            condition: The clinical condition (e.g., "diabetes", "ckd")
            product: Optional product filter (e.g., "patientsim")
            
        Returns:
            Best matching SkillRegistration, or None if not found
        """
        normalized = self._normalize_condition(condition)
        
        # Direct match
        if normalized in self._condition_index:
            candidates = self._condition_index[normalized]
        else:
            # Partial match
            candidates = []
            for cond, skills in self._condition_index.items():
                if normalized in cond or cond in normalized:
                    candidates.extend(skills)
        
        if not candidates:
            return None
        
        # Filter by product if specified
        if product:
            candidates = [
                name for name in candidates
                if product in self._registrations[name].products
            ]
        
        if not candidates:
            return None
        
        # Return highest priority
        best = max(
            candidates,
            key=lambda name: self._registrations[name].priority
        )
        return self._registrations[best]
    
    def get_capability_lookup(
        self,
        skill_name: str,
        capability: SkillCapability | str,
    ) -> str | None:
        """Get the lookup key for a skill's capability.
        
        Args:
            skill_name: Name of the skill
            capability: The capability to look up
            
        Returns:
            Lookup key string, or None if not found
        """
        if skill_name not in self._registrations:
            return None
        
        reg = self._registrations[skill_name]
        cap_str = capability.value if isinstance(capability, SkillCapability) else capability
        
        for cap in reg.capabilities:
            if cap.capability.value == cap_str:
                return cap.lookup_key
        
        return None
    
    def _get_skill_resolver(self):
        """Lazy load the SkillResolver."""
        if self._skill_resolver is None:
            from healthsim.generation.skill_reference import SkillResolver
            self._skill_resolver = SkillResolver()
        return self._skill_resolver
    
    def resolve_for_event(
        self,
        event_type: str,
        condition: str,
        entity: dict[str, Any] | None = None,
        product: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Resolve parameters for an event based on condition.
        
        This is the main entry point for automatic skill resolution.
        Given an event type and condition, it finds the appropriate
        skill and resolves the parameters.
        
        Args:
            event_type: Type of event (diagnosis, medication_order, lab_order, etc.)
            condition: Clinical condition (diabetes, ckd, etc.)
            entity: Entity attributes for variable substitution
            product: Optional product filter
            context: Additional context for resolution
            
        Returns:
            Resolved parameters dict
            
        Example:
            >>> params = registry.resolve_for_event(
            ...     event_type="diagnosis",
            ...     condition="diabetes",
            ...     entity={"control_status": "poorly-controlled"}
            ... )
            >>> print(params["icd10"])
            'E11.65'
        """
        # Find the skill
        registration = self.find_skill_for_condition(condition, product)
        if not registration:
            return {}
        
        # Map event type to capability
        capability = self._event_type_to_capability(event_type)
        if not capability:
            return {}
        
        # Get the lookup key for this capability
        lookup_key = self.get_capability_lookup(registration.skill_name, capability)
        if not lookup_key:
            # Try to use the capability name as lookup key
            lookup_key = capability.value
        
        # Resolve using SkillResolver
        resolver = self._get_skill_resolver()
        
        from healthsim.generation.skill_reference import SkillReference
        
        skill_ref = SkillReference(
            skill=registration.skill_name,
            lookup=lookup_key,
            context=context or {},
        )
        
        result = resolver.resolve(skill_ref, entity or {})
        return result.parameters
    
    def _event_type_to_capability(self, event_type: str) -> SkillCapability | None:
        """Map an event type to a skill capability."""
        mapping = {
            "diagnosis": SkillCapability.DIAGNOSIS,
            "medication_order": SkillCapability.MEDICATION,
            "medication": SkillCapability.MEDICATION,
            "fill": SkillCapability.MEDICATION,
            "refill": SkillCapability.MEDICATION,
            "lab_order": SkillCapability.LAB_ORDER,
            "lab": SkillCapability.LAB_ORDER,
            "procedure": SkillCapability.PROCEDURE,
            "encounter": SkillCapability.ENCOUNTER,
            "visit": SkillCapability.ENCOUNTER,
            "scheduled_visit": SkillCapability.ENCOUNTER,
            "referral": SkillCapability.REFERRAL,
        }
        return mapping.get(event_type.lower())
    
    def list_conditions(self) -> list[str]:
        """List all registered conditions."""
        return sorted(self._condition_index.keys())
    
    def list_skills(self) -> list[str]:
        """List all registered skills."""
        return sorted(self._registrations.keys())
    
    def get_registration(self, skill_name: str) -> SkillRegistration | None:
        """Get a skill's registration."""
        return self._registrations.get(skill_name)


# =============================================================================
# Global Registry Instance
# =============================================================================

_skill_registry: SkillRegistry | None = None


def get_skill_registry() -> SkillRegistry:
    """Get the global skill registry instance.
    
    Returns:
        The global SkillRegistry
    """
    global _skill_registry
    if _skill_registry is None:
        _skill_registry = SkillRegistry()
    return _skill_registry


def auto_resolve_parameters(
    event_type: str,
    condition: str,
    entity: dict[str, Any] | None = None,
    product: str | None = None,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Convenience function for auto-resolving event parameters.
    
    Args:
        event_type: Type of event (diagnosis, medication_order, etc.)
        condition: Clinical condition (diabetes, ckd, etc.)
        entity: Entity attributes for variable substitution
        product: Optional product filter
        context: Additional context for resolution
        
    Returns:
        Resolved parameters dict
        
    Example:
        >>> params = auto_resolve_parameters(
        ...     event_type="diagnosis",
        ...     condition="diabetes"
        ... )
        >>> print(params["icd10"])
        'E11.9'
    """
    registry = get_skill_registry()
    return registry.resolve_for_event(
        event_type=event_type,
        condition=condition,
        entity=entity,
        product=product,
        context=context,
    )


def register_skill(
    skill_name: str,
    conditions: list[str],
    capabilities: list[dict[str, str]],
    products: list[str] | None = None,
    aliases: list[str] | None = None,
    priority: int = 0,
) -> None:
    """Register a skill in the global registry.
    
    Args:
        skill_name: Name of the skill
        conditions: List of conditions this skill handles
        capabilities: List of capability dicts with 'capability' and 'lookup_key'
        products: List of applicable products
        aliases: Alternative names for the skill
        priority: Priority for conflict resolution
        
    Example:
        >>> register_skill(
        ...     skill_name="my-condition-skill",
        ...     conditions=["my condition", "my-condition"],
        ...     capabilities=[
        ...         {"capability": "diagnosis", "lookup_key": "diagnosis_code"}
        ...     ],
        ...     products=["patientsim"]
        ... )
    """
    registry = get_skill_registry()
    
    cap_declarations = [
        SkillCapabilityDeclaration(
            capability=SkillCapability(cap["capability"]),
            lookup_key=cap.get("lookup_key", ""),
        )
        for cap in capabilities
    ]
    
    registration = SkillRegistration(
        skill_name=skill_name,
        conditions=conditions,
        aliases=aliases or [],
        capabilities=cap_declarations,
        products=products or ["patientsim", "membersim"],
        priority=priority,
    )
    
    registry.register(registration)


__all__ = [
    "SkillCapability",
    "SkillCapabilityDeclaration", 
    "SkillRegistration",
    "SkillRegistry",
    "get_skill_registry",
    "auto_resolve_parameters",
    "register_skill",
]
