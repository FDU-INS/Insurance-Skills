"""NCPDP SCRIPT Standard generator for e-prescribing."""
import uuid
import xml.etree.ElementTree as ET
from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field


class SCRIPTMessageType(str, Enum):
    """NCPDP SCRIPT message types."""

    NEW_RX = "NewRx"
    RX_CHANGE = "RxChange"
    RX_RENEWAL = "RxRenewal"
    CANCEL_RX = "CancelRx"
    RX_FILL = "RxFill"
    RX_FILL_STATUS = "RxFillStatus"
    CENSUS = "Census"
    RESUPPLY = "Resupply"


class RxChangeType(str, Enum):
    """RxChange request types."""

    GENERIC_SUBSTITUTION = "G"
    THERAPEUTIC_SUBSTITUTION = "T"
    DRUG_USE_EVALUATION = "U"
    FORMULARY = "F"
    SCRIPT_CLARIFICATION = "S"
    PRIOR_AUTHORIZATION = "P"
    OUT_OF_STOCK = "OS"


class NewRxMessage(BaseModel):
    """NewRx message content."""

    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sent_time: datetime = Field(default_factory=datetime.now)

    # Prescriber
    prescriber_npi: str
    prescriber_first_name: str
    prescriber_last_name: str
    prescriber_address: str | None = None
    prescriber_city: str | None = None
    prescriber_state: str | None = None
    prescriber_zip: str | None = None
    prescriber_phone: str | None = None
    prescriber_dea: str | None = None

    # Patient
    patient_first_name: str
    patient_last_name: str
    patient_dob: date
    patient_gender: str
    patient_address: str | None = None
    patient_city: str | None = None
    patient_state: str | None = None
    patient_zip: str | None = None

    # Medication
    drug_description: str
    ndc: str | None = None
    quantity: str
    quantity_unit: str = "C48542"  # Tablet
    days_supply: int
    directions: str
    refills: int = 0
    substitutions_allowed: bool = True
    note: str | None = None

    # Pharmacy (optional - for directed prescriptions)
    pharmacy_ncpdp: str | None = None
    pharmacy_npi: str | None = None
    pharmacy_name: str | None = None


class RxChangeMessage(BaseModel):
    """RxChange message content."""

    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sent_time: datetime = Field(default_factory=datetime.now)
    relates_to_message_id: str

    change_type: RxChangeType
    change_reason: str | None = None

    # Original prescription info
    original_drug_description: str
    original_ndc: str | None = None

    # Proposed change
    proposed_drug_description: str
    proposed_ndc: str | None = None
    proposed_quantity: str | None = None
    proposed_days_supply: int | None = None

    # Pharmacy
    pharmacy_ncpdp: str
    pharmacy_npi: str


class RxRenewalMessage(BaseModel):
    """RxRenewal request message content."""

    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sent_time: datetime = Field(default_factory=datetime.now)

    # Patient
    patient_first_name: str
    patient_last_name: str
    patient_dob: date

    # Original prescription
    prescription_number: str
    drug_description: str
    ndc: str | None = None
    quantity: str
    days_supply: int
    last_fill_date: date

    # Pharmacy
    pharmacy_ncpdp: str
    pharmacy_npi: str
    pharmacy_name: str

    # Prescriber
    prescriber_npi: str


