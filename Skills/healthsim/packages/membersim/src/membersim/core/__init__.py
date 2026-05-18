"""Core MemberSim models."""

from membersim.core.accumulator import Accumulator
from membersim.core.generator import MemberGenerator
from membersim.core.member import Member, MemberFactory
from membersim.core.plan import SAMPLE_PLANS, Plan
from membersim.core.provider import SPECIALTIES, Provider
from membersim.core.subscriber import Subscriber

# Backward compatibility alias - MemberFactory was previously called MemberGenerator
# For new code, prefer MemberGenerator from generator.py (extends BaseGenerator)
# or MemberFactory from member.py (simple factory without BaseGenerator)
_MemberGeneratorLegacy = MemberFactory

__all__ = [
    "Accumulator",
    "Member",
    "MemberFactory",
    "MemberGenerator",
    "Plan",
    "Provider",
    "SAMPLE_PLANS",
    "SPECIALTIES",
    "Subscriber",
]
