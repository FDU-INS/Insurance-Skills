"""Tests for PopulationSim reference data import."""

import pytest
from pathlib import Path
import tempfile
import duckdb

from healthsim.db import DatabaseConnection
from healthsim.db.reference import (
    import_all_reference_data,
    get_reference_status,
    is_reference_data_loaded,
    REFERENCE_TABLES,
)
from healthsim.db.reference.populationsim import (
    import_places_tract,
    import_places_county,
    import_svi_tract,
    import_svi_county,
    import_adi_blockgroup,
    get_populationsim_data_path,
)


@pytest.fixture
def test_db():
    """Create a temporary test database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.duckdb"
        db_conn = DatabaseConnection(db_path)
        conn = db_conn.connect()
        yield conn
        db_conn.close()


@pytest.fixture
def data_path():
    """Get the PopulationSim data path."""
    return get_populationsim_data_path()


class TestDataPathDiscovery:
    """Tests for finding the data directory."""
    
    def test_data_path_exists(self, data_path):
        """Data path should exist."""
        assert data_path.exists(), f"Data path not found: {data_path}"
    
    def test_places_tract_csv_exists(self, data_path):
        """PLACES tract CSV should exist."""
        csv_path = data_path / "tract" / "places_tract_2024.csv"
        assert csv_path.exists(), f"CSV not found: {csv_path}"
    
    def test_svi_tract_csv_exists(self, data_path):
        """SVI tract CSV should exist."""
        csv_path = data_path / "tract" / "svi_tract_2022.csv"
        assert csv_path.exists(), f"CSV not found: {csv_path}"
    
    def test_adi_blockgroup_csv_exists(self, data_path):
        """ADI block group CSV should exist."""
        csv_path = data_path / "block_group" / "adi_blockgroup_2023.csv"
        assert csv_path.exists(), f"CSV not found: {csv_path}"


class TestPlacesTractImport:
    """Tests for CDC PLACES tract data import."""
    
    def test_import_creates_table(self, test_db):
        """Import should create the table."""
        count = import_places_tract(test_db)
        assert count > 80000, f"Expected >80000 rows, got {count}"
    
    def test_table_has_expected_columns(self, test_db):
        """Table should have key columns."""
        import_places_tract(test_db)
        
        # Check for key columns (normalized to lowercase)
        columns = test_db.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'ref_places_tract'
        """).fetchall()
        column_names = [c[0] for c in columns]
        
        expected_columns = ['stateabbr', 'countyfips', 'tractfips', 'totalpopulation']
        for col in expected_columns:
            assert col in column_names, f"Missing column: {col}"
    
    def test_skip_if_exists(self, test_db):
        """Should skip import if table already exists."""
        count1 = import_places_tract(test_db)
        count2 = import_places_tract(test_db, replace=False)
        assert count1 == count2
    
    def test_replace_reimports(self, test_db):
        """Replace=True should reimport data."""
        count1 = import_places_tract(test_db)
        count2 = import_places_tract(test_db, replace=True)
        assert count1 == count2  # Same data, but reimported


class TestPlacesCountyImport:
    """Tests for CDC PLACES county data import."""
    
    def test_import_creates_table(self, test_db):
        """Import should create the table."""
        count = import_places_county(test_db)
        assert count > 3000, f"Expected >3000 rows, got {count}"


class TestSviTractImport:
    """Tests for SVI tract data import."""
    
    def test_import_creates_table(self, test_db):
        """Import should create the table."""
        count = import_svi_tract(test_db)
        assert count > 80000, f"Expected >80000 rows, got {count}"
    
    def test_table_has_vulnerability_columns(self, test_db):
        """Table should have vulnerability theme columns."""
        import_svi_tract(test_db)
        
        columns = test_db.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'ref_svi_tract'
        """).fetchall()
        column_names = [c[0] for c in columns]
        
        # Check for theme columns
        assert 'rpl_themes' in column_names, "Missing rpl_themes column"


class TestSviCountyImport:
    """Tests for SVI county data import."""
    
    def test_import_creates_table(self, test_db):
        """Import should create the table."""
        count = import_svi_county(test_db)
        assert count > 3000, f"Expected >3000 rows, got {count}"


class TestAdiBlockgroupImport:
    """Tests for ADI block group data import."""
    
    def test_import_creates_table(self, test_db):
        """Import should create the table."""
        count = import_adi_blockgroup(test_db)
        assert count > 200000, f"Expected >200000 rows, got {count}"
    
    def test_table_has_adi_columns(self, test_db):
        """Table should have ADI ranking columns."""
        import_adi_blockgroup(test_db)
        
        columns = test_db.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'ref_adi_blockgroup'
        """).fetchall()
        column_names = [c[0] for c in columns]
        
        assert 'adi_natrank' in column_names, "Missing adi_natrank column"
        assert 'adi_staternk' in column_names, "Missing adi_staternk column"


