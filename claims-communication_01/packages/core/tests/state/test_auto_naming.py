"""Tests for auto-naming service."""

import pytest
from datetime import datetime
from unittest.mock import MagicMock

from healthsim.state.auto_naming import (
    extract_keywords,
    sanitize_name,
    ensure_unique_name,
    generate_cohort_name,
    parse_cohort_name,
)


class TestExtractKeywords:
    """Test keyword extraction from context."""
    
    def test_extract_healthcare_keywords_prioritized(self):
        """Healthcare keywords should be prioritized."""
        context = "Generate 50 diabetic patients with hypertension"
        keywords = extract_keywords(context)
        
        assert 'diabetic' in keywords or 'hypertension' in keywords
    
    def test_extract_with_entity_type(self):
        """Entity type should be added if not present."""
        context = "Generate some records"
        keywords = extract_keywords(context, entity_type="patient")
        
        assert 'patients' in keywords
    
    def test_extract_filters_stop_words(self):
        """Stop words should be filtered out."""
        context = "Generate a patient with the condition"
        keywords = extract_keywords(context)
        
        for word in ['a', 'the', 'with', 'generate']:
            assert word not in keywords
    
    def test_extract_max_keywords(self):
        """Should respect max_keywords limit."""
        context = "diabetes hypertension cardiac renal hepatic"
        keywords = extract_keywords(context, max_keywords=2)
        
        assert len(keywords) <= 2
    
    def test_extract_empty_context(self):
        """Empty context should return empty list unless entity_type provided."""
        keywords = extract_keywords(None)
        assert keywords == []
        
        keywords = extract_keywords(None, entity_type="claim")
        assert 'claims' in keywords
    
    def test_extract_short_words_filtered(self):
        """Words less than 3 characters should be filtered."""
        context = "an ER visit to the ED"
        keywords = extract_keywords(context)
        
        assert 'an' not in keywords
        assert 'to' not in keywords


class TestSanitizeName:
    """Test name sanitization."""
    
    def test_lowercase_conversion(self):
        """Should convert to lowercase."""
        assert sanitize_name("MyCohort") == "mycohort"
    
    def test_space_replacement(self):
        """Should replace spaces with hyphens."""
        assert sanitize_name("my cohort") == "my-cohort"
    
    def test_underscore_replacement(self):
        """Should replace underscores with hyphens."""
        assert sanitize_name("my_cohort") == "my-cohort"
    
    def test_special_char_removal(self):
        """Should remove special characters."""
        assert sanitize_name("my@cohort!") == "mycohort"
    
    def test_multiple_hyphens_collapsed(self):
        """Should collapse multiple hyphens."""
        assert sanitize_name("my--cohort") == "my-cohort"
    
    def test_leading_trailing_hyphens_stripped(self):
        """Should strip leading/trailing hyphens."""
        assert sanitize_name("-my-cohort-") == "my-cohort"
    
    def test_length_limit(self):
        """Should limit length to 50 characters."""
        long_name = "a" * 100
        result = sanitize_name(long_name)
        assert len(result) <= 50


class TestEnsureUniqueName:
    """Test unique name generation."""
    
    def test_unique_name_unchanged(self):
        """Unique name should be returned unchanged."""
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchone.return_value = (0,)
        
        result = ensure_unique_name("my-cohort", mock_conn)
        assert result == "my-cohort"
    
    def test_duplicate_name_gets_counter(self):
        """Duplicate name should get counter appended."""
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchone.side_effect = [(1,), (0,)]
        
        result = ensure_unique_name("my-cohort", mock_conn)
        assert result == "my-cohort-2"
    
    def test_multiple_duplicates_increment(self):
        """Multiple duplicates should increment counter."""
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchone.side_effect = [(1,), (1,), (0,)]
        
        result = ensure_unique_name("my-cohort", mock_conn)
        assert result == "my-cohort-3"


class TestGenerateCohortName:
    """Test cohort name generation."""
    
    def test_with_explicit_keywords(self):
        """Should use explicit keywords."""
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchone.return_value = (0,)
        
        result = generate_cohort_name(
            keywords=["diabetes", "elderly"],
            include_date=False,
            connection=mock_conn
        )
        
        assert "diabetes" in result
        assert "elderly" in result
    
    def test_with_context(self):
        """Should extract keywords from context."""
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchone.return_value = (0,)
        
        result = generate_cohort_name(
            context="Generate 50 diabetic patients",
            include_date=False,
            connection=mock_conn
        )
        
        assert "diabetic" in result or "patients" in result
    
    def test_with_prefix(self):
        """Should include prefix."""
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchone.return_value = (0,)
        
        result = generate_cohort_name(
            prefix="patientsim",
            entity_type="patient",
            include_date=False,
            connection=mock_conn
        )
        
        assert result.startswith("patientsim")
    
    def test_includes_date_by_default(self):
        """Should include date suffix by default."""
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchone.return_value = (0,)
        
        result = generate_cohort_name(
            keywords=["test"],
            connection=mock_conn
        )
        
        today = datetime.utcnow().strftime('%Y%m%d')
        assert today in result
    
    def test_fallback_to_cohort(self):
        """Should use 'cohort' if no keywords available."""
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchone.return_value = (0,)
        
        result = generate_cohort_name(
            include_date=False,
            connection=mock_conn
        )
        
        assert result == "cohort"


class TestParseCohortName:
    """Test cohort name parsing."""
    
    def test_parse_with_date(self):
        """Should parse name with date."""
        result = parse_cohort_name("diabetes-patients-20241226")
        
        assert result['keywords'] == ['diabetes', 'patients']
        assert result['date'] == '20241226'
        assert result['counter'] is None
    
    def test_parse_with_counter(self):
        """Should parse name with counter."""
        result = parse_cohort_name("diabetes-patients-20241226-2")
        
        assert result['keywords'] == ['diabetes', 'patients']
        assert result['date'] == '20241226'
        assert result['counter'] == 2
    
    def test_parse_without_date(self):
        """Should parse name without date."""
        result = parse_cohort_name("diabetes-patients")
        
        assert result['keywords'] == ['diabetes', 'patients']
        assert result['date'] is None
        assert result['counter'] is None
    
    def test_parse_single_keyword(self):
        """Should parse single keyword name."""
        result = parse_cohort_name("patients")
        
        assert result['keywords'] == ['patients']
        assert result['date'] is None
