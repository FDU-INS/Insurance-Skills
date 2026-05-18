"""SDTM Domain Definitions.

This module defines CDISC SDTM (Study Data Tabulation Model) domain
structures and variable mappings.

SDTM Domains implemented:
- DM: Demographics
- AE: Adverse Events
- EX: Exposure
- SV: Subject Visits
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class SDTMDomain(str, Enum):
    """SDTM domain codes."""
    DM = "DM"  # Demographics
    AE = "AE"  # Adverse Events
    EX = "EX"  # Exposure
    SV = "SV"  # Subject Visits
    DS = "DS"  # Disposition
    MH = "MH"  # Medical History
    CM = "CM"  # Concomitant Medications
    VS = "VS"  # Vital Signs
    LB = "LB"  # Laboratory Test Results


@dataclass
class SDTMVariable:
    """Definition of an SDTM variable."""
    name: str
    label: str
    data_type: str  # "Char", "Num", "Date"
    length: int | None = None
    required: bool = False
    codelist: str | None = None
    origin: str = "Derived"  # CRF, Derived, Assigned, Protocol


# =============================================================================
# DM Domain - Demographics
# =============================================================================

DM_VARIABLES = [
    SDTMVariable("STUDYID", "Study Identifier", "Char", 20, True),
    SDTMVariable("DOMAIN", "Domain Abbreviation", "Char", 2, True),
    SDTMVariable("USUBJID", "Unique Subject Identifier", "Char", 40, True),
    SDTMVariable("SUBJID", "Subject Identifier for the Study", "Char", 20, True),
    SDTMVariable("SITEID", "Study Site Identifier", "Char", 10, True),
    SDTMVariable("RFSTDTC", "Subject Reference Start Date/Time", "Char", 20),
    SDTMVariable("RFENDTC", "Subject Reference End Date/Time", "Char", 20),
    SDTMVariable("RFXSTDTC", "First Exposure Date/Time", "Char", 20),
    SDTMVariable("RFXENDTC", "Last Exposure Date/Time", "Char", 20),
    SDTMVariable("RFICDTC", "Informed Consent Date/Time", "Char", 20),
    SDTMVariable("RFPENDTC", "End of Participation Date/Time", "Char", 20),
    SDTMVariable("DTHDTC", "Date/Time of Death", "Char", 20),
    SDTMVariable("DTHFL", "Subject Death Flag", "Char", 1),
    SDTMVariable("BRTHDTC", "Date/Time of Birth", "Char", 20),
    SDTMVariable("AGE", "Age", "Num", 8),
    SDTMVariable("AGEU", "Age Units", "Char", 6),
    SDTMVariable("SEX", "Sex", "Char", 1, True),
    SDTMVariable("RACE", "Race", "Char", 50),
    SDTMVariable("ETHNIC", "Ethnicity", "Char", 50),
    SDTMVariable("ARMCD", "Planned Arm Code", "Char", 20),
    SDTMVariable("ARM", "Description of Planned Arm", "Char", 200),
    SDTMVariable("ACTARMCD", "Actual Arm Code", "Char", 20),
    SDTMVariable("ACTARM", "Description of Actual Arm", "Char", 200),
    SDTMVariable("COUNTRY", "Country", "Char", 3),
    SDTMVariable("DMDTC", "Date/Time of Collection", "Char", 20),
    SDTMVariable("DMDY", "Study Day of Collection", "Num", 8),
]


# =============================================================================
# AE Domain - Adverse Events
# =============================================================================

AE_VARIABLES = [
    SDTMVariable("STUDYID", "Study Identifier", "Char", 20, True),
    SDTMVariable("DOMAIN", "Domain Abbreviation", "Char", 2, True),
    SDTMVariable("USUBJID", "Unique Subject Identifier", "Char", 40, True),
    SDTMVariable("AESEQ", "Sequence Number", "Num", 8, True),
    SDTMVariable("AESPID", "Sponsor-Defined Identifier", "Char", 40),
    SDTMVariable("AETERM", "Reported Term for the Adverse Event", "Char", 200, True),
    SDTMVariable("AELLT", "Lowest Level Term", "Char", 200),
    SDTMVariable("AELLTCD", "Lowest Level Term Code", "Num", 8),
    SDTMVariable("AEDECOD", "Dictionary-Derived Term", "Char", 200),
    SDTMVariable("AEPTCD", "Preferred Term Code", "Num", 8),
    SDTMVariable("AEHLT", "High Level Term", "Char", 200),
    SDTMVariable("AEHLTCD", "High Level Term Code", "Num", 8),
    SDTMVariable("AEHLGT", "High Level Group Term", "Char", 200),
    SDTMVariable("AEHLGTCD", "High Level Group Term Code", "Num", 8),
    SDTMVariable("AEBODSYS", "Body System or Organ Class", "Char", 200),
    SDTMVariable("AEBDSYCD", "Body System or Organ Class Code", "Num", 8),
    SDTMVariable("AESOC", "Primary System Organ Class", "Char", 200),
    SDTMVariable("AESOCCD", "Primary System Organ Class Code", "Num", 8),
    SDTMVariable("AESEV", "Severity/Intensity", "Char", 10),
    SDTMVariable("AESER", "Serious Event", "Char", 1),
    SDTMVariable("AEACN", "Action Taken with Study Treatment", "Char", 50),
    SDTMVariable("AEREL", "Causality", "Char", 20),
    SDTMVariable("AEOUT", "Outcome of Adverse Event", "Char", 50),
    SDTMVariable("AESCONG", "Congenital Anomaly or Birth Defect", "Char", 1),
    SDTMVariable("AESDISAB", "Persist or Signif Disability/Incapacity", "Char", 1),
    SDTMVariable("AESDTH", "Results in Death", "Char", 1),
    SDTMVariable("AESHOSP", "Requires or Prolongs Hospitalization", "Char", 1),
    SDTMVariable("AESLIFE", "Is Life Threatening", "Char", 1),
    SDTMVariable("AESMIE", "Other Serious (Important Medical Events)", "Char", 1),
    SDTMVariable("AECONTRT", "Concomitant or Additional Trtmnt Given", "Char", 1),
    SDTMVariable("AESTDTC", "Start Date/Time of Adverse Event", "Char", 20),
    SDTMVariable("AEENDTC", "End Date/Time of Adverse Event", "Char", 20),
    SDTMVariable("AESTDY", "Study Day of Start of Adverse Event", "Num", 8),
    SDTMVariable("AEENDY", "Study Day of End of Adverse Event", "Num", 8),
    SDTMVariable("AEDUR", "Duration of Adverse Event", "Char", 20),
    SDTMVariable("AEENRF", "End Relative to Reference Period", "Char", 10),
    SDTMVariable("AEENRTPT", "End Relative to Reference Time Point", "Char", 20),
]


# =============================================================================
# EX Domain - Exposure
# =============================================================================

EX_VARIABLES = [
    SDTMVariable("STUDYID", "Study Identifier", "Char", 20, True),
    SDTMVariable("DOMAIN", "Domain Abbreviation", "Char", 2, True),
    SDTMVariable("USUBJID", "Unique Subject Identifier", "Char", 40, True),
    SDTMVariable("EXSEQ", "Sequence Number", "Num", 8, True),
    SDTMVariable("EXSPID", "Sponsor-Defined Identifier", "Char", 40),
    SDTMVariable("EXTRT", "Name of Actual Treatment", "Char", 200, True),
    SDTMVariable("EXCAT", "Category for Treatment", "Char", 100),
    SDTMVariable("EXSCAT", "Subcategory for Treatment", "Char", 100),
    SDTMVariable("EXDOSE", "Dose per Administration", "Num", 8),
    SDTMVariable("EXDOSTXT", "Dose Description", "Char", 100),
    SDTMVariable("EXDOSU", "Dose Units", "Char", 25),
    SDTMVariable("EXDOSFRM", "Dose Form", "Char", 50),
    SDTMVariable("EXDOSFRQ", "Dosing Frequency per Interval", "Char", 50),
    SDTMVariable("EXROUTE", "Route of Administration", "Char", 50),
    SDTMVariable("EXLOT", "Lot Number", "Char", 40),
    SDTMVariable("EXLOC", "Location of Dose Administration", "Char", 50),
    SDTMVariable("EXLAT", "Laterality", "Char", 50),
    SDTMVariable("EXDIR", "Directionality", "Char", 50),
    SDTMVariable("EXFAST", "Fasting Status", "Char", 1),
    SDTMVariable("EXADJ", "Reason for Dose Adjustment", "Char", 200),
    SDTMVariable("EPOCH", "Epoch", "Char", 50),
    SDTMVariable("EXSTDTC", "Start Date/Time of Treatment", "Char", 20),
    SDTMVariable("EXENDTC", "End Date/Time of Treatment", "Char", 20),
    SDTMVariable("EXSTDY", "Study Day of Start of Treatment", "Num", 8),
    SDTMVariable("EXENDY", "Study Day of End of Treatment", "Num", 8),
    SDTMVariable("EXDUR", "Duration of Treatment", "Char", 20),
]


# =============================================================================
# SV Domain - Subject Visits
# =============================================================================

SV_VARIABLES = [
    SDTMVariable("STUDYID", "Study Identifier", "Char", 20, True),
    SDTMVariable("DOMAIN", "Domain Abbreviation", "Char", 2, True),
    SDTMVariable("USUBJID", "Unique Subject Identifier", "Char", 40, True),
    SDTMVariable("VISITNUM", "Visit Number", "Num", 8, True),
    SDTMVariable("VISIT", "Visit Name", "Char", 200),
    SDTMVariable("VISITDY", "Planned Study Day of Visit", "Num", 8),
    SDTMVariable("TAESSION", "Planned Element within Session", "Char", 20),
    SDTMVariable("EPOCH", "Epoch", "Char", 50),
    SDTMVariable("SVSTDTC", "Start Date/Time of Visit", "Char", 20),
    SDTMVariable("SVENDTC", "End Date/Time of Visit", "Char", 20),
    SDTMVariable("SVSTDY", "Study Day of Start of Visit", "Num", 8),
    SDTMVariable("SVENDY", "Study Day of End of Visit", "Num", 8),
    SDTMVariable("SVUPDES", "Description of Unplanned Visit", "Char", 200),
]


# Domain variable definitions
DOMAIN_VARIABLES = {
    SDTMDomain.DM: DM_VARIABLES,
    SDTMDomain.AE: AE_VARIABLES,
    SDTMDomain.EX: EX_VARIABLES,
    SDTMDomain.SV: SV_VARIABLES,
}


def get_domain_variables(domain: SDTMDomain) -> list[SDTMVariable]:
    """Get variable definitions for a domain.
    
    Args:
        domain: SDTM domain
        
    Returns:
        List of variable definitions
    """
    return DOMAIN_VARIABLES.get(domain, [])


def get_required_variables(domain: SDTMDomain) -> list[str]:
    """Get required variable names for a domain.
    
    Args:
        domain: SDTM domain
        
    Returns:
        List of required variable names
    """
    return [v.name for v in get_domain_variables(domain) if v.required]