class TestAllDataImport:
    """Tests for importing all reference data."""
    
    def test_import_all_data(self, test_db):
        """Import all PopulationSim data."""
        results = import_all_reference_data(test_db, verbose=False)
        
        assert results['ref_places_tract'] > 80000
        assert results['ref_places_county'] > 3000
        assert results['ref_svi_tract'] > 80000
        assert results['ref_svi_county'] > 3000
        assert results['ref_adi_blockgroup'] > 200000


class TestReferenceStatus:
    """Tests for reference data status checking."""
    
    def test_status_before_import(self, test_db):
        """Status should show no data before import."""
        status = get_reference_status(test_db)
        
        for table_name, info in status.items():
            assert not info["exists"], f"{table_name} should not exist"
            assert not info["healthy"], f"{table_name} should not be healthy"
    
    def test_status_after_import(self, test_db):
        """Status should show healthy data after import."""
        import_all_reference_data(test_db, verbose=False)
        status = get_reference_status(test_db)
        
        for table_name, info in status.items():
            assert info["exists"], f"{table_name} should exist"
            assert info["healthy"], f"{table_name} should be healthy"
    
    def test_is_reference_data_loaded(self, test_db):
        """is_reference_data_loaded should return correct status."""
        assert not is_reference_data_loaded(test_db)
        
        import_all_reference_data(test_db, verbose=False)
        
        assert is_reference_data_loaded(test_db)


class TestGeographicQueries:
    """Tests for querying reference data by location."""
    
    def test_query_san_diego_diabetes(self, test_db):
        """Query San Diego County diabetes rates."""
        import_places_tract(test_db)
        
        result = test_db.execute("""
            SELECT AVG(diabetes_crudeprev) as avg_diabetes
            FROM ref_places_tract
            WHERE countyfips = '06073'
        """).fetchone()
        
        assert result[0] is not None
        assert 5.0 < result[0] < 25.0, f"Unexpected diabetes rate: {result[0]}"
    
    def test_query_california_tracts(self, test_db):
        """Query California tract count."""
        import_places_tract(test_db)
        
        result = test_db.execute("""
            SELECT COUNT(*) FROM ref_places_tract
            WHERE stateabbr = 'CA'
        """).fetchone()
        
        # California has ~8000+ census tracts
        assert result[0] > 8000, f"Expected >8000 CA tracts, got {result[0]}"
    
    def test_query_svi_high_vulnerability(self, test_db):
        """Query high vulnerability tracts."""
        import_svi_tract(test_db)
        
        # RPL_THEMES ranges from 0 to 1, higher = more vulnerable
        result = test_db.execute("""
            SELECT COUNT(*) FROM ref_svi_tract
            WHERE rpl_themes > 0.9
        """).fetchone()
        
        # About 10% should be highly vulnerable
        assert result[0] > 5000, f"Expected >5000 high vulnerability tracts, got {result[0]}"
    
    def test_join_places_and_svi(self, test_db):
        """Join PLACES and SVI data."""
        import_places_tract(test_db)
        import_svi_tract(test_db)
        
        # Join on tract FIPS
        result = test_db.execute("""
            SELECT p.tractfips, p.diabetes_crudeprev, s.rpl_themes
            FROM ref_places_tract p
            JOIN ref_svi_tract s ON p.tractfips = s.fips
            WHERE p.countyfips = '06073'
            LIMIT 10
        """).fetchall()
        
        assert len(result) > 0, "Join should return results"
        for row in result:
            assert row[0] is not None  # tract FIPS
            assert row[1] is not None  # diabetes rate
            assert row[2] is not None  # vulnerability score
