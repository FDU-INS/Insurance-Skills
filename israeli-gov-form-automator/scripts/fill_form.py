#!/usr/bin/env python3
"""
Israeli Government Form Field Helper

Validates and populates common Israeli government form fields:
- Teudat Zehut (ID number) with check digit validation
- Israeli phone numbers (mobile and landline)
- Israeli addresses with mikud (postal code)
- Common form data structures for gov.il, Rashut HaMisim, Bituach Leumi

Usage:
    python fill_form.py --help
    python fill_form.py validate-tz 123456782
    python fill_form.py validate-phone 0521234567
    python fill_form.py validate-address --city "תל אביב" --street "רוטשילד" --number 1 --mikud 6688101
    python fill_form.py form-fields --form tofes-101
"""

import argparse
import json
import re
import sys


def validate_teudat_zehut(id_number: str) -> dict:
    """Validate Israeli Teudat Zehut (ID number) with check digit."""
    id_str = id_number.strip().zfill(9)

    if len(id_str) != 9 or not id_str.isdigit():
        return {"valid": False, "error": "Must be 9 digits", "input": id_number}

    total = 0
    for i, digit in enumerate(id_str):
        val = int(digit) * (1 + (i % 2))
        if val > 9:
            val -= 9
        total += val

    is_valid = total % 10 == 0
    return {
        "valid": is_valid,
        "formatted": id_str,
        "input": id_number,
        "error": None if is_valid else "Check digit validation failed",
    }


def validate_israeli_phone(phone: str) -> dict:
    """Validate Israeli phone number (mobile or landline)."""
    cleaned = re.sub(r"[\s\-\(\)]", "", phone.strip())

    # Convert international format to local
    if cleaned.startswith("+972"):
        cleaned = "0" + cleaned[4:]
    elif cleaned.startswith("972"):
        cleaned = "0" + cleaned[3:]

    mobile_pattern = r"^05[0-9]{8}$"
    landline_pattern = r"^0[2-9][0-9]{7}$"

    is_mobile = bool(re.match(mobile_pattern, cleaned))
    is_landline = bool(re.match(landline_pattern, cleaned))

    if is_mobile:
        formatted = f"{cleaned[:3]}-{cleaned[3:]}"
        phone_type = "mobile"
    elif is_landline:
        formatted = f"{cleaned[:2]}-{cleaned[2:]}"
        phone_type = "landline"
    else:
        return {"valid": False, "error": "Invalid Israeli phone number", "input": phone}

    return {
        "valid": True,
        "formatted": formatted,
        "international": f"+972-{cleaned[1:]}",
        "type": phone_type,
        "input": phone,
    }


def validate_israeli_address(city: str, street: str, number: str, mikud: str = "", apartment: str = "") -> dict:
    """Validate Israeli address fields."""
    errors = []

    if not city or not city.strip():
        errors.append("City (yishuv) is required")

    if not street or not street.strip():
        errors.append("Street (rechov) is required")

    if not number or not number.strip():
        errors.append("House number is required")

    if mikud:
        mikud_clean = mikud.strip().replace("-", "")
        if not re.match(r"^\d{7}$", mikud_clean):
            errors.append("Mikud (postal code) must be 7 digits")

    if errors:
        return {"valid": False, "errors": errors}

    address_parts = [f"{street.strip()} {number.strip()}"]
    if apartment:
        address_parts[0] += f", דירה {apartment.strip()}"
    address_parts.append(city.strip())
    if mikud:
        address_parts[-1] += f", {mikud.strip()}"

    return {
        "valid": True,
        "formatted": "\n".join(address_parts),
        "fields": {
            "city": city.strip(),
            "street": street.strip(),
            "house_number": number.strip(),
            "apartment": apartment.strip() if apartment else None,
            "mikud": mikud.strip() if mikud else None,
        },
    }


