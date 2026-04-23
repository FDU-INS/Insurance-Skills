#!/usr/bin/env python3
"""
HealthSim Cohort Loader

Loads JSON cohort files into DuckDB canonical tables.

Usage:
    python cohort_loader.py <cohort_path> [--db <duckdb_path>]

Example:
    python cohort_loader.py cohorts/saved/bob-thompson-er-visit
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import uuid

try:
    import duckdb
except ImportError:
    print("Error: duckdb not installed. Run: pip install duckdb")
    sys.exit(1)


# Entity type to table mapping
ENTITY_TABLE_MAP = {
    # Core
    "person": "persons",
    "provider": "providers",
    "facility": "facilities",
    
    # PatientSim
    "patient": "patients",
    "encounter": "encounters",
    "diagnosis": "diagnoses",
    "procedure": "procedures",
    "lab_result": "lab_results",
    "medication": "medications",
    "allergy": "allergies",
    "vital": "vitals",
    
    # MemberSim
    "member": "members",
    "accumulator": "accumulators",
    "claim": "claims",
    "claim_line": "claim_lines",
    "authorization": "authorizations",
    
    # RxMemberSim
    "rx_member": "rx_members",
    "prescription": "prescriptions",
    "pharmacy_claim": "pharmacy_claims",
    "dur_alert": "dur_alerts",
    "pharmacy": "pharmacies",
    
    # TrialSim
    "study": "studies",
    "site": "sites",
    "treatment_arm": "treatment_arms",
    "subject": "subjects",
    "adverse_event": "adverse_events",
    "visit_schedule": "visit_schedule",
    "actual_visit": "actual_visits",
    "disposition_event": "disposition_events",
    
    # PopulationSim
    "geographic_entity": "geographic_entities",
    "population_profile": "population_profiles",
    "health_indicator": "health_indicators",
    "sdoh_index": "sdoh_indices",
    "cohort_specification": "cohort_specifications",
    
    # NetworkSim
    "network": "networks",
    "network_provider": "network_providers",
    "network_facility": "network_facilities",
    "provider_specialty": "provider_specialties",
}

# Primary key field for each entity type
ENTITY_PK_MAP = {
    "person": "person_id",
    "provider": "provider_id",
    "facility": "facility_id",
    "patient": "patient_id",
    "encounter": "encounter_id",
    "diagnosis": "diagnosis_id",
    "procedure": "procedure_id",
    "lab_result": "lab_result_id",
    "medication": "medication_id",
    "allergy": "allergy_id",
    "vital": "vital_id",
    "member": "member_id",
    "accumulator": "accumulator_id",
    "claim": "claim_id",
    "claim_line": "claim_line_id",
    "authorization": "authorization_id",
    "rx_member": "rx_member_id",
    "prescription": "prescription_id",
    "pharmacy_claim": "pharmacy_claim_id",
    "dur_alert": "dur_alert_id",
    "pharmacy": "pharmacy_id",
    "study": "study_id",
    "site": "site_id",
    "treatment_arm": "arm_id",
    "subject": "subject_id",
    "adverse_event": "ae_id",
    "visit_schedule": "visit_schedule_id",
    "actual_visit": "actual_visit_id",
    "disposition_event": "disposition_id",
    "geographic_entity": "geo_id",
    "population_profile": "profile_id",
    "health_indicator": "indicator_id",
    "sdoh_index": "sdoh_id",
    "cohort_specification": "cohort_spec_id",
    "network": "network_id",
    "network_provider": "network_provider_id",
    "network_facility": "network_facility_id",
    "provider_specialty": "specialty_id",
}


class CohortLoader:
    """Loads JSON cohorts into DuckDB."""
    
    def __init__(self, db_path: str):
        """Initialize with database path."""
        self.db_path = db_path
        self.conn = duckdb.connect(db_path)
        self.loaded_entities: List[tuple] = []  # (entity_type, entity_id)
        
    def close(self):
        """Close database connection."""
        self.conn.close()
        
    def get_table_columns(self, table_name: str) -> List[str]:
        """Get column names for a table."""
        result = self.conn.execute(f"DESCRIBE {table_name}").fetchall()
        return [row[0] for row in result]
    
    def insert_entity(self, entity_type: str, data: Dict[str, Any]) -> Optional[str]:
        """Insert a single entity into the appropriate table."""
        table_name = ENTITY_TABLE_MAP.get(entity_type)
        if not table_name:
            print(f"  Warning: Unknown entity type '{entity_type}'")
            return None
            
        pk_field = ENTITY_PK_MAP.get(entity_type)
        if not pk_field:
            print(f"  Warning: No PK defined for entity type '{entity_type}'")
            return None
            
        # Get table columns
        table_columns = self.get_table_columns(table_name)
        
        # Filter data to only include columns that exist in table
        filtered_data = {k: v for k, v in data.items() if k in table_columns}
        
        if not filtered_data:
            print(f"  Warning: No matching columns for {entity_type}")
            return None
            
        # Build INSERT statement
        columns = list(filtered_data.keys())
        placeholders = ", ".join(["?" for _ in columns])
        column_list = ", ".join(columns)
        
        sql = f"INSERT INTO {table_name} ({column_list}) VALUES ({placeholders})"
        values = [filtered_data[col] for col in columns]
        
        try:
            self.conn.execute(sql, values)
            entity_id = filtered_data.get(pk_field)
            if entity_id:
                self.loaded_entities.append((entity_type, entity_id))
            return entity_id
        except Exception as e:
            print(f"  Error inserting {entity_type}: {e}")
            return None
    
    def load_json_file(self, file_path: Path) -> int:
        """Load entities from a JSON file. Returns count of entities loaded."""
        count = 0
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Handle different JSON structures
        if isinstance(data, dict):
            for key, value in data.items():
                # Singular key maps to entity type
                entity_type = key.rstrip('s')  # Remove trailing 's' for plurals
                if entity_type in ENTITY_TABLE_MAP:
                    if isinstance(value, list):
                        for item in value:
                            if self.insert_entity(entity_type, item):
                                count += 1
                    elif isinstance(value, dict):
                        if self.insert_entity(entity_type, value):
                            count += 1
                # Handle already plural keys
                elif key in ENTITY_TABLE_MAP:
                    if isinstance(value, list):
                        for item in value:
                            if self.insert_entity(key, item):
                                count += 1
                    elif isinstance(value, dict):
                        if self.insert_entity(key, value):
                            count += 1
        
        return count
    
    def load_cohort(self, cohort_path: str, cohort_name: Optional[str] = None) -> Dict[str, Any]:
        """Load all JSON files from a cohort directory."""
        path = Path(cohort_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Cohort path not found: {cohort_path}")
        
        # Determine cohort name
        if cohort_name is None:
            cohort_name = path.name
        
        # Generate cohort ID
        cohort_id = f"SCN-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        print(f"\nLoading cohort: {cohort_name}")
        print(f"Cohort ID: {cohort_id}")
        print("-" * 50)
        
        # Find all JSON files
        json_files = list(path.glob("*.json"))
        
        if not json_files:
            raise ValueError(f"No JSON files found in {cohort_path}")
        
        total_count = 0
        file_counts = {}
        
        for json_file in json_files:
            print(f"\nProcessing: {json_file.name}")
            count = self.load_json_file(json_file)
            file_counts[json_file.name] = count
            total_count += count
            print(f"  Loaded {count} entities")
        
        # Create cohort record
        self.conn.execute("""
            INSERT INTO cohorts (cohort_id, name, description, entity_count, is_active, schema_version)
            VALUES (?, ?, ?, ?, TRUE, '1.0')
        """, [cohort_id, cohort_name, f"Loaded from {cohort_path}", total_count])
        
        # Link entities to cohort
        for entity_type, entity_id in self.loaded_entities:
            self.conn.execute("""
                INSERT INTO cohort_entities (cohort_id, entity_type, entity_id)
                VALUES (?, ?, ?)
            """, [cohort_id, entity_type, entity_id])
        
        # Commit
        self.conn.commit()
        
        print("\n" + "=" * 50)
        print(f"Cohort loaded successfully!")
        print(f"  Total entities: {total_count}")
        print(f"  Files processed: {len(json_files)}")
        
        return {
            "cohort_id": cohort_id,
            "cohort_name": cohort_name,
            "total_entities": total_count,
            "file_counts": file_counts
        }


def main():
    parser = argparse.ArgumentParser(description="Load HealthSim cohort into DuckDB")
    parser.add_argument("cohort_path", help="Path to cohort directory")
    parser.add_argument("--db", default="healthsim.duckdb", help="DuckDB database path")
    parser.add_argument("--name", help="Override cohort name")
    
    args = parser.parse_args()
    
    # Find database
    db_path = args.db
    if not os.path.exists(db_path):
        # Try looking in common locations
        workspace_root = Path(__file__).parent.parent
        alt_path = workspace_root / "healthsim.duckdb"
        if alt_path.exists():
            db_path = str(alt_path)
        else:
            print(f"Error: Database not found at {db_path}")
            sys.exit(1)
    
    loader = CohortLoader(db_path)
    
    try:
        result = loader.load_cohort(args.cohort_path, args.name)
        print(f"\nCohort ID: {result['cohort_id']}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        loader.close()


if __name__ == "__main__":
    main()
