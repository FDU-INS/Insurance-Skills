"""MIMIC-III format export functionality.

This module provides transformers to convert PatientSim Patient objects
into MIMIC-III compatible database tables.

MIMIC-III is a widely-used critical care database. This module generates
data that conforms to the MIMIC-III schema structure.
"""

from patientsim.formats.mimic.transformer import MIMICTransformer

__all__ = ["MIMICTransformer"]
