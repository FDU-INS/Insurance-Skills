"""Tests for unified healthsim.generate() entry point."""

import pytest

import healthsim
from healthsim.generation import ExecutionResult


class TestListProducts:
    """Tests for list_products()."""

    def test_list_products(self):
        """Test listing available products."""
        products = healthsim.list_products()
        assert isinstance(products, list)
        assert "membersim" in products
        assert "patientsim" in products
        assert "rxmembersim" in products
        assert "trialsim" in products


class TestListTemplates:
    """Tests for list_templates()."""

    def test_list_member_templates(self):
        """Test listing member templates."""
        templates = healthsim.list_templates("members")
        assert isinstance(templates, list)
        assert len(templates) > 0
        assert "commercial-ppo-healthy" in templates

    def test_list_patient_templates(self):
        """Test listing patient templates."""
        templates = healthsim.list_templates("patients")
        assert len(templates) > 0
        assert "diabetic-senior" in templates

    def test_list_rx_templates(self):
        """Test listing rx templates."""
        templates = healthsim.list_templates("rx")
        assert len(templates) > 0

    def test_list_trial_templates(self):
        """Test listing trial templates."""
        templates = healthsim.list_templates("trials")
        assert len(templates) > 0
        assert "phase3-oncology-trial" in templates

    def test_list_templates_aliases(self):
        """Test that aliases work for list_templates."""
        t1 = healthsim.list_templates("members")
        t2 = healthsim.list_templates("membersim")
        t3 = healthsim.list_templates("member")
        assert t1 == t2 == t3


class TestQuickSample:
    """Tests for quick_sample()."""

    def test_quick_sample_members(self):
        """Test quick sample for members."""
        result = healthsim.quick_sample("members", 5)
        assert result.count == 5

    def test_quick_sample_patients(self):
        """Test quick sample for patients."""
        result = healthsim.quick_sample("patients", 5)
        # PatientSim returns list directly
        assert len(result) == 5

    def test_quick_sample_rx(self):
        """Test quick sample for rx members."""
        result = healthsim.quick_sample("rx", 5)
        # RxMemberSim returns list directly
        assert len(result) == 5

    def test_quick_sample_trials(self):
        """Test quick sample for trials."""
        result = healthsim.quick_sample("trials", 5)
        assert result.count == 5

    def test_quick_sample_aliases(self):
        """Test that product aliases work."""
        r1 = healthsim.quick_sample("member", 3)
        r2 = healthsim.quick_sample("members", 3)
        r3 = healthsim.quick_sample("membersim", 3)
        assert r1.count == r2.count == r3.count == 3


class TestGenerate:
    """Tests for generate()."""

    def test_generate_members_with_template(self):
        """Test generating members with template."""
        result = healthsim.generate("members", template="commercial-ppo-healthy", count=10, seed=42)
        assert result.count == 10

    def test_generate_patients_with_template(self):
        """Test generating patients with template."""
        result = healthsim.generate("patients", template="diabetic-senior", count=10, seed=42)
        assert result.count == 10

    def test_generate_rx_with_template(self):
        """Test generating rx members with template."""
        result = healthsim.generate("rx", template="commercial-chronic", count=10, seed=42)
        assert result.count == 10

    def test_generate_trials_with_template(self):
        """Test generating trial subjects with template."""
        result = healthsim.generate("trials", template="phase3-oncology-trial", count=10, seed=42)
        assert result.count == 10

    def test_generate_reproducible(self):
        """Test that same seed produces same results."""
        r1 = healthsim.generate("members", template="commercial-ppo-healthy", count=5, seed=42)
        r2 = healthsim.generate("members", template="commercial-ppo-healthy", count=5, seed=42)
        
        assert r1.count == r2.count
        # Check first member has same attributes
        assert r1.members[0].member_id == r2.members[0].member_id

    def test_generate_invalid_product(self):
        """Test error for invalid product."""
        with pytest.raises(ValueError, match="Unknown product"):
            healthsim.generate("invalid-product", count=10)

    def test_generate_invalid_template(self):
        """Test error for invalid template."""
        with pytest.raises(KeyError):
            healthsim.generate("members", template="nonexistent-template", count=10)


class TestGenerateWithJourney:
    """Tests for generate() with journey parameter."""

    def test_generate_with_journey(self):
        """Test generating with journey."""
        from healthsim.generation import OrchestratorResult
        
        result = healthsim.generate(
            "patients",
            template="diabetic-senior",
            journey="diabetic-first-year",
            count=5,
            seed=42,
        )
        
        # When journey is provided, returns OrchestratorResult
        assert isinstance(result, OrchestratorResult)
        assert result.entity_count == 5
        assert result.event_count > 0
