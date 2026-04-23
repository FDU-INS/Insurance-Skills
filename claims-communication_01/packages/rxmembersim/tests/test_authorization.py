"""Tests for prior authorization module."""

from datetime import date
from decimal import Decimal

from rxmembersim.authorization.criteria import (
    ClinicalCriteriaLibrary,
    ClinicalCriteriaSet,
    ClinicalCriterion,
    CriterionType,
)
from rxmembersim.authorization.prior_auth import (
    PADenialReason,
    PARequestType,
    PAStatus,
    PriorAuthWorkflow,
)
from rxmembersim.authorization.question_sets import CommonQuestionSets


class TestPriorAuthWorkflow:
    """Tests for PriorAuthWorkflow."""

    def test_create_request(self) -> None:
        """Test creating a PA request."""
        workflow = PriorAuthWorkflow()
        request = workflow.create_request(
            member_id="MEM001",
            cardholder_id="CARD001",
            ndc="00169413512",
            drug_name="Ozempic 0.5mg",
            quantity=Decimal("1"),
            days_supply=28,
            prescriber_npi="1234567890",
            prescriber_name="Dr. Smith",
            diagnosis_codes=["E11.9"],
        )

        assert request.pa_request_id.startswith("PA-")
        assert request.member_id == "MEM001"
        assert request.drug_name == "Ozempic 0.5mg"
        assert request.quantity_requested == Decimal("1")

    def test_approve_request(self) -> None:
        """Test approving a PA request."""
        workflow = PriorAuthWorkflow()
        request = workflow.create_request(
            member_id="MEM001",
            cardholder_id="CARD001",
            ndc="00169413512",
            drug_name="Ozempic 0.5mg",
            quantity=Decimal("1"),
            days_supply=28,
            prescriber_npi="1234567890",
            prescriber_name="Dr. Smith",
        )

        response = workflow.approve(request)

        assert response.status == PAStatus.APPROVED
        assert response.pa_number is not None
        assert response.pa_number.startswith("AUTH")
        assert response.effective_date == date.today()
        assert response.quantity_approved == Decimal("1")
        assert response.refills_approved == 12

    def test_deny_request(self) -> None:
        """Test denying a PA request."""
        workflow = PriorAuthWorkflow()
        request = workflow.create_request(
            member_id="MEM001",
            cardholder_id="CARD001",
            ndc="00169413512",
            drug_name="Ozempic 0.5mg",
            quantity=Decimal("1"),
            days_supply=28,
            prescriber_npi="1234567890",
            prescriber_name="Dr. Smith",
        )

        response = workflow.deny(
            request,
            PADenialReason.STEP_THERAPY_REQUIRED,
            message="Metformin trial required first",
            alternatives=["Metformin 500mg", "Glipizide 5mg"],
        )

        assert response.status == PAStatus.DENIED
        assert response.denial_reason == PADenialReason.STEP_THERAPY_REQUIRED
        assert "Metformin" in response.denial_message
        assert len(response.suggested_alternatives) == 2
        assert response.appeal_deadline is not None

    def test_partial_approve(self) -> None:
        """Test partial approval with modified terms."""
        workflow = PriorAuthWorkflow()
        request = workflow.create_request(
            member_id="MEM001",
            cardholder_id="CARD001",
            ndc="00169413512",
            drug_name="Ozempic 0.5mg",
            quantity=Decimal("4"),
            days_supply=90,
            prescriber_npi="1234567890",
            prescriber_name="Dr. Smith",
        )

        response = workflow.partial_approve(
            request,
            quantity=Decimal("1"),
            days_supply=28,
            duration_days=90,
            reason="Approved for 28-day supply only",
        )

        assert response.status == PAStatus.PARTIAL
        assert response.quantity_approved == Decimal("1")
        assert response.days_supply_approved == 28

    def test_auto_approval_emergency(self) -> None:
        """Test auto-approval for emergency requests."""
        workflow = PriorAuthWorkflow()
        request = workflow.create_request(
            member_id="MEM001",
            cardholder_id="CARD001",
            ndc="00169413512",
            drug_name="Ozempic 0.5mg",
            quantity=Decimal("1"),
            days_supply=28,
            prescriber_npi="1234567890",
            prescriber_name="Dr. Smith",
            urgency="emergency",
        )

        response = workflow.check_auto_approval(request)

        assert response is not None
        assert response.status == PAStatus.APPROVED
        assert response.auto_approved is True

    def test_auto_approval_renewal(self) -> None:
        """Test auto-approval for renewal requests."""
        workflow = PriorAuthWorkflow()
        request = workflow.create_request(
            member_id="MEM001",
            cardholder_id="CARD001",
            ndc="00169413512",
            drug_name="Ozempic 0.5mg",
            quantity=Decimal("1"),
            days_supply=28,
            prescriber_npi="1234567890",
            prescriber_name="Dr. Smith",
        )
        request.request_type = PARequestType.RENEWAL

        response = workflow.check_auto_approval(request)

        assert response is not None
        assert response.status == PAStatus.APPROVED

    def test_no_auto_approval_routine(self) -> None:
        """Test no auto-approval for routine requests."""
        workflow = PriorAuthWorkflow()
        request = workflow.create_request(
            member_id="MEM001",
            cardholder_id="CARD001",
            ndc="00169413512",
            drug_name="Ozempic 0.5mg",
            quantity=Decimal("1"),
            days_supply=28,
            prescriber_npi="1234567890",
            prescriber_name="Dr. Smith",
            urgency="routine",
        )

        response = workflow.check_auto_approval(request)

        assert response is None

    def test_check_existing_auth(self) -> None:
        """Test checking for existing authorization."""
        workflow = PriorAuthWorkflow()

        # Create and approve a request
        request = workflow.create_request(
            member_id="MEM001",
            cardholder_id="CARD001",
            ndc="00169413512",
            drug_name="Ozempic 0.5mg",
            quantity=Decimal("1"),
            days_supply=28,
            prescriber_npi="1234567890",
            prescriber_name="Dr. Smith",
        )
        workflow.approve(request)

        # Check for existing auth
        existing = workflow.check_existing_auth("MEM001", "00169413512")

        assert existing is not None
        assert existing.status == PAStatus.APPROVED

    def test_no_existing_auth(self) -> None:
        """Test no existing authorization found."""
        workflow = PriorAuthWorkflow()

        existing = workflow.check_existing_auth("MEM999", "99999999999")

        assert existing is None


