"""Pharmacy member data generator.

This module provides the RxMemberGenerator class for creating synthetic
pharmacy benefit member data with consistent coverage and benefit structures.
Extends healthsim-core's BaseGenerator for reproducibility support.
"""

from datetime import date, timedelta
from decimal import Decimal

from healthsim.generation import BaseGenerator

from rxmembersim.core.drug import DEASchedule, DrugReference
from rxmembersim.core.member import BenefitAccumulators, MemberDemographics, RxMember
from rxmembersim.core.prescription import DAWCode, Prescription


class RxMemberGenerator(BaseGenerator):
    """Generator for pharmacy benefit member data.

    Extends healthsim-core's BaseGenerator to provide reproducible
    generation of pharmacy member data including coverage, formulary,
    and accumulator information.

    Example:
        >>> gen = RxMemberGenerator(seed=42)
        >>> member = gen.generate_member()
        >>> print(f"{member.demographics.first_name} {member.demographics.last_name}")
        John Smith
    """

    # Default pharmacy benefit identifiers
    DEFAULT_BIN = "610014"
    DEFAULT_PCN = "RXTEST"
    DEFAULT_GROUP = "GRP001"

    def __init__(self, seed: int | None = None, locale: str = "en_US") -> None:
        """Initialize the pharmacy member generator.

        Args:
            seed: Random seed for reproducibility
            locale: Locale for Faker (default: en_US)
        """
        super().__init__(seed=seed, locale=locale)
        self._member_counter = 0
        self._rx_counter = 0
        self._claim_counter = 0

    def generate_member(
        self,
        age_range: tuple[int, int] | None = None,
        bin: str | None = None,
        pcn: str | None = None,
        group_number: str | None = None,
        plan_code: str | None = None,
        formulary_id: str | None = None,
    ) -> RxMember:
        """Generate a random pharmacy benefit member.

        Args:
            age_range: (min_age, max_age) or None for default (18, 85)
            bin: Bank Identification Number (default: 610014)
            pcn: Processor Control Number (default: RXTEST)
            group_number: Group number (default: GRP001)
            plan_code: Plan code identifier
            formulary_id: Formulary identifier

        Returns:
            Generated RxMember instance
        """
        if age_range is None:
            age_range = (18, 85)

        self._member_counter += 1

        # Generate birth date based on age
        min_age, max_age = age_range
        today = date.today()
        max_birth = today - timedelta(days=min_age * 365)
        min_birth = today - timedelta(days=max_age * 365)
        birth_date = self.random_date_between(min_birth, max_birth)

        # Generate name based on random gender
        gender = self.random_choice(["M", "F"])
        if gender == "M":
            first_name = self.faker.first_name_male()
        else:
            first_name = self.faker.first_name_female()

        member_id = f"RXM{self.random_int(10000000, 99999999)}"
        cardholder_id = f"{self.random_int(100000000, 999999999)}"

        # Generate coverage dates (within last 3 years)
        days_ago = self.random_int(0, 1095)
        effective_date = today - timedelta(days=days_ago)

        # Generate accumulators based on time into benefit year
        # Assume Jan 1 starts the benefit year
        benefit_year_start = date(today.year, 1, 1)
        if effective_date > benefit_year_start:
            benefit_year_start = effective_date

        # Standard commercial plan amounts
        annual_deductible = Decimal("250")
        annual_oop_max = Decimal("3000")

        # Random accumulator progress based on month
        month_factor = (today - benefit_year_start).days / 365.0
        deductible_met = min(annual_deductible, Decimal(str(round(float(annual_deductible) * month_factor * self.random_float(0.5, 1.5), 2))))
        oop_met = min(annual_oop_max, Decimal(str(round(float(annual_oop_max) * month_factor * self.random_float(0.3, 1.0), 2))))

        return RxMember(
            member_id=member_id,
            cardholder_id=cardholder_id,
            person_code="01",  # Primary cardholder
            bin=bin or self.DEFAULT_BIN,
            pcn=pcn or self.DEFAULT_PCN,
            group_number=group_number or self.DEFAULT_GROUP,
            demographics=MemberDemographics(
                first_name=first_name,
                last_name=self.faker.last_name(),
                date_of_birth=birth_date,
                gender=gender,
                address_line1=self.faker.street_address(),
                city=self.faker.city(),
                state=self.faker.state_abbr(),
                zip_code=self.faker.postcode(),
                phone=self.faker.phone_number(),
            ),
            effective_date=effective_date,
            accumulators=BenefitAccumulators(
                deductible_met=deductible_met,
                deductible_remaining=annual_deductible - deductible_met,
                oop_met=oop_met,
                oop_remaining=annual_oop_max - oop_met,
            ),
            plan_code=plan_code,
            formulary_id=formulary_id,
        )

    def generate_prescription(
        self,
        prescriber_npi: str | None = None,
        ndc: str | None = None,
        drug_name: str | None = None,
        quantity: Decimal | None = None,
        days_supply: int | None = None,
        refills: int | None = None,
    ) -> Prescription:
        """Generate a random prescription.

        Args:
            prescriber_npi: Prescriber NPI (generated if not provided)
            ndc: NDC code (generated if not provided)
            drug_name: Drug name (generated if not provided)
            quantity: Quantity prescribed
            days_supply: Days supply
            refills: Number of refills authorized

        Returns:
            Generated Prescription instance
        """
        self._rx_counter += 1

        today = date.today()
        written_date = today - timedelta(days=self.random_int(0, 30))
        expiration_date = written_date + timedelta(days=365)

        # Common retail quantities
        if days_supply is None:
            days_supply = self.random_choice([30, 90])

        if quantity is None:
            quantity = Decimal(str(days_supply))  # Default to 1 unit per day

        if refills is None:
            refills = self.random_choice([0, 1, 2, 3, 5, 11])

        # Generate prescription number
        rx_number = f"RX{self.random_int(10000000, 99999999)}"

        # Generate or use provided NDC (11-digit format)
        if ndc is None:
            ndc = f"{self.random_int(10000, 99999):05d}{self.random_int(1000, 9999):04d}{self.random_int(10, 99):02d}"

        if drug_name is None:
            drug_name = self.random_choice([
                "Metformin 500mg Tablet",
                "Lisinopril 10mg Tablet",
                "Atorvastatin 20mg Tablet",
                "Omeprazole 20mg Capsule",
                "Amlodipine 5mg Tablet",
                "Metoprolol 25mg Tablet",
                "Losartan 50mg Tablet",
                "Gabapentin 300mg Capsule",
                "Levothyroxine 50mcg Tablet",
                "Sertraline 50mg Tablet",
            ])

        if prescriber_npi is None:
            prescriber_npi = f"{self.random_int(1000000000, 1999999999)}"

        return Prescription(
            prescription_number=rx_number,
            ndc=ndc,
            drug_name=drug_name,
            quantity_prescribed=quantity,
            days_supply=days_supply,
            refills_authorized=refills,
            refills_remaining=refills,
            prescriber_npi=prescriber_npi,
            prescriber_name=f"Dr. {self.faker.last_name()}",
            written_date=written_date,
            expiration_date=expiration_date,
            daw_code=DAWCode.NO_SELECTION,
            diagnosis_codes=[],
        )

    def generate_drug(
        self,
        ndc: str | None = None,
        drug_name: str | None = None,
        is_brand: bool | None = None,
        is_controlled: bool = False,
    ) -> DrugReference:
        """Generate a drug reference entry.

        Args:
            ndc: NDC code (generated if not provided)
            drug_name: Drug name (generated if not provided)
            is_brand: Whether this is a brand drug
            is_controlled: Whether this is a controlled substance

        Returns:
            Generated DrugReference instance
        """
        # Generate NDC if not provided
        if ndc is None:
            ndc = f"{self.random_int(10000, 99999):05d}{self.random_int(1000, 9999):04d}{self.random_int(10, 99):02d}"

        if is_brand is None:
            is_brand = self.random_choice([True, False, False, False])  # 25% brand

        # Sample drug names
        if drug_name is None:
            if is_brand:
                drug_name = self.random_choice([
                    "Lipitor", "Crestor", "Eliquis", "Jardiance", "Ozempic",
                    "Humira", "Keytruda", "Entresto", "Xarelto", "Trulicity"
                ])
            else:
                drug_name = self.random_choice([
                    "Metformin", "Lisinopril", "Atorvastatin", "Omeprazole",
                    "Amlodipine", "Metoprolol", "Losartan", "Gabapentin",
                    "Levothyroxine", "Sertraline"
                ])

        # Generate GPI (14-character Generic Product Identifier)
        gpi = f"{self.random_int(10, 99)}{self.random_int(1000, 9999)}{self.random_int(10, 99)}{self.random_int(1000, 9999)}{self.random_int(10, 99)}"

        dea_schedule = DEASchedule.NON_CONTROLLED
        if is_controlled:
            dea_schedule = self.random_choice([
                DEASchedule.SCHEDULE_II,
                DEASchedule.SCHEDULE_III,
                DEASchedule.SCHEDULE_IV,
                DEASchedule.SCHEDULE_V,
            ])

        return DrugReference(
            ndc=ndc,
            drug_name=drug_name,
            generic_name=drug_name.split()[0] if not is_brand else f"Generic {drug_name}",
            gpi=gpi,
            therapeutic_class=self.random_choice([
                "Antidiabetics", "Antihypertensives", "Statins",
                "Proton Pump Inhibitors", "Beta Blockers", "ACE Inhibitors",
                "Anticonvulsants", "SSRIs", "Thyroid Hormones"
            ]),
            strength=self.random_choice(["5mg", "10mg", "20mg", "25mg", "50mg", "100mg", "500mg"]),
            dosage_form=self.random_choice(["Tablet", "Capsule", "Solution", "Injection"]),
            route_of_admin=self.random_choice(["Oral", "Subcutaneous", "Intravenous"]),
            dea_schedule=dea_schedule,
            is_brand=is_brand,
            multi_source_code="N" if is_brand else "Y",
            awp=round(self.random_float(5.0, 500.0), 2) if is_brand else round(self.random_float(2.0, 50.0), 2),
        )
