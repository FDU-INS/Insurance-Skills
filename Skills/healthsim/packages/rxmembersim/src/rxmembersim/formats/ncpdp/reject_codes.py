"""NCPDP standard reject codes."""
from enum import Enum


class RejectCategory(str, Enum):
    """Reject code categories."""

    ELIGIBILITY = "Eligibility"
    COVERAGE = "Coverage"
    DUR = "DUR"
    QUANTITY = "Quantity"
    PRIOR_AUTHORIZATION = "Prior Authorization"
    SUBMISSION = "Submission"
    SYSTEM = "System"
    OTHER = "Other"


# NCPDP Standard Reject Codes
NCPDP_REJECT_CODES: dict[str, str] = {
    # Submission/Format rejects (01-24)
    "01": "Missing/Invalid BIN Number",
    "02": "Missing/Invalid Version Number",
    "03": "Missing/Invalid Transaction Code",
    "04": "Missing/Invalid Processor Control Number",
    "05": "Missing/Invalid Date of Birth",
    "06": "Missing/Invalid Cardholder ID",
    "07": "Missing/Invalid Group ID",
    "08": "Missing/Invalid Person Code",
    "09": "Missing/Invalid Birth/Sequence Number",
    "10": "Missing/Invalid Patient Name",
    "11": "Missing/Invalid Patient Gender",
    "12": "Missing/Invalid Patient Street Address",
    "13": "Missing/Invalid Patient City",
    "14": "Missing/Invalid Patient State/Province",
    "15": "Missing/Invalid Patient ZIP/Postal Code",
    "16": "Missing/Invalid Cardholder First Name",
    "17": "Missing/Invalid Cardholder Last Name",
    "18": "Missing/Invalid Cardholder Street Address",
    "19": "Missing/Invalid Cardholder City",
    "20": "Missing/Invalid Cardholder State/Province",
    "21": "Missing/Invalid Cardholder ZIP/Postal Code",
    "22": "Missing/Invalid Cardholder ID Qualifier",
    "23": "Missing/Invalid Place of Service",
    "24": "Missing/Invalid Employer ID",
    "25": "Missing/Invalid Prescription/Service Reference Number",
    # Eligibility rejects (65-69)
    "65": "Patient Not Covered",
    "66": "Patient Age Exceeds Maximum Age",
    "67": "Patient Age Precedes Minimum Age",
    "68": "Member ID Not Found",
    "69": "Invalid Date of Birth",
    # Coverage rejects (70-79)
    "70": "Product/Service Not Covered",
    "71": "Prescriber Not Covered",
    "72": "Primary Prescriber Required",
    "73": "Original Prescription Number Submitted",
    "74": "Inappropriate Prescriber ID",
    "75": "Prior Authorization Required",
    "76": "Plan Limitations Exceeded",
    "77": "Discontinued Product/Service ID Number",
    "78": "Cost Exceeds Maximum",
    "79": "Refill Too Soon",
    # DUR rejects (80-88)
    "80": "Drug-Drug Interaction",
    "81": "Duplicate Therapy",
    "82": "Overuse",
    "83": "Drug Conflict with Pregnancy",
    "84": "Drug-Disease Precaution",
    "85": "Drug Conflict with Age",
    "86": "Drug-Gender Precaution",
    "87": "Dosage Exceeds Maximum",
    "88": "DUR Reject Error",
    # Quantity rejects (89-92)
    "89": "Quantity Below Minimum",
    "90": "Quantity Exceeds Maximum",
    "91": "Days Supply Below Minimum",
    "92": "Days Supply Exceeds Maximum",
    # Prior auth rejects (93-95)
    "93": "Prior Authorization Number Submitted",
    "94": "Prior Authorization Expired",
    "95": "Prior Authorization Cancelled",
    # System rejects (96-99)
    "96": "Claim Not Processed",
    "97": "Host Processor Unavailable",
    "98": "Transmission Error",
    "99": "Host Processing Error",
    # Additional common rejects
    "1C": "Missing/Invalid Compound Code",
    "1E": "Missing/Invalid Unit of Measure",
    "1F": "Missing/Invalid Basis of Cost Determination",
    "1G": "Missing/Invalid DAW Code",
    "1H": "Missing/Invalid Prescription Origin Code",
    "1J": "Missing/Invalid Submission Clarification Code",
    "1K": "Missing/Invalid Primary Care Provider ID",
    "2A": "Missing/Invalid NDC/UPC-HRI",
    "2C": "Missing/Invalid Quantity Dispensed",
    "2E": "Missing/Invalid Days Supply",
    "2G": "Missing/Invalid Fill Number",
    "3A": "Missing/Invalid Prescriber ID Qualifier",
    "3E": "Missing/Invalid Prescriber ID",
    "4E": "Missing/Invalid Patient ID Qualifier",
    "5C": "Missing/Invalid Provider ID",
    "5E": "Missing/Invalid Provider ID Qualifier",
    "6C": "Missing/Invalid Date of Service",
    "6E": "Missing/Invalid Date Written",
    "7C": "Missing/Invalid Ingredient Cost Submitted",
    "7E": "Missing/Invalid Dispensing Fee Submitted",
    "8C": "Missing/Invalid Gross Amount Due",
    "8E": "Missing/Invalid Patient Paid Amount Submitted",
    "9E": "Missing/Invalid Pharmacy NPI",
    "MR": "Product Not On Formulary",
    "ER": "Fill Too Early",
    "ET": "Exceeds Duration of Therapy",
    "FD": "Fraud Detection Alert",
    "FM": "Formulary Mismatch",
    "NC": "Non-Covered Product",
    "NF": "Not Found",
    "NP": "Not Primary",
    "PA": "Prior Authorization Required",
    "PD": "Plan Day Limit Exceeded",
    "PM": "Plan Maximum Exceeded",
    "QE": "Quantity Exceeded",
    "QL": "Quantity Limits Exceeded",
    "RE": "Refills Exceeded",
    "RX": "Prescription Expired",
    "SE": "Step Therapy Required",
    "SP": "Specialty Pharmacy Required",
    "TP": "Therapeutic Interchange",
}


