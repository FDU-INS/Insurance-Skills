"""Tests for ePA (Electronic Prior Authorization) transactions."""

from rxmembersim.authorization.question_sets import CommonQuestionSets
from rxmembersim.formats.ncpdp.epa import (
    QuestionType,
    ePAAnswer,
    ePAGenerator,
    ePAMessageType,
    ePAQuestion,
    ePAQuestionSet,
)


class TestEPAGenerator:
    """Tests for ePAGenerator."""

    def test_generate_initiation_request(self) -> None:
        """Test generating PA initiation request."""
        generator = ePAGenerator()
        request = generator.generate_initiation_request(
            member_id="MEM001",
            patient_first="John",
            patient_last="Doe",
            patient_dob="1980-01-15",
            patient_gender="M",
            prescriber_npi="1234567890",
            prescriber_name="Dr. Smith",
            drug_description="Ozempic 1mg/dose",
            ndc="00169413512",
            quantity="1",
            days_supply=28,
        )

        assert request.message_id.startswith("MSG")
        assert request.member_id == "MEM001"
        assert request.patient_first_name == "John"
        assert request.patient_last_name == "Doe"
        assert request.drug_description == "Ozempic 1mg/dose"
        assert request.ndc == "00169413512"
        assert request.days_supply == 28
        assert request.message_type == ePAMessageType.PA_INITIATION_REQUEST

    def test_generate_initiation_with_diagnosis(self) -> None:
        """Test generating PA initiation with diagnosis codes."""
        generator = ePAGenerator()
        request = generator.generate_initiation_request(
            member_id="MEM001",
            patient_first="John",
            patient_last="Doe",
            patient_dob="1980-01-15",
            patient_gender="M",
            prescriber_npi="1234567890",
            prescriber_name="Dr. Smith",
            drug_description="Ozempic",
            ndc="00169413512",
            quantity="1",
            days_supply=28,
            diagnosis_codes=["E11.9", "E66.01"],
            urgency="urgent",
        )

        assert len(request.diagnosis_codes) == 2
        assert "E11.9" in request.diagnosis_codes
        assert request.urgency_indicator == "urgent"

    def test_generate_question_response(self) -> None:
        """Test generating response with questions."""
        generator = ePAGenerator()
        request = generator.generate_initiation_request(
            member_id="MEM001",
            patient_first="John",
            patient_last="Doe",
            patient_dob="1980-01-15",
            patient_gender="M",
            prescriber_npi="1234567890",
            prescriber_name="Dr. Smith",
            drug_description="Ozempic",
            ndc="00169413512",
            quantity="1",
            days_supply=28,
        )

        questions = ePAQuestionSet(
            question_set_id="TEST01",
            drug_name="Test Drug",
            questions=[
                ePAQuestion(
                    question_id="Q1",
                    question_text="Has patient tried metformin?",
                    question_type=QuestionType.BOOLEAN,
                )
            ],
        )

        response = generator.generate_question_response(request, questions)

        assert response.relates_to_message_id == request.message_id
        assert response.response_type == "Question"
        assert response.question_set is not None
        assert response.question_set.question_set_id == "TEST01"
        assert response.message_type == ePAMessageType.PA_INITIATION_RESPONSE

    def test_generate_approval_response(self) -> None:
        """Test generating approval response."""
        generator = ePAGenerator()

        response = generator.generate_approval_response(
            request_message_id="MSG1234567890",
            pa_number="AUTH123456789",
            quantity_approved="1",
            days_supply_approved=28,
            refills_approved=12,
        )

        assert response.relates_to_message_id == "MSG1234567890"
        assert response.determination == "Approved"
        assert response.pa_number == "AUTH123456789"
        assert response.quantity_approved == "1"
        assert response.days_supply_approved == 28
        assert response.refills_approved == 12
        assert response.effective_date is not None
        assert response.expiration_date is not None
        assert response.message_type == ePAMessageType.PA_RESPONSE

    def test_generate_denial_response(self) -> None:
        """Test generating denial response."""
        generator = ePAGenerator()

        response = generator.generate_denial_response(
            request_message_id="MSG1234567890",
            denial_reason="Step therapy requirement not met",
            denial_code="75",
            alternatives=["Metformin 500mg", "Glipizide 5mg"],
        )

        assert response.relates_to_message_id == "MSG1234567890"
        assert response.determination == "Denied"
        assert response.denial_reason == "Step therapy requirement not met"
        assert response.denial_code == "75"
        assert len(response.suggested_alternatives) == 2
        assert response.appeal_deadline is not None
        assert response.appeal_process is not None

    def test_generate_more_info_response(self) -> None:
        """Test generating more info needed response."""
        generator = ePAGenerator()

        questions = ePAQuestionSet(
            question_set_id="ADDL01",
            drug_name="Additional Info",
            questions=[
                ePAQuestion(
                    question_id="A1",
                    question_text="Please provide HbA1c value",
                    question_type=QuestionType.NUMERIC,
                )
            ],
        )

        response = generator.generate_more_info_response(
            request_message_id="MSG1234567890",
            questions=questions,
            requested_documents=["Lab results", "Clinical notes"],
        )

        assert response.determination == "MoreInfoNeeded"
        assert response.additional_questions is not None
        assert len(response.requested_documents) == 2

    def test_generate_pa_request(self) -> None:
        """Test generating PA request with answers."""
        generator = ePAGenerator()

        answers = [
            ePAAnswer(
                question_id="Q1",
                answer_type=QuestionType.BOOLEAN,
                boolean_answer=True,
            ),
            ePAAnswer(
                question_id="Q2",
                answer_type=QuestionType.TEXT,
                text_answer="Patient intolerant to metformin",
            ),
        ]

        request = generator.generate_pa_request(
            relates_to="MSG1234567890",
            pa_reference="REF12345678",
            answers=answers,
            clinical_notes="Patient has documented GI intolerance to metformin",
        )

        assert request.relates_to_message_id == "MSG1234567890"
        assert request.pa_reference_number == "REF12345678"
        assert len(request.answers) == 2
        assert request.clinical_notes is not None
        assert request.message_type == ePAMessageType.PA_REQUEST


