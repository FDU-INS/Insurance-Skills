#!/usr/bin/env python3
"""
Pre-Trip Checker (Agent 7)
Combines Visa/Documents (7A) and Safety/Alerts (7B)
"""

import argparse
import json
from datetime import datetime, timedelta
from typing import Dict, List

# Visa-free access by passport (simplified)
VISA_FREE = {
    "SG": {
        "TH": {"days": 30, "type": "visa_free", "purpose": ["tourism", "business"]},
        "JP": {"days": 90, "type": "visa_free", "purpose": ["tourism", "business"]},
        "ID": {"days": 30, "type": "visa_free", "purpose": ["tourism"]},
        "MY": {"days": 30, "type": "visa_free", "purpose": ["tourism", "business"]},
        "US": {"days": 90, "type": "esta_required", "purpose": ["tourism", "business"]},
    },
    "US": {
        "TH": {"days": 30, "type": "visa_free", "purpose": ["tourism"]},
        "JP": {"days": 90, "type": "visa_free", "purpose": ["tourism", "business"]},
    },
}

# Passport validity rules
PASSPORT_RULES = {
    "default": "6_months",  # Must be valid 6 months beyond entry
    "some_countries": "3_months",
    "eu": "duration_of_stay",
}

# Travel advisory levels
ADVISORY_LEVELS = {
    "TH": {"level": 1, "label": "Exercise Normal Precautions", "source": "US"},
    "JP": {"level": 1, "label": "Exercise Normal Precautions", "source": "US"},
    "ID": {"level": 2, "label": "Exercise Increased Caution", "source": "US"},
    "MY": {"level": 1, "label": "Exercise Normal Precautions", "source": "US"},
}

# Vaccination requirements
VACCINATION_REQS = {
    "TH": {"required": [], "recommended": ["Hepatitis A", "Typhoid", "Tetanus"]},
    "JP": {"required": [], "recommended": ["Routine vaccines"]},
    "ID": {"required": ["Yellow Fever (if from endemic)"], "recommended": ["Hepatitis A", "Typhoid", "Malaria prophylaxis"]},
}

# Emergency contacts
EMERGENCY_CONTACTS = {
    "TH": {"police": "191", "ambulance": "1669", "tourist_police": "1155"},
    "JP": {"police": "110", "ambulance": "119", "tourist_info": "03-3201-3331"},
    "ID": {"police": "110", "ambulance": "118", "tourist_info": "+62-21-3831007"},
}

def check_visa(passport_country: str, destination: str, purpose: str, duration: int) -> Dict:
    """Check visa requirements"""
    passport_code = passport_country.upper()
    dest_code = destination.upper()
    
    if passport_code in VISA_FREE and dest_code in VISA_FREE[passport_code]:
        visa_info = VISA_FREE[passport_code][dest_code]
        if purpose in visa_info["purpose"] and duration <= visa_info["days"]:
            return {
                "required": False,
                "type": visa_info["type"],
                "allowed_stay": visa_info["days"],
                "status": "✅ Visa not required",
                "notes": f"{purpose.title()} up to {visa_info['days']} days",
            }
    
    return {
        "required": True,
        "type": "visa_required",
        "status": "⚠️ Visa required",
        "notes": "Apply before travel",
    }

def check_passport_validity(passport_expiry: str, entry_date: str) -> Dict:
    """Check passport validity"""
    if not passport_expiry:
        return {
            "status": "⚠️ Unknown",
            "notes": "Enter passport expiry date",
            "ok": None,
        }
    
    expiry = datetime.strptime(passport_expiry, "%Y-%m-%d")
    entry = datetime.strptime(entry_date, "%Y-%m-%d")
    six_months_after = entry + timedelta(days=180)
    
    if expiry >= six_months_after:
        return {
            "status": "✅ Valid",
            "expires": passport_expiry,
            "rule": "6 months beyond entry",
            "ok": True,
        }
    elif expiry >= entry:
        return {
            "status": "⚠️ May be insufficient",
            "expires": passport_expiry,
            "rule": "6 months beyond entry recommended",
            "ok": False,
        }
    else:
        return {
            "status": "❌ Expired",
            "expires": passport_expiry,
            "rule": "Must be valid for travel",
            "ok": False,
        }

def check_advisories(destination: str) -> Dict:
    """Check travel advisories"""
    dest_code = destination.upper()
    advisory = ADVISORY_LEVELS.get(dest_code, {"level": 1, "label": "No data", "source": "Unknown"})
    
    emoji = "✅" if advisory["level"] == 1 else "⚠️" if advisory["level"] == 2 else "❌"
    
    return {
        "level": advisory["level"],
        "label": advisory["label"],
        "source": advisory["source"],
        "status": f"{emoji} {advisory['label']}",
    }

def check_health(destination: str) -> Dict:
    """Check health requirements"""
    dest_code = destination.upper()
    reqs = VACCINATION_REQS.get(dest_code, {"required": [], "recommended": []})
    
    return {
        "required": reqs["required"],
        "recommended": reqs["recommended"],
        "status": "✅ No mandatory vaccinations" if not reqs["required"] else "⚠️ Vaccinations required",
    }

