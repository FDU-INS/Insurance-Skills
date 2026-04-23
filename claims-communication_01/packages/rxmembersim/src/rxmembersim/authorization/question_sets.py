"""Common ePA question sets for prior authorization."""

from ..formats.ncpdp.epa import QuestionType, ePAQuestion, ePAQuestionSet


class CommonQuestionSets:
    """Pre-built question sets for common PA scenarios."""

    @staticmethod
    def step_therapy_exception() -> ePAQuestionSet:
        """Questions for step therapy exception requests."""
        return ePAQuestionSet(
            question_set_id="STEP_THERAPY_01",
            drug_name="Step Therapy Exception",
            description="Questions for step therapy override requests",
            questions=[
                ePAQuestion(
                    question_id="ST001",
                    question_text="Has patient tried the prerequisite therapy?",
                    question_type=QuestionType.BOOLEAN,
                    required=True,
                ),
                ePAQuestion(
                    question_id="ST002",
                    question_text="Which prerequisite medication(s) were tried?",
                    question_type=QuestionType.MULTI_SELECT,
                    required=True,
                    options=[
                        "Metformin",
                        "Glipizide",
                        "Glimepiride",
                        "Glyburide",
                        "Other",
                    ],
                    depends_on_question="ST001",
                    depends_on_answer="true",
                ),
                ePAQuestion(
                    question_id="ST003",
                    question_text="Reason for discontinuation",
                    question_type=QuestionType.SINGLE_SELECT,
                    required=True,
                    options=[
                        "Inadequate response",
                        "Adverse reaction",
                        "Contraindication",
                        "Drug interaction",
                        "Patient intolerance",
                        "Other",
                    ],
                ),
                ePAQuestion(
                    question_id="ST004",
                    question_text="Duration of previous therapy (days)",
                    question_type=QuestionType.NUMERIC,
                    required=True,
                    min_value=0,
                    max_value=365,
                    unit="days",
                ),
                ePAQuestion(
                    question_id="ST005",
                    question_text="Please describe the adverse reaction or reason",
                    question_type=QuestionType.TEXT,
                    required=False,
                    depends_on_question="ST003",
                    depends_on_answer="Adverse reaction",
                ),
            ],
        )

    @staticmethod
    def specialty_medication() -> ePAQuestionSet:
        """Questions for specialty medication requests."""
        return ePAQuestionSet(
            question_set_id="SPECIALTY_01",
            drug_name="Specialty Medication",
            description="Questions for specialty pharmacy medications",
            questions=[
                ePAQuestion(
                    question_id="SP001",
                    question_text="Primary diagnosis for this medication?",
                    question_type=QuestionType.TEXT,
                    required=True,
                    help_text="Enter ICD-10 code or description",
                ),
                ePAQuestion(
                    question_id="SP002",
                    question_text="Is prescriber a specialist?",
                    question_type=QuestionType.BOOLEAN,
                    required=True,
                ),
                ePAQuestion(
                    question_id="SP003",
                    question_text="Prescriber specialty",
                    question_type=QuestionType.SINGLE_SELECT,
                    required=True,
                    options=[
                        "Rheumatology",
                        "Dermatology",
                        "Gastroenterology",
                        "Oncology",
                        "Neurology",
                        "Endocrinology",
                        "Other",
                    ],
                    depends_on_question="SP002",
                    depends_on_answer="true",
                ),
                ePAQuestion(
                    question_id="SP004",
                    question_text="Will patient use specialty pharmacy?",
                    question_type=QuestionType.BOOLEAN,
                    required=True,
                ),
                ePAQuestion(
                    question_id="SP005",
                    question_text="Has patient been educated on storage/administration?",
                    question_type=QuestionType.BOOLEAN,
                    required=True,
                ),
            ],
        )

    @staticmethod
    def quantity_override() -> ePAQuestionSet:
        """Questions for quantity limit override requests."""
        return ePAQuestionSet(
            question_set_id="QTY_OVERRIDE_01",
            drug_name="Quantity Override",
            description="Questions for quantity limit exception requests",
            questions=[
                ePAQuestion(
                    question_id="QO001",
                    question_text="Reason for quantity override",
                    question_type=QuestionType.SINGLE_SELECT,
                    required=True,
                    options=[
                        "Higher dose required",
                        "Multiple daily doses",
                        "Titration period",
                        "Vacation supply",
                        "Other",
                    ],
                ),
                ePAQuestion(
                    question_id="QO002",
                    question_text="Requested quantity per fill",
                    question_type=QuestionType.NUMERIC,
                    required=True,
                    min_value=1,
                    unit="units",
                ),
                ePAQuestion(
                    question_id="QO003",
                    question_text="Clinical justification",
                    question_type=QuestionType.TEXT,
                    required=True,
                    help_text="Provide clinical rationale for quantity override",
                ),
                ePAQuestion(
                    question_id="QO004",
                    question_text="Expected duration of increased quantity need",
                    question_type=QuestionType.SINGLE_SELECT,
                    required=True,
                    options=[
                        "30 days",
                        "90 days",
                        "6 months",
                        "1 year",
                        "Ongoing",
                    ],
                ),
            ],
        )

    @staticmethod
    def glp1_agonist() -> ePAQuestionSet:
        """Questions for GLP-1 agonist medications (Ozempic, Wegovy, etc.)."""
        return ePAQuestionSet(
            question_set_id="GLP1_01",
            drug_name="GLP-1 Agonist",
            description="Questions for GLP-1 receptor agonist authorization",
            questions=[
                ePAQuestion(
                    question_id="GLP1_001",
                    question_text="Primary indication",
                    question_type=QuestionType.SINGLE_SELECT,
                    required=True,
                    options=[
                        "Type 2 Diabetes",
                        "Weight Management",
                        "Both",
                    ],
                ),
                ePAQuestion(
                    question_id="GLP1_002",
                    question_text="Current HbA1c value (%)",
                    question_type=QuestionType.NUMERIC,
                    required=True,
                    min_value=4.0,
                    max_value=15.0,
                    unit="%",
                ),
                ePAQuestion(
                    question_id="GLP1_003",
                    question_text="Has patient tried metformin?",
                    question_type=QuestionType.BOOLEAN,
                    required=True,
                ),
                ePAQuestion(
                    question_id="GLP1_004",
                    question_text="Duration of metformin therapy",
                    question_type=QuestionType.NUMERIC,
                    required=True,
                    min_value=0,
                    max_value=365,
                    unit="days",
                    depends_on_question="GLP1_003",
                    depends_on_answer="true",
                ),
                ePAQuestion(
                    question_id="GLP1_005",
                    question_text="Current BMI",
                    question_type=QuestionType.NUMERIC,
                    required=True,
                    min_value=15,
                    max_value=80,
                    unit="kg/m²",
                ),
                ePAQuestion(
                    question_id="GLP1_006",
                    question_text="Has patient had bariatric surgery?",
                    question_type=QuestionType.BOOLEAN,
                    required=True,
                ),
            ],
        )

    @staticmethod
    def tnf_inhibitor() -> ePAQuestionSet:
        """Questions for TNF inhibitor medications (Humira, Enbrel, etc.)."""
        return ePAQuestionSet(
            question_set_id="TNF_01",
            drug_name="TNF Inhibitor",
            description="Questions for TNF-alpha inhibitor authorization",
            questions=[
                ePAQuestion(
                    question_id="TNF_001",
                    question_text="Primary diagnosis",
                    question_type=QuestionType.SINGLE_SELECT,
                    required=True,
                    options=[
                        "Rheumatoid Arthritis",
                        "Psoriatic Arthritis",
                        "Ankylosing Spondylitis",
                        "Plaque Psoriasis",
                        "Crohn's Disease",
                        "Ulcerative Colitis",
                        "Other",
                    ],
                ),
                ePAQuestion(
                    question_id="TNF_002",
                    question_text="Has patient tried methotrexate?",
                    question_type=QuestionType.BOOLEAN,
                    required=True,
                ),
                ePAQuestion(
                    question_id="TNF_003",
                    question_text="Duration of methotrexate therapy (days)",
                    question_type=QuestionType.NUMERIC,
                    required=True,
                    min_value=0,
                    max_value=365,
                    unit="days",
                    depends_on_question="TNF_002",
                    depends_on_answer="true",
                ),
                ePAQuestion(
                    question_id="TNF_004",
                    question_text="Has TB testing been performed?",
                    question_type=QuestionType.BOOLEAN,
                    required=True,
                ),
                ePAQuestion(
                    question_id="TNF_005",
                    question_text="TB test result",
                    question_type=QuestionType.SINGLE_SELECT,
                    required=True,
                    options=["Negative", "Positive - treated", "Positive - untreated"],
                    depends_on_question="TNF_004",
                    depends_on_answer="true",
                ),
                ePAQuestion(
                    question_id="TNF_006",
                    question_text="Prescriber specialty",
                    question_type=QuestionType.SINGLE_SELECT,
                    required=True,
                    options=[
                        "Rheumatology",
                        "Dermatology",
                        "Gastroenterology",
                        "Other",
                    ],
                ),
            ],
        )

    @staticmethod
    def controlled_substance() -> ePAQuestionSet:
        """Questions for controlled substance authorizations."""
        return ePAQuestionSet(
            question_set_id="CONTROLLED_01",
            drug_name="Controlled Substance",
            description="Questions for controlled substance authorization",
            questions=[
                ePAQuestion(
                    question_id="CS001",
                    question_text="Primary diagnosis requiring this medication",
                    question_type=QuestionType.TEXT,
                    required=True,
                ),
                ePAQuestion(
                    question_id="CS002",
                    question_text="Has patient tried non-controlled alternatives?",
                    question_type=QuestionType.BOOLEAN,
                    required=True,
                ),
                ePAQuestion(
                    question_id="CS003",
                    question_text="Which alternatives were tried?",
                    question_type=QuestionType.TEXT,
                    required=True,
                    depends_on_question="CS002",
                    depends_on_answer="true",
                ),
                ePAQuestion(
                    question_id="CS004",
                    question_text="Is patient enrolled in prescription monitoring program?",
                    question_type=QuestionType.BOOLEAN,
                    required=True,
                ),
                ePAQuestion(
                    question_id="CS005",
                    question_text="Has patient signed controlled substance agreement?",
                    question_type=QuestionType.BOOLEAN,
                    required=True,
                ),
            ],
        )
