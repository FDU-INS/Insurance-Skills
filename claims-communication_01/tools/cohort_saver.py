#!/usr/bin/env python3
"""
HealthSim Cohort Saver

Exports cohorts from DuckDB to JSON files.

Usage:
    python cohort_saver.py <cohort_name> [--output <output_path>] [--db <duckdb_path>]

Example:
    python cohort_saver.py "bob-thompson-er-visit" --output ./exports
"""

import argparse
import json
import os
import sys
from datetime import datetime, date
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import duckdb
except ImportError:
    print("Error: duckdb not installed. Run: pip install duckdb")
    sys.exit(1)


# Entity type to table and PK mapping
ENTITY_CONFIG = {
    # Core
    "person": {"table": "persons", "pk": "person_id"},
    "provider": {"table": "providers", "pk": "provider_id"},
    "facility": {"table": "facilities", "pk": "facility_id"},
    
    # PatientSim
    "patient": {"table": "patients", "pk": "patient_id"},
    "encounter": {"table": "encounters", "pk": "encounter_id"},
    "diagnosis": {"table": "diagnoses", "pk": "diagnosis_id"},
    "procedure": {"table": "procedures", "pk": "procedure_id"},
    "lab_result": {"table": "lab_results", "pk": "lab_result_id"},
    "medication": {"table": "medications", "pk": "medication_id"},
    "allergy": {"table": "allergies", "pk": "allergy_id"},
    "vital": {"table": "vitals", "pk": "vital_id"},
    
    # MemberSim
    "member": {"table": "members", "pk": "member_id"},
    "accumulator": {"table": "accumulators", "pk": "accumulator_id"},
    "claim": {"table": "claims", "pk": "claim_id"},
    "claim_line": {"table": "claim_lines", "pk": "claim_line_id"},
    "authorization": {"table": "authorizations", "pk": "authorization_id"},
    
    # RxMemberSim
    "rx_member": {"table": "rx_members", "pk": "rx_member_id"},
    "prescription": {"table": "prescriptions", "pk": "prescription_id"},
    "pharmacy_claim": {"table": "pharmacy_claims", "pk": "pharmacy_claim_id"},
    "dur_alert": {"table": "dur_alerts", "pk": "dur_alert_id"},
    "pharmacy": {"table": "pharmacies", "pk": "pharmacy_id"},
    
    # TrialSim
    "study": {"table": "studies", "pk": "study_id"},
    "site": {"table": "sites", "pk": "site_id"},
    "treatment_arm": {"table": "treatment_arms", "pk": "arm_id"},
    "subject": {"table": "subjects", "pk": "subject_id"},
    "adverse_event": {"table": "adverse_events", "pk": "ae_id"},
    "visit_schedule": {"table": "visit_schedule", "pk": "visit_schedule_id"},
    "actual_visit": {"table": "actual_visits", "pk": "actual_visit_id"},
    "disposition_event": {"table": "disposition_events", "pk": "disposition_id"},
    
    # PopulationSim
    "geographic_entity": {"table": "geographic_entities", "pk": "geo_id"},
    "population_profile": {"table": "population_profiles", "pk": "profile_id"},
    "health_indicator": {"table": "health_indicators", "pk": "indicator_id"},
    "sdoh_index": {"table": "sdoh_indices", "pk": "sdoh_id"},
    "cohort_specification": {"table": "cohort_specifications", "pk": "cohort_spec_id"},
    
    # NetworkSim
    "network": {"table": "networks", "pk": "network_id"},
    "network_provider": {"table": "network_providers", "pk": "network_provider_id"},
    "network_facility": {"table": "network_facilities", "pk": "network_facility_id"},
    "provider_specialty": {"table": "provider_specialties", "pk": "specialty_id"},
}