def get_reject_description(code: str) -> str:
    """Get description for reject code."""
    return NCPDP_REJECT_CODES.get(code, f"Unknown Reject Code ({code})")


def get_reject_category(code: str) -> RejectCategory:
    """Get category for reject code."""
    # Handle numeric codes
    if code.isdigit():
        code_num = int(code)
        if 1 <= code_num <= 24:
            return RejectCategory.SUBMISSION
        if 65 <= code_num <= 69:
            return RejectCategory.ELIGIBILITY
        if 70 <= code_num <= 79:
            return RejectCategory.COVERAGE
        if 80 <= code_num <= 88:
            return RejectCategory.DUR
        if 89 <= code_num <= 92:
            return RejectCategory.QUANTITY
        if 93 <= code_num <= 95:
            return RejectCategory.PRIOR_AUTHORIZATION
        if 96 <= code_num <= 99:
            return RejectCategory.SYSTEM

    # Handle alpha/alphanumeric codes
    code_upper = code.upper()
    if code_upper in ("PA", "SE", "SP"):
        return RejectCategory.PRIOR_AUTHORIZATION
    if code_upper in ("80", "81", "82", "83", "84", "85", "86", "87", "88"):
        return RejectCategory.DUR
    if code_upper in ("QL", "QE", "PD", "PM"):
        return RejectCategory.QUANTITY
    if code_upper in ("MR", "FM", "NC", "NF", "TP"):
        return RejectCategory.COVERAGE

    return RejectCategory.OTHER


def get_rejects_by_category(category: RejectCategory) -> dict[str, str]:
    """Get all reject codes for a category."""
    return {
        code: desc
        for code, desc in NCPDP_REJECT_CODES.items()
        if get_reject_category(code) == category
    }


def is_hard_reject(code: str) -> bool:
    """
    Determine if reject is a hard reject (cannot be overridden).

    Hard rejects typically include eligibility issues and certain
    coverage restrictions that cannot be bypassed.
    """
    hard_reject_codes = {
        "65",  # Patient Not Covered
        "68",  # Member ID Not Found
        "94",  # Prior Authorization Expired
        "95",  # Prior Authorization Cancelled
        "96",  # Claim Not Processed
        "97",  # Host Processor Unavailable
        "98",  # Transmission Error
        "99",  # Host Processing Error
    }
    return code in hard_reject_codes


def is_dur_reject(code: str) -> bool:
    """Check if code is a DUR-related reject."""
    return get_reject_category(code) == RejectCategory.DUR


def get_dur_codes() -> dict[str, str]:
    """Get all DUR-related reject codes."""
    return get_rejects_by_category(RejectCategory.DUR)
