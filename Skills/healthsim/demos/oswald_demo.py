#!/usr/bin/env python3
"""
Oswald Family Healthcare Journey Demo

Demonstrates the HealthSim Generative Framework through a realistic
multi-product healthcare journey for the Oswald family.

The Journey:
1. Health plan enrollment (MemberSim)
2. Acute medical event - James's heart attack (PatientSim)
3. Ongoing diabetes management (PatientSim)
4. Clinical trial participation (TrialSim)

Usage:
    python oswald_demo.py [--seed 42] [--output ./output]
"""

import argparse
from datetime import date, timedelta
from pathlib import Path
import json
import sys

# Add package to path if running directly
sys.path.insert(0, str(Path(__file__).parent.parent / "packages" / "core" / "src"))

from healthsim.generation import (
    JourneyDefinition,
    EventDefinition,
)
from healthsim.generation.person import Person


def create_oswald_family():
    """Create the Oswald family members."""
    return {
        "james": Person(
            id="james-oswald-001",
            given_name="James",
            family_name="Oswald",
            birth_date=date(1955, 3, 15),
            gender="M",
            conditions=["diabetes", "hypertension"]
        ),
        "margaret": Person(
            id="margaret-oswald-001", 
            given_name="Margaret",
            family_name="Oswald",
            birth_date=date(1958, 7, 22),
            gender="F",
            conditions=["hyperlipidemia"]
        ),
        "michael": Person(
            id="michael-oswald-001",
            given_name="Michael",
            family_name="Oswald",
            birth_date=date(1985, 11, 8),
            gender="M",
            conditions=[]
        )
    }


def demo_health_plan_enrollment(family: dict, start_date: date) -> dict:
    """Phase 1: Health Plan Enrollment (MemberSim)"""
    print("\n" + "="*60)
    print("PHASE 1: Health Plan Enrollment")
    print("="*60)
    
    print(f"  Enrollment Date: {start_date}")
    print(f"  Plan Type: PPO")
    print(f"  Members: James (subscriber), Margaret (spouse), Michael (dependent)")
    
    result = {
        "members": [
            {"id": "MBR-001", "name": "James Oswald", "role": "subscriber"},
            {"id": "MBR-002", "name": "Margaret Oswald", "role": "spouse"},
            {"id": "MBR-003", "name": "Michael Oswald", "role": "dependent"}
        ],
        "coverage_start": start_date.isoformat()
    }
    
    print(f"  ✓ Generated {len(result['members'])} member records")
    return result


def demo_acute_event(james: Person, event_date: date) -> dict:
    """Phase 2: Acute Medical Event - James's Heart Attack (PatientSim)"""
    print("\n" + "="*60)
    print("PHASE 2: Acute Medical Event - James's Heart Attack")
    print("="*60)
    
    journey = JourneyDefinition(
        id="ami-hospitalization",
        description="Acute myocardial infarction hospitalization and follow-up",
        duration_days=90,
        events=[
            EventDefinition(id="er-presentation", event_type="encounter",
                          timing={"type": "fixed", "day": 0}),
            EventDefinition(id="cath-procedure", event_type="procedure",
                          timing={"type": "fixed", "day": 0}),
            EventDefinition(id="inpatient-stay", event_type="encounter",
                          timing={"type": "fixed", "day": 0}),
            EventDefinition(id="cardiology-followup", event_type="encounter",
                          timing={"type": "fixed", "day": 14}),
            EventDefinition(id="cardiac-rehab", event_type="referral",
                          timing={"type": "fixed", "day": 21}),
        ]
    )
    
    print(f"  Event Date: {event_date}")
    print(f"  Diagnosis: Acute ST-elevation MI (I21.0)")
    print(f"  Procedures: PCI with stent placement")
    print(f"  LOS: 4 days")
    
    events = []
    for event_def in journey.events:
        events.append({
            "id": event_def.id,
            "type": event_def.event_type,
            "date": (event_date + timedelta(days=event_def.timing.get("day", 0))).isoformat()
        })
    
    result = {
        "patient": james.id,
        "journey": journey.id,
        "events": events,
        "diagnoses": ["I21.0", "I25.10", "E11.9", "I10"],
    }
    
    print(f"  ✓ Generated {len(events)} clinical events")
    return result