class NCPDPScriptGenerator:
    """Generate NCPDP SCRIPT messages."""

    SCRIPT_VERSION = "2017071"
    NAMESPACE = "http://www.ncpdp.org/schema/SCRIPT"

    def generate_new_rx(self, message: NewRxMessage) -> str:
        """Generate NewRx XML message."""
        root = ET.Element("Message")
        root.set("version", self.SCRIPT_VERSION)
        root.set("xmlns", self.NAMESPACE)

        # Header
        header = ET.SubElement(root, "Header")
        ET.SubElement(header, "MessageID").text = message.message_id
        ET.SubElement(header, "SentTime").text = message.sent_time.isoformat()
        ET.SubElement(header, "RelatesToMessageID")

        # Body
        body = ET.SubElement(root, "Body")
        newrx = ET.SubElement(body, "NewRx")

        # Prescriber
        self._add_prescriber(newrx, message)

        # Patient
        self._add_patient(newrx, message)

        # Pharmacy (if directed)
        if message.pharmacy_ncpdp or message.pharmacy_npi:
            self._add_pharmacy(newrx, message)

        # Medication
        self._add_medication_prescribed(newrx, message)

        return self._to_xml_string(root)

    def generate_rx_change(self, message: RxChangeMessage) -> str:
        """Generate RxChange message."""
        root = ET.Element("Message")
        root.set("version", self.SCRIPT_VERSION)
        root.set("xmlns", self.NAMESPACE)

        # Header
        header = ET.SubElement(root, "Header")
        ET.SubElement(header, "MessageID").text = message.message_id
        ET.SubElement(header, "SentTime").text = message.sent_time.isoformat()
        ET.SubElement(header, "RelatesToMessageID").text = message.relates_to_message_id

        # Body
        body = ET.SubElement(root, "Body")
        rxchange = ET.SubElement(body, "RxChangeRequest")

        # Change request
        change_req = ET.SubElement(rxchange, "ChangeRequestType")
        ET.SubElement(change_req, "Code").text = message.change_type.value
        if message.change_reason:
            ET.SubElement(change_req, "Reason").text = message.change_reason

        # Original medication
        original_med = ET.SubElement(rxchange, "MedicationPrescribed")
        ET.SubElement(original_med, "DrugDescription").text = message.original_drug_description
        if message.original_ndc:
            drug_coded = ET.SubElement(original_med, "DrugCoded")
            ET.SubElement(drug_coded, "NDC").text = message.original_ndc

        # Proposed medication
        proposed_med = ET.SubElement(rxchange, "MedicationRequested")
        ET.SubElement(proposed_med, "DrugDescription").text = message.proposed_drug_description
        if message.proposed_ndc:
            drug_coded = ET.SubElement(proposed_med, "DrugCoded")
            ET.SubElement(drug_coded, "NDC").text = message.proposed_ndc
        if message.proposed_quantity:
            qty = ET.SubElement(proposed_med, "Quantity")
            ET.SubElement(qty, "Value").text = message.proposed_quantity
        if message.proposed_days_supply:
            ET.SubElement(proposed_med, "DaysSupply").text = str(message.proposed_days_supply)

        # Pharmacy
        pharmacy = ET.SubElement(rxchange, "Pharmacy")
        ident = ET.SubElement(pharmacy, "Identification")
        ET.SubElement(ident, "NCPDPID").text = message.pharmacy_ncpdp
        ET.SubElement(ident, "NPI").text = message.pharmacy_npi

        return self._to_xml_string(root)

    def generate_rx_renewal(self, message: RxRenewalMessage) -> str:
        """Generate RxRenewal request message."""
        root = ET.Element("Message")
        root.set("version", self.SCRIPT_VERSION)
        root.set("xmlns", self.NAMESPACE)

        # Header
        header = ET.SubElement(root, "Header")
        ET.SubElement(header, "MessageID").text = message.message_id
        ET.SubElement(header, "SentTime").text = message.sent_time.isoformat()
        ET.SubElement(header, "RelatesToMessageID")

        # Body
        body = ET.SubElement(root, "Body")
        renewal = ET.SubElement(body, "RxRenewalRequest")

        # Pharmacy
        pharmacy = ET.SubElement(renewal, "Pharmacy")
        ident = ET.SubElement(pharmacy, "Identification")
        ET.SubElement(ident, "NCPDPID").text = message.pharmacy_ncpdp
        ET.SubElement(ident, "NPI").text = message.pharmacy_npi
        ET.SubElement(pharmacy, "StoreName").text = message.pharmacy_name

        # Prescriber
        prescriber = ET.SubElement(renewal, "Prescriber")
        presc_ident = ET.SubElement(prescriber, "Identification")
        ET.SubElement(presc_ident, "NPI").text = message.prescriber_npi

        # Patient
        patient = ET.SubElement(renewal, "Patient")
        name = ET.SubElement(patient, "Name")
        ET.SubElement(name, "FirstName").text = message.patient_first_name
        ET.SubElement(name, "LastName").text = message.patient_last_name
        ET.SubElement(patient, "DateOfBirth").text = message.patient_dob.isoformat()

        # Medication
        med = ET.SubElement(renewal, "MedicationDispensed")
        ET.SubElement(med, "DrugDescription").text = message.drug_description
        if message.ndc:
            drug_coded = ET.SubElement(med, "DrugCoded")
            ET.SubElement(drug_coded, "NDC").text = message.ndc
        qty = ET.SubElement(med, "Quantity")
        ET.SubElement(qty, "Value").text = message.quantity
        ET.SubElement(med, "DaysSupply").text = str(message.days_supply)
        ET.SubElement(med, "LastFillDate").text = message.last_fill_date.isoformat()
        ET.SubElement(med, "PharmacyRxNumber").text = message.prescription_number

        return self._to_xml_string(root)

    def generate_cancel_rx(
        self,
        message_id: str,
        relates_to: str,
        prescriber_npi: str,
        patient_first: str,
        patient_last: str,
        patient_dob: date,
        drug_description: str,
        cancel_reason: str = "Patient request",
    ) -> str:
        """Generate CancelRx message."""
        root = ET.Element("Message")
        root.set("version", self.SCRIPT_VERSION)
        root.set("xmlns", self.NAMESPACE)

        # Header
        header = ET.SubElement(root, "Header")
        ET.SubElement(header, "MessageID").text = message_id
        ET.SubElement(header, "SentTime").text = datetime.now().isoformat()
        ET.SubElement(header, "RelatesToMessageID").text = relates_to

        # Body
        body = ET.SubElement(root, "Body")
        cancel = ET.SubElement(body, "CancelRx")

        # Prescriber
        prescriber = ET.SubElement(cancel, "Prescriber")
        ident = ET.SubElement(prescriber, "Identification")
        ET.SubElement(ident, "NPI").text = prescriber_npi

        # Patient
        patient = ET.SubElement(cancel, "Patient")
        name = ET.SubElement(patient, "Name")
        ET.SubElement(name, "FirstName").text = patient_first
        ET.SubElement(name, "LastName").text = patient_last
        ET.SubElement(patient, "DateOfBirth").text = patient_dob.isoformat()

        # Medication
        med = ET.SubElement(cancel, "MedicationPrescribed")
        ET.SubElement(med, "DrugDescription").text = drug_description

        # Cancel reason
        ET.SubElement(cancel, "CancelReason").text = cancel_reason

        return self._to_xml_string(root)

    def _add_prescriber(self, parent: ET.Element, message: NewRxMessage) -> None:
        """Add prescriber element."""
        prescriber = ET.SubElement(parent, "Prescriber")

        # Identification
        ident = ET.SubElement(prescriber, "Identification")
        ET.SubElement(ident, "NPI").text = message.prescriber_npi
        if message.prescriber_dea:
            ET.SubElement(ident, "DEANumber").text = message.prescriber_dea

        # Name
        name = ET.SubElement(prescriber, "Name")
        ET.SubElement(name, "FirstName").text = message.prescriber_first_name
        ET.SubElement(name, "LastName").text = message.prescriber_last_name

        # Address
        if message.prescriber_address:
            addr = ET.SubElement(prescriber, "Address")
            ET.SubElement(addr, "AddressLine1").text = message.prescriber_address
            if message.prescriber_city:
                ET.SubElement(addr, "City").text = message.prescriber_city
            if message.prescriber_state:
                ET.SubElement(addr, "State").text = message.prescriber_state
            if message.prescriber_zip:
                ET.SubElement(addr, "ZipCode").text = message.prescriber_zip

        # Phone
        if message.prescriber_phone:
            comm = ET.SubElement(prescriber, "CommunicationNumbers")
            phone = ET.SubElement(comm, "Phone")
            ET.SubElement(phone, "Number").text = message.prescriber_phone

    def _add_patient(self, parent: ET.Element, message: NewRxMessage) -> None:
        """Add patient element."""
        patient = ET.SubElement(parent, "Patient")

        # Name
        name = ET.SubElement(patient, "Name")
        ET.SubElement(name, "FirstName").text = message.patient_first_name
        ET.SubElement(name, "LastName").text = message.patient_last_name

        # Demographics
        ET.SubElement(patient, "DateOfBirth").text = message.patient_dob.isoformat()
        gender = ET.SubElement(patient, "Gender")
        ET.SubElement(gender, "Code").text = message.patient_gender

        # Address
        if message.patient_address:
            addr = ET.SubElement(patient, "Address")
            ET.SubElement(addr, "AddressLine1").text = message.patient_address
            if message.patient_city:
                ET.SubElement(addr, "City").text = message.patient_city
            if message.patient_state:
                ET.SubElement(addr, "State").text = message.patient_state
            if message.patient_zip:
                ET.SubElement(addr, "ZipCode").text = message.patient_zip

    def _add_pharmacy(self, parent: ET.Element, message: NewRxMessage) -> None:
        """Add pharmacy element."""
        pharmacy = ET.SubElement(parent, "Pharmacy")

        ident = ET.SubElement(pharmacy, "Identification")
        if message.pharmacy_ncpdp:
            ET.SubElement(ident, "NCPDPID").text = message.pharmacy_ncpdp
        if message.pharmacy_npi:
            ET.SubElement(ident, "NPI").text = message.pharmacy_npi

        if message.pharmacy_name:
            ET.SubElement(pharmacy, "StoreName").text = message.pharmacy_name

    def _add_medication_prescribed(
        self, parent: ET.Element, message: NewRxMessage
    ) -> None:
        """Add medication prescribed element."""
        med = ET.SubElement(parent, "MedicationPrescribed")

        # Drug description
        ET.SubElement(med, "DrugDescription").text = message.drug_description

        # Drug coded (NDC)
        if message.ndc:
            drug_coded = ET.SubElement(med, "DrugCoded")
            ET.SubElement(drug_coded, "ProductCode").text = message.ndc
            ET.SubElement(drug_coded, "ProductCodeQualifier").text = "ND"

        # Quantity
        quantity = ET.SubElement(med, "Quantity")
        ET.SubElement(quantity, "Value").text = message.quantity
        ET.SubElement(quantity, "CodeListQualifier").text = "38"
        ET.SubElement(quantity, "QuantityUnitOfMeasure").text = message.quantity_unit

        # Days supply
        ET.SubElement(med, "DaysSupply").text = str(message.days_supply)

        # Directions
        sig = ET.SubElement(med, "Sig")
        ET.SubElement(sig, "SigText").text = message.directions

        # Refills
        ET.SubElement(med, "Refills").text = str(message.refills)

        # Substitutions
        sub = ET.SubElement(med, "Substitutions")
        ET.SubElement(sub, "Code").text = "0" if message.substitutions_allowed else "1"

        # Note
        if message.note:
            ET.SubElement(med, "Note").text = message.note

    def _to_xml_string(self, root: ET.Element) -> str:
        """Convert element tree to XML string with declaration."""
        return '<?xml version="1.0" encoding="UTF-8"?>' + ET.tostring(
            root, encoding="unicode"
        )

    def parse_message(self, xml_string: str) -> dict:
        """Parse SCRIPT XML message into dictionary."""
        # Remove XML declaration if present
        if xml_string.startswith("<?xml"):
            xml_string = xml_string[xml_string.index("?>") + 2 :]

        root = ET.fromstring(xml_string)
        return self._element_to_dict(root)

    def _element_to_dict(self, element: ET.Element) -> dict:
        """Recursively convert XML element to dictionary."""
        result: dict = {}

        # Add attributes
        if element.attrib:
            result["@attributes"] = element.attrib

        # Add children
        for child in element:
            child_data = self._element_to_dict(child)
            tag = child.tag

            # Remove namespace if present
            if "}" in tag:
                tag = tag.split("}")[1]

            if tag in result:
                # Convert to list if multiple elements with same tag
                if not isinstance(result[tag], list):
                    result[tag] = [result[tag]]
                result[tag].append(child_data)
            else:
                result[tag] = child_data

        # Add text content
        if element.text and element.text.strip():
            if result:
                result["#text"] = element.text.strip()
            else:
                return element.text.strip()  # type: ignore[return-value]

        return result