# Common government form field mappings
FORM_FIELDS = {
    "tofes-101": {
        "name": "Employee Tax Coordination Form / טופס 101",
        "portal": "Rashut HaMisim (misim.gov.il)",
        "fields": [
            {"name": "shem_prati", "label": "First Name / שם פרטי", "type": "text", "required": True},
            {"name": "shem_mishpacha", "label": "Last Name / שם משפחה", "type": "text", "required": True},
            {"name": "mispar_zehut", "label": "ID Number / מספר זהות", "type": "tz", "required": True},
            {"name": "taarich_leida", "label": "Date of Birth / תאריך לידה", "type": "date", "required": True},
            {"name": "matsav_mishpachti", "label": "Marital Status / מצב משפחתי", "type": "select", "required": True},
            {"name": "ktovet", "label": "Address / כתובת", "type": "address", "required": True},
            {"name": "telefon", "label": "Phone / טלפון", "type": "phone", "required": True},
            {"name": "maasik", "label": "Employer / מעסיק", "type": "text", "required": True},
            {"name": "nekudot_zikui", "label": "Tax Credits / נקודות זיכוי", "type": "number", "required": True},
        ],
    },
    "tofes-106": {
        "name": "Annual Salary Report / טופס 106",
        "portal": "Rashut HaMisim (misim.gov.il)",
        "fields": [
            {"name": "shem_maasik", "label": "Employer Name / שם מעסיק", "type": "text", "required": True},
            {"name": "mispar_tik", "label": "Tax File Number / מספר תיק", "type": "text", "required": True},
            {"name": "shnat_mas", "label": "Tax Year / שנת מס", "type": "number", "required": True},
            {"name": "sachar_bruto", "label": "Gross Salary / שכר ברוטו", "type": "number", "required": True},
            {"name": "mas_shnukai", "label": "Tax Deducted / מס שנוכה", "type": "number", "required": True},
            {"name": "bituach_leumi", "label": "NI Contributions / ביטוח לאומי", "type": "number", "required": True},
        ],
    },
    "dmei-leida": {
        "name": "Maternity Benefit Claim / תביעת דמי לידה",
        "portal": "Bituach Leumi (btl.gov.il)",
        "fields": [
            {"name": "shem_prati", "label": "First Name / שם פרטי", "type": "text", "required": True},
            {"name": "mispar_zehut", "label": "ID Number / מספר זהות", "type": "tz", "required": True},
            {"name": "taarich_leida_yeled", "label": "Child Birth Date / תאריך לידת הילד", "type": "date", "required": True},
            {"name": "maasik", "label": "Employer / מעסיק", "type": "text", "required": True},
            {"name": "sachar_3_chodashim", "label": "Last 3 Months Salary / שכר 3 חודשים אחרונים", "type": "number", "required": True},
            {"name": "taarich_hafsakah", "label": "Work Stop Date / תאריך הפסקת עבודה", "type": "date", "required": True},
        ],
    },
    "rishum-chevra": {
        "name": "Company Registration / רישום חברה",
        "portal": "Rasham HaChevarot (ica.justice.gov.il)",
        "fields": [
            {"name": "shem_chevra_1", "label": "Company Name Option 1 / שם חברה 1", "type": "text", "required": True},
            {"name": "shem_chevra_2", "label": "Company Name Option 2 / שם חברה 2", "type": "text", "required": True},
            {"name": "shem_chevra_3", "label": "Company Name Option 3 / שם חברה 3", "type": "text", "required": True},
            {"name": "hon_meniayot", "label": "Share Capital / הון מניות", "type": "number", "required": True},
            {"name": "ktovet_chevra", "label": "Company Address / כתובת החברה", "type": "address", "required": True},
            {"name": "shem_meyased", "label": "Founder Name / שם מייסד", "type": "text", "required": True},
            {"name": "tz_meyased", "label": "Founder ID / ת.ז. מייסד", "type": "tz", "required": True},
        ],
    },
}


def get_form_fields(form_name: str) -> dict:
    """Get field definitions for a known government form."""
    if form_name in FORM_FIELDS:
        return FORM_FIELDS[form_name]
    return {"error": f"Unknown form: {form_name}", "available_forms": list(FORM_FIELDS.keys())}


def main():
    parser = argparse.ArgumentParser(description="Israeli Government Form Field Helper")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # validate-tz
    tz_parser = subparsers.add_parser("validate-tz", help="Validate Teudat Zehut number")
    tz_parser.add_argument("id_number", help="9-digit Israeli ID number")

    # validate-phone
    phone_parser = subparsers.add_parser("validate-phone", help="Validate Israeli phone number")
    phone_parser.add_argument("phone", help="Israeli phone number")

    # validate-address
    addr_parser = subparsers.add_parser("validate-address", help="Validate Israeli address")
    addr_parser.add_argument("--city", required=True, help="City name")
    addr_parser.add_argument("--street", required=True, help="Street name")
    addr_parser.add_argument("--number", required=True, help="House number")
    addr_parser.add_argument("--mikud", default="", help="Postal code (7 digits)")
    addr_parser.add_argument("--apartment", default="", help="Apartment number")

    # form-fields
    form_parser = subparsers.add_parser("form-fields", help="Get form field definitions")
    form_parser.add_argument("--form", required=True, help="Form name (e.g., tofes-101)")
    form_parser.add_argument("--list", action="store_true", help="List available forms")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "validate-tz":
        result = validate_teudat_zehut(args.id_number)
    elif args.command == "validate-phone":
        result = validate_israeli_phone(args.phone)
    elif args.command == "validate-address":
        result = validate_israeli_address(args.city, args.street, args.number, args.mikud, args.apartment)
    elif args.command == "form-fields":
        if args.list:
            result = {"available_forms": list(FORM_FIELDS.keys())}
        else:
            result = get_form_fields(args.form)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
