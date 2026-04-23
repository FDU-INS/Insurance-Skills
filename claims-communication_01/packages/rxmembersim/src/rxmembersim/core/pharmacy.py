"""Pharmacy model."""
from enum import Enum

from faker import Faker
from pydantic import BaseModel


class PharmacyType(str, Enum):
    """Pharmacy types."""

    RETAIL = "retail"
    MAIL_ORDER = "mail"
    SPECIALTY = "specialty"
    LONG_TERM_CARE = "ltc"
    HOSPITAL = "hospital"
    CLINIC = "clinic"
    NUCLEAR = "nuclear"
    MILITARY = "military"
    INDIAN_HEALTH = "ihs"


class Pharmacy(BaseModel):
    """Pharmacy information."""

    ncpdp_id: str  # 7-digit NCPDP ID
    npi: str  # 10-digit NPI

    name: str
    dba_name: str | None = None  # Doing Business As name
    pharmacy_type: PharmacyType = PharmacyType.RETAIL

    # Address
    address_line1: str
    address_line2: str | None = None
    city: str
    state: str
    zip_code: str

    # Contact
    phone: str
    fax: str | None = None
    email: str | None = None

    # Network status
    in_network: bool = True
    preferred: bool = False
    specialty_certified: bool = False

    # Capabilities
    accepts_electronic_prescriptions: bool = True
    has_delivery: bool = False
    has_24_hour: bool = False
    has_drive_thru: bool = False

    # Chain info
    chain_code: str | None = None
    chain_name: str | None = None

    # DEA registration (required for controlled substances)
    dea_number: str | None = None


class PharmacyGenerator:
    """Generate synthetic pharmacy data."""

    CHAIN_PHARMACIES = [
        ("CVS", "CVS Pharmacy"),
        ("WAG", "Walgreens"),
        ("RAD", "Rite Aid"),
        ("WMT", "Walmart Pharmacy"),
        ("TGT", "Target Pharmacy"),
        ("KRG", "Kroger Pharmacy"),
        ("PUB", "Publix Pharmacy"),
        ("SAF", "Safeway Pharmacy"),
        ("ALB", "Albertsons Pharmacy"),
        ("HEB", "H-E-B Pharmacy"),
    ]

    SPECIALTY_PHARMACIES = [
        ("ACA", "Accredo"),
        ("CVS", "CVS Specialty"),
        ("EXP", "Express Scripts Specialty"),
        ("DIP", "Diplomat Pharmacy"),
        ("BIO", "BioScrip"),
        ("ONC", "Onco360"),
        ("AVI", "Avita Pharmacy"),
    ]

    def __init__(self) -> None:
        self.fake = Faker()

    def generate(
        self,
        pharmacy_type: PharmacyType = PharmacyType.RETAIL,
        chain: bool = True,
        in_network: bool = True,
    ) -> Pharmacy:
        """Generate a random pharmacy."""
        ncpdp_id = str(self.fake.random_number(digits=7, fix_len=True))
        npi = self._generate_npi()

        if pharmacy_type == PharmacyType.SPECIALTY:
            chain_code, chain_name = self.fake.random_element(self.SPECIALTY_PHARMACIES)
            name = f"{chain_name} #{self.fake.random_number(digits=4, fix_len=True)}"
        elif chain:
            chain_code, chain_name = self.fake.random_element(self.CHAIN_PHARMACIES)
            name = f"{chain_name} #{self.fake.random_number(digits=4, fix_len=True)}"
        else:
            chain_code = None
            chain_name = None
            name = f"{self.fake.last_name()} Pharmacy"

        return Pharmacy(
            ncpdp_id=ncpdp_id,
            npi=npi,
            name=name,
            pharmacy_type=pharmacy_type,
            address_line1=self.fake.street_address(),
            city=self.fake.city(),
            state=self.fake.state_abbr(),
            zip_code=self.fake.zipcode(),
            phone=self.fake.phone_number(),
            fax=self.fake.phone_number() if self.fake.boolean(70) else None,
            in_network=in_network,
            preferred=self.fake.boolean(20) if in_network else False,
            specialty_certified=pharmacy_type == PharmacyType.SPECIALTY,
            accepts_electronic_prescriptions=True,
            has_delivery=self.fake.boolean(40),
            has_24_hour=self.fake.boolean(15),
            has_drive_thru=self.fake.boolean(50),
            chain_code=chain_code,
            chain_name=chain_name,
            dea_number=self._generate_dea(),
        )

    def generate_mail_order(self, in_network: bool = True) -> Pharmacy:
        """Generate a mail-order pharmacy."""
        return self.generate(
            pharmacy_type=PharmacyType.MAIL_ORDER,
            chain=True,
            in_network=in_network,
        )

    def generate_specialty(self, in_network: bool = True) -> Pharmacy:
        """Generate a specialty pharmacy."""
        return self.generate(
            pharmacy_type=PharmacyType.SPECIALTY,
            chain=True,
            in_network=in_network,
        )

    def _generate_npi(self) -> str:
        """Generate a valid NPI (10 digits starting with 1 or 2)."""
        prefix = self.fake.random_element(["1", "2"])
        return prefix + str(self.fake.random_number(digits=9, fix_len=True))

    def _generate_dea(self) -> str:
        """Generate a DEA number format."""
        # DEA format: 2 letters + 7 digits
        # First letter: registrant type (A,B,C,D,E,F,G,H,J,K,L,M,P,R,S,T,U,X)
        # Second letter: first letter of registrant's last name
        first_letter = self.fake.random_element(
            ["A", "B", "C", "D", "F", "G", "M", "P", "R"]
        )
        second_letter = self.fake.random_uppercase_letter()
        digits = str(self.fake.random_number(digits=7, fix_len=True))
        return f"{first_letter}{second_letter}{digits}"
