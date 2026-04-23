#!/usr/bin/env python3
"""
Compliance checker - check carrier FMCSA compliance and track expiries.
"""
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.freight_db import get_connection, get_carrier_by_mc


def check_carrier_compliance(mc_number: str) -> dict:
    """Check if carrier is compliant."""
    from scripts.fmcsa_vet import vet_carrier
    
    vet_result = vet_carrier(mc_number)
    
    carrier = get_carrier_by_mc(mc_number)
    
    compliant = vet_result.get("vetting_status") == "PASS"
    warnings = []
    
    if carrier and carrier.get("insurance_expiry"):
        try:
            expiry = datetime.fromisoformat(carrier["insurance_expiry"])
            days_until = (expiry - datetime.now()).days
            if days_until < 0:
                compliant = False
                warnings.append(f"Insurance EXPIRED ({abs(days_until)} days ago)")
            elif days_until < 14:
                warnings.append(f"Insurance expires in {days_until} days")
            elif days_until < 30:
                warnings.append(f"Insurance expires in {days_until} days - renew soon")
        except:
            pass
    
    return {
        "mc_number": mc_number,
        "compliant": compliant,
        "vetting_status": vet_result.get("vetting_status"),
        "warnings": warnings,
        "carrier_info": vet_result.get("carrier_info", {})
    }


def scan_all_compliance() -> list:
    """Scan all carriers broker has worked with."""
    conn = get_connection()
    carriers = conn.execute("SELECT mc_number FROM carriers").fetchall()
    
    results = []
    for row in carriers:
        mc = row[0]
        if mc:
            results.append(check_carrier_compliance(mc))
    
    return results


def get_expiry_alerts() -> list:
    """Get list of upcoming insurance expiries."""
    conn = get_connection()
    
    carriers = conn.execute(
        "SELECT mc_number, name, insurance_expiry FROM carriers WHERE insurance_expiry IS NOT NULL"
    ).fetchall()
    
    alerts = []
    now = datetime.now()
    
    for row in carriers:
        mc, name, expiry_str = row
        try:
            expiry = datetime.fromisoformat(expiry_str)
            days = (expiry - now).days
            
            if days < 30:
                alerts.append({
                    "mc_number": mc,
                    "carrier_name": name,
                    "days_until": days,
                    "urgency": "EXPIRED" if days < 0 else "CRITICAL" if days < 7 else "WARNING"
                })
        except:
            pass
    
    return sorted(alerts, key=lambda x: x["days_until"])


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Check carrier compliance")
    parser.add_argument("--mc", help="Check specific MC number")
    parser.add_argument("--scan-all", action="store_true", help="Scan all carriers")
    parser.add_argument("--expiry-alerts", action="store_true", help="Show expiry alerts")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    
    if args.mc:
        result = check_carrier_compliance(args.mc)
        print(json.dumps(result, indent=2) if args.json else f"{result['mc_number']}: {'✅ Compliant' if result['compliant'] else '❌ Not compliant'}")
    elif args.scan_all:
        results = scan_all_compliance()
        for r in results:
            print(f"{r['mc_number']}: {'✅' if r['compliant'] else '❌'} {', '.join(r['warnings'])}")
    elif args.expiry_alerts:
        alerts = get_expiry_alerts()
        for a in alerts:
            emoji = "🔴" if a["urgency"] == "EXPIRED" else "🟠" if a["urgency"] == "CRITICAL" else "🟡"
            print(f"{emoji} {a['carrier_name']} (MC#{a['mc_number']}): {a['days_until']} days")
    else:
        print("Use --mc, --scan-all, or --expiry-alerts")