class TestClinicalCriteria:
    """Tests for clinical criteria evaluation."""

    def test_evaluate_diagnosis_met(self) -> None:
        """Test diagnosis criterion met."""
        criteria_set = ClinicalCriteriaSet(
            criteria_set_id="TEST-001",
            drug_gpi="27200060",
            drug_name="GLP-1 Agonist",
            criteria=[
                ClinicalCriterion(
                    criterion_id="DX-001",
                    criterion_type=CriterionType.DIAGNOSIS,
                    description="Type 2 Diabetes required",
                    diagnosis_codes=["E11"],
                )
            ],
        )

        result = criteria_set.evaluate(
            diagnosis_codes=["E11.9"],
            previous_therapies=[],
        )

        assert result.met is True
        assert len(result.unmet_criteria) == 0

    def test_evaluate_diagnosis_not_met(self) -> None:
        """Test diagnosis criterion not met."""
        criteria_set = ClinicalCriteriaSet(
            criteria_set_id="TEST-001",
            drug_gpi="27200060",
            drug_name="GLP-1 Agonist",
            criteria=[
                ClinicalCriterion(
                    criterion_id="DX-001",
                    criterion_type=CriterionType.DIAGNOSIS,
                    description="Type 2 Diabetes required",
                    diagnosis_codes=["E11"],
                )
            ],
        )

        result = criteria_set.evaluate(
            diagnosis_codes=["J44.9"],  # COPD, not diabetes
            previous_therapies=[],
        )

        assert result.met is False
        assert len(result.unmet_criteria) == 1
        assert "Type 2 Diabetes" in result.unmet_criteria[0]

    def test_evaluate_previous_therapy(self) -> None:
        """Test previous therapy criterion."""
        criteria_set = ClinicalCriteriaSet(
            criteria_set_id="TEST-001",
            drug_gpi="27200060",
            drug_name="GLP-1 Agonist",
            criteria=[
                ClinicalCriterion(
                    criterion_id="STEP-001",
                    criterion_type=CriterionType.PREVIOUS_THERAPY,
                    description="Metformin trial required",
                    required_therapies=["metformin", "2710003"],
                )
            ],
        )

        # Met
        result = criteria_set.evaluate(
            diagnosis_codes=[],
            previous_therapies=["metformin"],
        )
        assert result.met is True

        # Not met
        result = criteria_set.evaluate(
            diagnosis_codes=[],
            previous_therapies=["glipizide"],
        )
        assert result.met is False

    def test_evaluate_age_restriction(self) -> None:
        """Test age restriction criterion."""
        criteria_set = ClinicalCriteriaSet(
            criteria_set_id="TEST-001",
            drug_gpi="65100020",
            drug_name="CNS Stimulant",
            criteria=[
                ClinicalCriterion(
                    criterion_id="AGE-001",
                    criterion_type=CriterionType.AGE,
                    description="Age 6-65 required",
                    min_age=6,
                    max_age=65,
                )
            ],
        )

        # Within range
        result = criteria_set.evaluate(
            diagnosis_codes=[],
            previous_therapies=[],
            member_age=25,
        )
        assert result.met is True

        # Too young
        result = criteria_set.evaluate(
            diagnosis_codes=[],
            previous_therapies=[],
            member_age=4,
        )
        assert result.met is False

        # Too old
        result = criteria_set.evaluate(
            diagnosis_codes=[],
            previous_therapies=[],
            member_age=70,
        )
        assert result.met is False

    def test_evaluate_specialist(self) -> None:
        """Test specialist requirement criterion."""
        criteria_set = ClinicalCriteriaSet(
            criteria_set_id="TEST-001",
            drug_gpi="66400020",
            drug_name="TNF Inhibitor",
            criteria=[
                ClinicalCriterion(
                    criterion_id="SPEC-001",
                    criterion_type=CriterionType.SPECIALIST,
                    description="Specialist required",
                    specialist_types=["rheumatology", "dermatology"],
                )
            ],
        )

        # Specialist match
        result = criteria_set.evaluate(
            diagnosis_codes=[],
            previous_therapies=[],
            prescriber_specialty="rheumatology",
        )
        assert result.met is True

        # No specialist
        result = criteria_set.evaluate(
            diagnosis_codes=[],
            previous_therapies=[],
            prescriber_specialty="family_medicine",
        )
        assert result.met is False

    def test_evaluate_lab_result(self) -> None:
        """Test lab result criterion."""
        criteria_set = ClinicalCriteriaSet(
            criteria_set_id="TEST-001",
            drug_gpi="27200060",
            drug_name="GLP-1 Agonist",
            criteria=[
                ClinicalCriterion(
                    criterion_id="LAB-001",
                    criterion_type=CriterionType.LAB_RESULT,
                    description="HbA1c >= 7.0%",
                    lab_test="HbA1c",
                    lab_min_value=7.0,
                )
            ],
        )

        # Lab meets criteria
        result = criteria_set.evaluate(
            diagnosis_codes=[],
            previous_therapies=[],
            lab_results={"HbA1c": 8.5},
        )
        assert result.met is True

        # Lab below criteria
        result = criteria_set.evaluate(
            diagnosis_codes=[],
            previous_therapies=[],
            lab_results={"HbA1c": 6.5},
        )
        assert result.met is False

    def test_evaluate_multiple_criteria(self) -> None:
        """Test evaluating multiple criteria."""
        criteria = ClinicalCriteriaLibrary.glp1_criteria()

        # All met
        result = criteria.evaluate(
            diagnosis_codes=["E11.9"],
            previous_therapies=["metformin"],
            lab_results={"HbA1c": 8.0},
        )
        assert result.met is True
        assert result.criteria_met >= 2

        # Diagnosis not met
        result = criteria.evaluate(
            diagnosis_codes=["J44.9"],
            previous_therapies=["metformin"],
        )
        assert result.met is False