def demo_chronic_management(james: Person, start_date: date) -> dict:
    """Phase 3: Ongoing Diabetes Management (PatientSim)"""
    print("\n" + "="*60)
    print("PHASE 3: Ongoing Diabetes Management")
    print("="*60)
    
    print(f"  Start Date: {start_date}")
    print(f"  Duration: 365 days")
    print(f"  Quarterly Visits: 4 PCP encounters")
    
    events = []
    for q in range(4):
        visit_date = start_date + timedelta(days=q*90)
        events.append({"type": "encounter", "date": visit_date.isoformat()})
        events.append({"type": "lab", "date": visit_date.isoformat(), "test": "HbA1c"})
    
    result = {
        "patient": james.id,
        "events": events,
        "medications": ["metformin", "lisinopril", "atorvastatin", "aspirin"],
    }
    
    print(f"  ✓ Generated {len(events)} care events")
    return result


def demo_clinical_trial(james: Person, enrollment_date: date) -> dict:
    """Phase 4: Clinical Trial Participation (TrialSim)"""
    print("\n" + "="*60)
    print("PHASE 4: Clinical Trial Enrollment")
    print("="*60)
    
    print(f"  Trial: CVOT-2024-001 (Phase III)")
    print(f"  Screening Date: {enrollment_date}")
    
    visits = [{"type": "screening", "date": enrollment_date.isoformat()}]
    baseline = enrollment_date + timedelta(days=14)
    visits.append({"type": "baseline", "date": baseline.isoformat()})
    
    for i in range(8):
        visit_date = baseline + timedelta(weeks=12*(i+1))
        visits.append({"type": f"visit_{i+1}", "date": visit_date.isoformat()})
    
    result = {
        "subject_id": "SUBJ-001",
        "patient": james.id,
        "protocol": "CVOT-2024-001",
        "arm": "treatment",
        "visits": visits,
    }
    
    print(f"  ✓ Subject enrolled, randomized to treatment arm")
    print(f"  ✓ Generated {len(visits)} scheduled visits")
    return result


def run_demo(seed: int = 42, output_dir: Path = None):
    """Run the complete Oswald family demo."""
    print("\n" + "="*60)
    print("   HEALTHSIM GENERATIVE FRAMEWORK DEMO")
    print("   The Oswald Family Healthcare Journey")
    print("="*60)
    
    enrollment_date = date(2024, 1, 1)
    heart_attack_date = date(2024, 6, 15)
    trial_screening = date(2024, 10, 1)
    
    family = create_oswald_family()
    james = family["james"]
    
    print(f"\nFamily Members:")
    for name, person in family.items():
        conditions = ", ".join(person.conditions) if person.conditions else "none"
        print(f"  {person.given_name} {person.family_name} ({person.gender}, born {person.birth_date}) - {conditions}")
    
    results = {}
    results["enrollment"] = demo_health_plan_enrollment(family, enrollment_date)
    results["acute_event"] = demo_acute_event(james, heart_attack_date)
    results["chronic_care"] = demo_chronic_management(james, date(2024, 7, 15))
    results["clinical_trial"] = demo_clinical_trial(james, trial_screening)
    
    print("\n" + "="*60)
    print("DEMO SUMMARY")
    print("="*60)
    
    total_events = (
        len(results['acute_event']['events']) +
        len(results['chronic_care']['events']) +
        len(results['clinical_trial']['visits'])
    )
    print(f"  Total healthcare events generated: {total_events}")
    
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "oswald_demo_results.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n  Results saved to: {output_file}")
    
    print("\n" + "="*60)
    print("Demo complete!")
    print("="*60)
    
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Oswald Family Healthcare Journey Demo")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--output", type=Path, help="Output directory")
    args = parser.parse_args()
    
    run_demo(seed=args.seed, output_dir=args.output)