def get_emergency_contacts(destination: str) -> Dict:
    """Get emergency contacts"""
    dest_code = destination.upper()
    return EMERGENCY_CONTACTS.get(dest_code, {"police": "Unknown", "ambulance": "Unknown"})

def check_pre_trip(passport_country: str, destination: str, depart: str,
                   nationality: str = None, purpose: str = "tourism",
                   duration: int = 7, transit: str = None,
                   passport_expiry: str = None) -> Dict:
    """Main pre-trip check function"""
    
    results = {
        "passport": passport_country.upper(),
        "destination": destination.upper(),
        "depart": depart,
        "nationality": nationality or passport_country,
        "purpose": purpose,
        "duration": duration,
        "visa": check_visa(passport_country, destination, purpose, duration),
        "passport_validity": check_passport_validity(passport_expiry, depart),
        "advisory": check_advisories(destination),
        "health": check_health(destination),
        "emergency_contacts": get_emergency_contacts(destination),
        "transit": None,
        "document_checklist": [],
        "overall_status": "✅ Ready to travel",
    }
    
    # Check transit if applicable
    if transit:
        results["transit"] = check_visa(passport_country, transit, "transit", 1)
    
    # Document checklist
    results["document_checklist"] = [
        "Passport (original + 2 photocopies)",
        "Flight tickets (printed)",
        "Hotel reservations (printed)",
        "Travel insurance policy",
        "Emergency contacts list",
        "Passport photos (2)",
    ]
    
    # Determine overall status
    if results["visa"]["required"] or not results["passport_validity"].get("ok", True):
        results["overall_status"] = "⚠️ Action required before travel"
    
    if results["advisory"]["level"] >= 3:
        results["overall_status"] = "❌ Reconsider travel"
    
    return results

def format_output(data: Dict) -> str:
    """Format for human reading"""
    lines = []
    
    lines.append("🛂 PRE-TRIP CHECKER (Agent 7)")
    lines.append("=" * 70)
    lines.append(f"📍 {data['passport']} → {data['destination']}")
    lines.append(f"📅 Departure: {data['depart']} ({data['duration']} days)")
    lines.append(f"🎯 Purpose: {data['purpose']}")
    lines.append("")
    
    # Visa & Documents (7A)
    lines.append("🛂 VISA & DOCUMENTS (7A)")
    lines.append("-" * 70)
    lines.append(data["visa"]["status"])
    lines.append(f"   {data['visa']['notes']}")
    lines.append("")
    
    lines.append("📄 PASSPORT")
    lines.append(f"   {data['passport_validity']['status']}")
    if data['passport_validity'].get('expires'):
        lines.append(f"   Expires: {data['passport_validity']['expires']}")
    lines.append(f"   Rule: {data['passport_validity'].get('rule', '6 months beyond entry')}")
    lines.append("")
    
    if data.get("transit"):
        lines.append("✈️  TRANSIT")
        lines.append(f"   {data['transit']['status']}")
        lines.append(f"   {data['transit']['notes']}")
        lines.append("")
    
    lines.append("📋 DOCUMENT CHECKLIST")
    for item in data["document_checklist"]:
        lines.append(f"□ {item}")
    lines.append("")
    
    # Safety & Alerts (7B)
    lines.append("🚨 SAFETY & ALERTS (7B)")
    lines.append("-" * 70)
    lines.append("Travel Advisory:")
    lines.append(f"   {data['advisory']['status']}")
    lines.append(f"   Source: {data['advisory']['source']}")
    lines.append("")
    
    lines.append("💉 HEALTH")
    lines.append(f"   {data['health']['status']}")
    if data['health']['required']:
        lines.append(f"   Required: {', '.join(data['health']['required'])}")
    if data['health']['recommended']:
        lines.append(f"   Recommended: {', '.join(data['health']['recommended'])}")
    lines.append("")
    
    lines.append("📞 EMERGENCY CONTACTS")
    contacts = data["emergency_contacts"]
    lines.append(f"   Police: {contacts.get('police', 'N/A')}")
    lines.append(f"   Ambulance: {contacts.get('ambulance', 'N/A')}")
    lines.append("")
    
    lines.append("🎯 OVERALL STATUS")
    lines.append("-" * 70)
    lines.append(data["overall_status"])
    
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Pre-trip verification")
    parser.add_argument("--passport", required=True, help="Passport country code")
    parser.add_argument("--destination", required=True, help="Destination country code")
    parser.add_argument("--depart", required=True, help="Departure date (YYYY-MM-DD)")
    parser.add_argument("--nationality", help="Nationality (if different from passport)")
    parser.add_argument("--purpose", default="tourism", choices=["tourism", "business", "transit"])
    parser.add_argument("--duration", type=int, default=7, help="Trip duration in days")
    parser.add_argument("--transit", help="Transit country code")
    parser.add_argument("--passport-expiry", help="Passport expiry date (YYYY-MM-DD)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    results = check_pre_trip(
        passport_country=args.passport,
        destination=args.destination,
        depart=args.depart,
        nationality=args.nationality,
        purpose=args.purpose,
        duration=args.duration,
        transit=args.transit,
        passport_expiry=args.passport_expiry
    )
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(format_output(results))

if __name__ == "__main__":
    main()
