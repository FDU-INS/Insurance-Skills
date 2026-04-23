"""HL7v2 message generation functionality.

This module provides generators to create HL7v2 messages from PatientSim objects.
Supports ADT message types (A01, A03, A08).
"""

from patientsim.formats.hl7v2.generator import HL7v2Generator

__all__ = ["HL7v2Generator"]