# Group entity types by product for organized export
PRODUCT_ENTITIES = {
    "core": ["person", "provider", "facility"],
    "patientsim": ["patient", "encounter", "diagnosis", "procedure", "lab_result", "medication", "allergy", "vital"],
    "membersim": ["member", "accumulator", "claim", "claim_line", "authorization"],
    "rxmembersim": ["rx_member", "prescription", "pharmacy_claim", "dur_alert", "pharmacy"],
    "trialsim": ["study", "site", "treatment_arm", "subject", "adverse_event", "visit_schedule", "actual_visit", "disposition_event"],
    "populationsim": ["geographic_entity", "population_profile", "health_indicator", "sdoh_index", "cohort_specification"],
    "networksim": ["network", "network_provider", "network_facility", "provider_specialty"],
}


class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for dates and decimals."""
    
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


class CohortSaver:
    """Exports cohorts from DuckDB to JSON files."""
    
    def __init__(self, db_path: str):
        """Initialize with database path."""
        self.db_path = db_path
        self.conn = duckdb.connect(db_path, read_only=True)
        
    def close(self):
        """Close database connection."""
        self.conn.close()
    
    def get_cohort(self, cohort_name: str) -> Optional[Dict[str, Any]]:
        """Get cohort by name."""
        result = self.conn.execute("""
            SELECT cohort_id, name, description, created_at, entity_count, products
            FROM cohorts
            WHERE name = ?
        """, [cohort_name]).fetchone()
        
        if not result:
            return None
            
        return {
            "cohort_id": result[0],
            "name": result[1],
            "description": result[2],
            "created_at": result[3],
            "entity_count": result[4],
            "products": result[5]
        }
    
    def get_cohort_entities(self, cohort_id: str) -> List[tuple]:
        """Get all entity references for a cohort."""
        return self.conn.execute("""
            SELECT entity_type, entity_id
            FROM cohort_entities
            WHERE cohort_id = ?
            ORDER BY entity_type, entity_id
        """, [cohort_id]).fetchall()
    
    def get_cohort_tags(self, cohort_id: str) -> List[str]:
        """Get tags for a cohort."""
        results = self.conn.execute("""
            SELECT tag FROM cohort_tags WHERE cohort_id = ?
        """, [cohort_id]).fetchall()
        return [r[0] for r in results]
    
    def fetch_entity(self, entity_type: str, entity_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a single entity from the database."""
        config = ENTITY_CONFIG.get(entity_type)
        if not config:
            return None
        
        table = config["table"]
        pk = config["pk"]
        
        # Get column names
        cols = self.conn.execute(f"DESCRIBE {table}").fetchall()
        column_names = [c[0] for c in cols]
        
        # Fetch entity
        result = self.conn.execute(f"""
            SELECT * FROM {table} WHERE {pk} = ?
        """, [entity_id]).fetchone()
        
        if not result:
            return None
        
        # Convert to dict, excluding None values
        entity = {}
        for i, col in enumerate(column_names):
            if result[i] is not None:
                entity[col] = result[i]
        
        return entity
    
    def save_cohort(self, cohort_name: str, output_path: str, 
                      format: str = "by_product") -> Dict[str, Any]:
        """
        Save cohort to JSON files.
        
        Args:
            cohort_name: Name of cohort to export
            output_path: Directory to save files
            format: 'by_product' (separate files per product) or 'single' (one file)
        """
        # Get cohort
        cohort = self.get_cohort(cohort_name)
        if not cohort:
            raise ValueError(f"Cohort not found: {cohort_name}")
        
        cohort_id = cohort["cohort_id"]
        
        # Create output directory
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\nExporting cohort: {cohort_name}")
        print(f"Cohort ID: {cohort_id}")
        print(f"Output: {output_dir}")
        print("-" * 50)
        
        # Get all entity references
        entity_refs = self.get_cohort_entities(cohort_id)
        tags = self.get_cohort_tags(cohort_id)
        
        # Organize entities by type
        entities_by_type: Dict[str, List[Dict]] = {}
        
        for entity_type, entity_id in entity_refs:
            entity = self.fetch_entity(entity_type, entity_id)
            if entity:
                if entity_type not in entities_by_type:
                    entities_by_type[entity_type] = []
                entities_by_type[entity_type].append(entity)
        
        # Count
        total_entities = sum(len(v) for v in entities_by_type.values())
        
        if format == "by_product":
            # Save separate files per product
            files_written = []
            
            for product, entity_types in PRODUCT_ENTITIES.items():
                product_data = {}
                has_data = False
                
                for entity_type in entity_types:
                    if entity_type in entities_by_type:
                        # Use plural form for JSON keys
                        key = entity_type + "s" if not entity_type.endswith("s") else entity_type
                        product_data[key] = entities_by_type[entity_type]
                        has_data = True
                
                if has_data:
                    filename = f"{product}.json"
                    filepath = output_dir / filename
                    with open(filepath, 'w') as f:
                        json.dump(product_data, f, indent=2, cls=JSONEncoder)
                    files_written.append(filename)
                    print(f"  Wrote {filename}: {sum(len(v) for v in product_data.values())} entities")
            
            # Save cohort metadata
            metadata = {
                "cohort_id": cohort_id,
                "name": cohort_name,
                "description": cohort.get("description"),
                "created_at": cohort.get("created_at"),
                "exported_at": datetime.now().isoformat(),
                "entity_count": total_entities,
                "tags": tags,
                "files": files_written
            }
            
            with open(output_dir / "cohort.json", 'w') as f:
                json.dump(metadata, f, indent=2, cls=JSONEncoder)
            
        else:  # single file
            # Save everything in one file
            all_data = {
                "cohort": {
                    "cohort_id": cohort_id,
                    "name": cohort_name,
                    "description": cohort.get("description"),
                    "tags": tags
                },
                "entities": entities_by_type
            }
            
            with open(output_dir / f"{cohort_name}.json", 'w') as f:
                json.dump(all_data, f, indent=2, cls=JSONEncoder)
        
        # Write README
        readme_content = f"""# {cohort_name}

Exported from HealthSim DuckDB on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

- **Cohort ID**: {cohort_id}
- **Total Entities**: {total_entities}
- **Tags**: {', '.join(tags) if tags else 'None'}

## Entity Counts

| Entity Type | Count |
|-------------|-------|
"""
        for entity_type, entities in sorted(entities_by_type.items()):
            readme_content += f"| {entity_type} | {len(entities)} |\n"
        
        with open(output_dir / "README.md", 'w') as f:
            f.write(readme_content)
        
        print("\n" + "=" * 50)
        print(f"Export complete!")
        print(f"  Total entities: {total_entities}")
        print(f"  Output directory: {output_dir}")
        
        return {
            "cohort_id": cohort_id,
            "cohort_name": cohort_name,
            "total_entities": total_entities,
            "output_path": str(output_dir)
        }


def main():
    parser = argparse.ArgumentParser(description="Export HealthSim cohort to JSON")
    parser.add_argument("cohort_name", help="Name of cohort to export")
    parser.add_argument("--output", "-o", default="./exports", help="Output directory")
    parser.add_argument("--db", default="healthsim.duckdb", help="DuckDB database path")
    parser.add_argument("--format", choices=["by_product", "single"], default="by_product",
                        help="Export format: separate files per product or single file")
    
    args = parser.parse_args()
    
    # Find database
    db_path = args.db
    if not os.path.exists(db_path):
        workspace_root = Path(__file__).parent.parent
        alt_path = workspace_root / "healthsim.duckdb"
        if alt_path.exists():
            db_path = str(alt_path)
        else:
            print(f"Error: Database not found at {db_path}")
            sys.exit(1)
    
    # Create output path with cohort name
    output_path = Path(args.output) / args.cohort_name.replace(" ", "-").lower()
    
    saver = CohortSaver(db_path)
    
    try:
        result = saver.save_cohort(args.cohort_name, str(output_path), args.format)
        print(f"\nExported to: {result['output_path']}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        saver.close()


if __name__ == "__main__":
    main()
