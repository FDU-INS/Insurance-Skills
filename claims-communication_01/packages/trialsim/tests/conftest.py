"""Pytest configuration and fixtures for TrialSim tests."""

import pytest

from trialsim.core import (
    AdverseEventGenerator,
    ExposureGenerator,
    TrialSubjectGenerator,
    VisitGenerator,
)


@pytest.fixture
def subject_generator():
    """Create a subject generator with fixed seed."""
    return TrialSubjectGenerator(seed=42)


@pytest.fixture
def visit_generator():
    """Create a visit generator with fixed seed."""
    return VisitGenerator(seed=42)


@pytest.fixture
def ae_generator():
    """Create an adverse event generator with fixed seed."""
    return AdverseEventGenerator(seed=42)


@pytest.fixture
def exposure_generator():
    """Create an exposure generator with fixed seed."""
    return ExposureGenerator(seed=42)


@pytest.fixture
def sample_subject(subject_generator):
    """Create a sample subject for testing."""
    return subject_generator.generate(
        protocol_id="TEST-PROTO-001",
        site_id="TEST-SITE-001",
    )
