"""Prescriber model."""
from enum import Enum

from faker import Faker
from pydantic import BaseModel


class PrescriberType(str, Enum):
    """Prescriber types/credentials."""

    MD = "MD"  # Medical Doctor
    DO = "DO"  # Doctor of Osteopathy
    NP = "NP"  # Nurse Practitioner
    PA = "PA"  # Physician Assistant
    DDS = "DDS"  # Doctor of Dental Surgery
    DMD = "DMD"  # Doctor of Medicine in Dentistry
    DPM = "DPM"  # Doctor of Podiatric Medicine
    OD = "OD"  # Doctor of Optometry
    PHARMD = "PharmD"  # Doctor of Pharmacy (limited prescribing)
    CNM = "CNM"  # Certified Nurse Midwife
    CRNA = "CRNA"  # Certified Registered Nurse Anesthetist


class PrescriberSpecialty(str, Enum):
    """Common prescriber specialties."""

    FAMILY_MEDICINE = "Family Medicine"
    INTERNAL_MEDICINE = "Internal Medicine"
    PEDIATRICS = "Pediatrics"
    CARDIOLOGY = "Cardiology"
    DERMATOLOGY = "Dermatology"
    ENDOCRINOLOGY = "Endocrinology"
    GASTROENTEROLOGY = "Gastroenterology"
    HEMATOLOGY = "Hematology"
    INFECTIOUS_DISEASE = "Infectious Disease"
    NEPHROLOGY = "Nephrology"
    NEUROLOGY = "Neurology"
    ONCOLOGY = "Oncology"
    OPHTHALMOLOGY = "Ophthalmology"
    ORTHOPEDICS = "Orthopedics"
    PSYCHIATRY = "Psychiatry"
    PULMONOLOGY = "Pulmonology"
    RHEUMATOLOGY = "Rheumatology"
    SURGERY = "Surgery"
    UROLOGY = "Urology"
    EMERGENCY_MEDICINE = "Emergency Medicine"
    ANESTHESIOLOGY = "Anesthesiology"
    PAIN_MANAGEMENT = "Pain Management"
    OBSTETRICS_GYNECOLOGY = "Obstetrics/Gynecology"
    GERIATRICS = "Geriatrics"


class Prescriber(BaseModel):
    """Prescriber information."""

    npi: str  # 10-digit NPI
    dea: str | None = None  # DEA number for controlled substances

    first_name: str
    last_name: str
    middle_name: str | None = None
    suffix: str | None = None  # Jr., Sr., III, etc.
    credential: PrescriberType = PrescriberType.MD

    specialty: PrescriberSpecialty | None = None
    taxonomy_code: str | None = None  # Provider taxonomy code

    # Practice information
    practice_name: str | None = None
    address_line1: str | None = None
    address_line2: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    phone: str | None = None
    fax: str | None = None
    email: str | None = None

    # State license
    state_license: str | None = None
    license_state: str | None = None

    # Status
    active: bool = True
    can_prescribe_controlled: bool = True

    @property
    def full_name(self) -> str:
        """Get full name with credential."""
        parts = [self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.last_name)
        if self.suffix:
            parts.append(self.suffix)
        return " ".join(parts)

    @property
    def display_name(self) -> str:
        """Get display name with credential."""
        return f"{self.full_name}, {self.credential.value}"