class TestEPAXMLGeneration:
    """Tests for XML generation."""

    def test_initiation_request_to_xml(self) -> None:
        """Test converting initiation request to XML."""
        generator = ePAGenerator()
        request = generator.generate_initiation_request(
            member_id="MEM001",
            patient_first="John",
            patient_last="Doe",
            patient_dob="1980-01-15",
            patient_gender="M",
            prescriber_npi="1234567890",
            prescriber_name="Dr. Smith",
            drug_description="Ozempic",
            ndc="00169413512",
            quantity="1",
            days_supply=28,
        )

        xml = generator.to_xml(request)

        assert "<Message" in xml
        assert "xmlns" in xml
        assert "<MessageID>" in xml
        assert "<PAInitiationRequest>" in xml
        assert "MEM001" in xml
        assert "John" in xml

    def test_response_to_xml(self) -> None:
        """Test converting response to XML."""
        generator = ePAGenerator()

        response = generator.generate_approval_response(
            request_message_id="MSG1234567890",
            pa_number="AUTH123456789",
        )

        xml = generator.to_xml(response)

        assert "<Message" in xml
        assert "<PAResponse>" in xml
        assert "AUTH123456789" in xml
        assert "Approved" in xml


class TestEPAQuestionModels:
    """Tests for ePA question models."""

    def test_question_with_options(self) -> None:
        """Test creating question with options."""
        question = ePAQuestion(
            question_id="Q1",
            question_text="Select reason",
            question_type=QuestionType.SINGLE_SELECT,
            options=["Option A", "Option B", "Option C"],
        )

        assert question.question_type == QuestionType.SINGLE_SELECT
        assert len(question.options) == 3

    def test_question_with_constraints(self) -> None:
        """Test creating question with numeric constraints."""
        question = ePAQuestion(
            question_id="Q1",
            question_text="Enter HbA1c value",
            question_type=QuestionType.NUMERIC,
            min_value=4.0,
            max_value=15.0,
            unit="%",
        )

        assert question.min_value == 4.0
        assert question.max_value == 15.0
        assert question.unit == "%"

    def test_question_with_dependency(self) -> None:
        """Test creating question with conditional display."""
        question = ePAQuestion(
            question_id="Q2",
            question_text="Which medication?",
            question_type=QuestionType.TEXT,
            depends_on_question="Q1",
            depends_on_answer="true",
        )

        assert question.depends_on_question == "Q1"
        assert question.depends_on_answer == "true"

    def test_question_set(self) -> None:
        """Test creating question set."""
        qs = ePAQuestionSet(
            question_set_id="TEST01",
            drug_name="Test Drug",
            description="Test questions",
            questions=[
                ePAQuestion(
                    question_id="Q1",
                    question_text="Question 1?",
                    question_type=QuestionType.BOOLEAN,
                ),
                ePAQuestion(
                    question_id="Q2",
                    question_text="Question 2?",
                    question_type=QuestionType.TEXT,
                ),
            ],
        )

        assert qs.question_set_id == "TEST01"
        assert len(qs.questions) == 2