class TestClinicalCriteriaLibrary:
    """Tests for pre-built criteria sets."""

    def test_glp1_criteria(self) -> None:
        """Test GLP-1 criteria set."""
        criteria = ClinicalCriteriaLibrary.glp1_criteria()

        assert criteria.criteria_set_id == "GLP1-PA-001"
        assert len(criteria.criteria) >= 2

    def test_tnf_inhibitor_criteria(self) -> None:
        """Test TNF inhibitor criteria set."""
        criteria = ClinicalCriteriaLibrary.tnf_inhibitor_criteria()

        assert criteria.criteria_set_id == "TNF-PA-001"
        assert len(criteria.criteria) >= 3

    def test_stimulant_criteria(self) -> None:
        """Test stimulant criteria set."""
        criteria = ClinicalCriteriaLibrary.stimulant_criteria()

        assert criteria.criteria_set_id == "STIM-PA-001"
        assert len(criteria.criteria) >= 3


class TestQuestionSets:
    """Tests for common question sets."""

    def test_step_therapy_questions(self) -> None:
        """Test step therapy exception questions."""
        qs = CommonQuestionSets.step_therapy_exception()

        assert qs.question_set_id == "STEP_THERAPY_01"
        assert len(qs.questions) >= 4

        # Check for required questions
        question_ids = [q.question_id for q in qs.questions]
        assert "ST001" in question_ids
        assert "ST003" in question_ids

    def test_specialty_medication_questions(self) -> None:
        """Test specialty medication questions."""
        qs = CommonQuestionSets.specialty_medication()

        assert qs.question_set_id == "SPECIALTY_01"
        assert len(qs.questions) >= 4

    def test_quantity_override_questions(self) -> None:
        """Test quantity override questions."""
        qs = CommonQuestionSets.quantity_override()

        assert qs.question_set_id == "QTY_OVERRIDE_01"
        assert len(qs.questions) >= 3

    def test_glp1_questions(self) -> None:
        """Test GLP-1 specific questions."""
        qs = CommonQuestionSets.glp1_agonist()

        assert qs.question_set_id == "GLP1_01"
        assert len(qs.questions) >= 5

        # Check for HbA1c question
        hba1c_questions = [q for q in qs.questions if "HbA1c" in q.question_text]
        assert len(hba1c_questions) > 0

    def test_tnf_inhibitor_questions(self) -> None:
        """Test TNF inhibitor questions."""
        qs = CommonQuestionSets.tnf_inhibitor()

        assert qs.question_set_id == "TNF_01"
        assert len(qs.questions) >= 5

        # Check for TB question
        tb_questions = [q for q in qs.questions if "TB" in q.question_text]
        assert len(tb_questions) > 0

    def test_controlled_substance_questions(self) -> None:
        """Test controlled substance questions."""
        qs = CommonQuestionSets.controlled_substance()

        assert qs.question_set_id == "CONTROLLED_01"
        assert len(qs.questions) >= 4

    def test_conditional_questions(self) -> None:
        """Test conditional question dependencies."""
        qs = CommonQuestionSets.step_therapy_exception()

        # Find question with dependency
        dependent_questions = [
            q for q in qs.questions if q.depends_on_question is not None
        ]
        assert len(dependent_questions) > 0

        # Verify dependency is valid
        for q in dependent_questions:
            parent_ids = [p.question_id for p in qs.questions]
            assert q.depends_on_question in parent_ids
