"""C-CDA format transformer module.

This module provides C-CDA (Consolidated Clinical Document Architecture)
document generation from PatientSim model objects.

Example:
    >>> from patientsim.formats.ccda import CCDATransformer, CCDAConfig, DocumentType
    >>> config = CCDAConfig(
    ...     document_type=DocumentType.CCD,
    ...     organization_name="Example Hospital",
    ...     organization_oid="2.16.840.1.113883.3.1234",
    ... )
    >>> transformer = CCDATransformer(config)
    >>> xml = transformer.transform(patient, encounters, diagnoses)

    # Or use SectionBuilder for individual sections:
    >>> from patientsim.formats.ccda import SectionBuilder
    >>> builder = SectionBuilder()
    >>> problems_xml = builder.build_problems(diagnoses)
    >>> allergies_xml = builder.build_allergies(allergies)

    # Use NarrativeBuilder for HTML narratives:
    >>> from patientsim.formats.ccda import NarrativeBuilder
    >>> narrator = NarrativeBuilder()
    >>> problems_html = narrator.build_problems_narrative(diagnoses)

    # Use CodeSystemRegistry for vocabulary lookups:
    >>> from patientsim.formats.ccda import CodeSystemRegistry, CodedValue
    >>> registry = CodeSystemRegistry()
    >>> coded = registry.get_snomed_for_icd10("E11.9")
"""

from patientsim.formats.ccda.header import HeaderBuilder
from patientsim.formats.ccda.narratives import NarrativeBuilder
from patientsim.formats.ccda.sections import SectionBuilder
from patientsim.formats.ccda.transformer import CCDAConfig, CCDATransformer, DocumentType
from patientsim.formats.ccda.validators import CCDAValidator, ValidationResult
from patientsim.formats.ccda.vocabulary import (
    CODE_SYSTEMS,
    CodedValue,
    CodeSystemRegistry,
    get_code_system,
)

__all__ = [
    # Core transformer
    "CCDAConfig",
    "CCDATransformer",
    "DocumentType",
    # Builders
    "HeaderBuilder",
    "NarrativeBuilder",
    "SectionBuilder",
    # Validators
    "CCDAValidator",
    "ValidationResult",
    # Vocabulary
    "CODE_SYSTEMS",
    "CodedValue",
    "CodeSystemRegistry",
    "get_code_system",
]