class PrescriberGenerator:
    """Generate synthetic prescriber data."""

    SPECIALTY_DEA_SUFFIX = {
        PrescriberSpecialty.PAIN_MANAGEMENT: "X",  # Buprenorphine waiver
        PrescriberSpecialty.PSYCHIATRY: "X",
        PrescriberSpecialty.ANESTHESIOLOGY: "X",
    }

    def __init__(self) -> None:
        self.fake = Faker()

    def generate(
        self,
        credential: PrescriberType = PrescriberType.MD,
        specialty: PrescriberSpecialty | None = None,
        can_prescribe_controlled: bool = True,
    ) -> Prescriber:
        """Generate a random prescriber."""
        npi = self._generate_npi()

        # Generate DEA if can prescribe controlled
        dea = self._generate_dea() if can_prescribe_controlled else None

        # Pick specialty if not provided
        if specialty is None:
            specialty = self.fake.random_element(list(PrescriberSpecialty))

        # Generate state for license
        state = self.fake.state_abbr()

        return Prescriber(
            npi=npi,
            dea=dea,
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            middle_name=self.fake.first_name() if self.fake.boolean(30) else None,
            suffix=self.fake.suffix() if self.fake.boolean(10) else None,
            credential=credential,
            specialty=specialty,
            taxonomy_code=self._get_taxonomy_code(specialty),
            practice_name=f"{self.fake.last_name()} {specialty.value} Associates"
            if self.fake.boolean(70)
            else None,
            address_line1=self.fake.street_address(),
            city=self.fake.city(),
            state=state,
            zip_code=self.fake.zipcode(),
            phone=self.fake.phone_number(),
            fax=self.fake.phone_number() if self.fake.boolean(60) else None,
            state_license=f"{state}{self.fake.random_number(digits=6, fix_len=True)}",
            license_state=state,
            active=True,
            can_prescribe_controlled=can_prescribe_controlled,
        )

    def generate_specialist(
        self, specialty: PrescriberSpecialty
    ) -> Prescriber:
        """Generate a prescriber with specific specialty."""
        return self.generate(specialty=specialty)

    def generate_mid_level(self) -> Prescriber:
        """Generate a mid-level prescriber (NP or PA)."""
        credential = self.fake.random_element([PrescriberType.NP, PrescriberType.PA])
        return self.generate(credential=credential)

    def _generate_npi(self) -> str:
        """Generate a valid NPI (10 digits starting with 1)."""
        return "1" + str(self.fake.random_number(digits=9, fix_len=True))

    def _generate_dea(self) -> str:
        """Generate a DEA number format."""
        # DEA format: 2 letters + 7 digits
        # First letter: registrant type
        # Second letter: first letter of registrant's last name
        first_letter = self.fake.random_element(["A", "B", "F", "M"])
        second_letter = self.fake.random_uppercase_letter()
        digits = str(self.fake.random_number(digits=7, fix_len=True))
        return f"{first_letter}{second_letter}{digits}"

    def _get_taxonomy_code(self, specialty: PrescriberSpecialty) -> str:
        """Get provider taxonomy code for specialty."""
        # Simplified taxonomy codes
        taxonomy_map = {
            PrescriberSpecialty.FAMILY_MEDICINE: "207Q00000X",
            PrescriberSpecialty.INTERNAL_MEDICINE: "207R00000X",
            PrescriberSpecialty.PEDIATRICS: "208000000X",
            PrescriberSpecialty.CARDIOLOGY: "207RC0000X",
            PrescriberSpecialty.DERMATOLOGY: "207N00000X",
            PrescriberSpecialty.ENDOCRINOLOGY: "207RE0101X",
            PrescriberSpecialty.GASTROENTEROLOGY: "207RG0100X",
            PrescriberSpecialty.NEUROLOGY: "2084N0400X",
            PrescriberSpecialty.ONCOLOGY: "207RX0202X",
            PrescriberSpecialty.PSYCHIATRY: "2084P0800X",
            PrescriberSpecialty.RHEUMATOLOGY: "207RR0500X",
            PrescriberSpecialty.SURGERY: "208600000X",
            PrescriberSpecialty.EMERGENCY_MEDICINE: "207P00000X",
            PrescriberSpecialty.PAIN_MANAGEMENT: "208VP0014X",
            PrescriberSpecialty.OBSTETRICS_GYNECOLOGY: "207V00000X",
        }
        return taxonomy_map.get(specialty, "207Q00000X")