class TestEPAAnswerModels:
    """Tests for ePA answer models."""

    def test_boolean_answer(self) -> None:
        """Test boolean answer."""
        answer = ePAAnswer(
            question_id="Q1",
            answer_type=QuestionType.BOOLEAN,
            boolean_answer=True,
        )

        assert answer.boolean_answer is True

    def test_text_answer(self) -> None:
        """Test text answer."""
        answer = ePAAnswer(
            question_id="Q1",
            answer_type=QuestionType.TEXT,
            text_answer="Patient has documented intolerance",
        )

        assert answer.text_answer == "Patient has documented intolerance"

    def test_numeric_answer(self) -> None:
        """Test numeric answer."""
        answer = ePAAnswer(
            question_id="Q1",
            answer_type=QuestionType.NUMERIC,
            numeric_answer=8.5,
        )

        assert answer.numeric_answer == 8.5

    def test_single_select_answer(self) -> None:
        """Test single select answer."""
        answer = ePAAnswer(
            question_id="Q1",
            answer_type=QuestionType.SINGLE_SELECT,
            selected_options=["Option A"],
        )

        assert len(answer.selected_options) == 1
        assert answer.selected_options[0] == "Option A"

    def test_multi_select_answer(self) -> None:
        """Test multi select answer."""
        answer = ePAAnswer(
            question_id="Q1",
            answer_type=QuestionType.MULTI_SELECT,
            selected_options=["Option A", "Option B"],
        )

        assert len(answer.selected_options) == 2


class TestEPAWithCommonQuestionSets:
    """Tests for ePA with common question sets."""

    def test_glp1_workflow(self) -> None:
        """Test full ePA workflow for GLP-1."""
        generator = ePAGenerator()

        # 1. Create initiation request
        init_request = generator.generate_initiation_request(
            member_id="MEM001",
            patient_first="John",
            patient_last="Doe",
            patient_dob="1970-01-15",
            patient_gender="M",
            prescriber_npi="1234567890",
            prescriber_name="Dr. Smith",
            drug_description="Ozempic 0.5mg",
            ndc="00169413512",
            quantity="1",
            days_supply=28,
            diagnosis_codes=["E11.9"],
        )

        # 2. Generate question response
        questions = CommonQuestionSets.glp1_agonist()
        question_response = generator.generate_question_response(
            init_request, questions
        )

        assert question_response.response_type == "Question"
        assert question_response.question_set is not None

        # 3. Create PA request with answers
        answers = [
            ePAAnswer(
                question_id="GLP1_001",
                answer_type=QuestionType.SINGLE_SELECT,
                selected_options=["Type 2 Diabetes"],
            ),
            ePAAnswer(
                question_id="GLP1_002",
                answer_type=QuestionType.NUMERIC,
                numeric_answer=8.5,
            ),
            ePAAnswer(
                question_id="GLP1_003",
                answer_type=QuestionType.BOOLEAN,
                boolean_answer=True,
            ),
            ePAAnswer(
                question_id="GLP1_004",
                answer_type=QuestionType.NUMERIC,
                numeric_answer=120,
            ),
            ePAAnswer(
                question_id="GLP1_005",
                answer_type=QuestionType.NUMERIC,
                numeric_answer=32.5,
            ),
            ePAAnswer(
                question_id="GLP1_006",
                answer_type=QuestionType.BOOLEAN,
                boolean_answer=False,
            ),
        ]

        pa_request = generator.generate_pa_request(
            relates_to=question_response.message_id,
            pa_reference=question_response.pa_reference_number or "REF12345678",
            answers=answers,
        )

        assert len(pa_request.answers) == 6

        # 4. Generate approval
        approval = generator.generate_approval_response(
            request_message_id=pa_request.message_id,
            pa_number="AUTH987654321",
            quantity_approved="1",
            days_supply_approved=28,
        )

        assert approval.determination == "Approved"
        assert approval.pa_number == "AUTH987654321"

    def test_step_therapy_workflow(self) -> None:
        """Test ePA workflow for step therapy exception."""
        generator = ePAGenerator()

        # Create initiation
        init_request = generator.generate_initiation_request(
            member_id="MEM002",
            patient_first="Jane",
            patient_last="Smith",
            patient_dob="1985-06-20",
            patient_gender="F",
            prescriber_npi="9876543210",
            prescriber_name="Dr. Jones",
            drug_description="Jardiance 10mg",
            ndc="00002323201",
            quantity="30",
            days_supply=30,
        )

        # Get step therapy questions
        questions = CommonQuestionSets.step_therapy_exception()
        question_response = generator.generate_question_response(
            init_request, questions
        )

        assert question_response.question_set.question_set_id == "STEP_THERAPY_01"
        assert len(question_response.question_set.questions) >= 4
