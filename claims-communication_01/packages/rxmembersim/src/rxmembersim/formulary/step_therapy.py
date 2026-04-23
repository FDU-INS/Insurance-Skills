"""Step therapy management."""
from datetime import date, timedelta

from pydantic import BaseModel, Field


class StepTherapyStep(BaseModel):
    """Single step in step therapy protocol."""

    step_number: int
    step_name: str
    required_drugs: list[str]  # NDCs or GPI prefixes
    minimum_days: int = 30
    minimum_fills: int = 1
    description: str | None = None


class StepTherapyProtocol(BaseModel):
    """Step therapy protocol definition."""

    protocol_id: str
    protocol_name: str
    description: str | None = None

    # Target drugs that require this step therapy
    target_drugs: list[str]  # NDCs or GPI prefixes

    # Steps required before target drug
    steps: list[StepTherapyStep]

    # Lookback period for checking history
    lookback_days: int = 365

    def check_satisfied(
        self,
        target_ndc: str,
        claim_history: list,
        service_date: date,
    ) -> "StepTherapyResult":
        """
        Check if step therapy requirements are satisfied.

        Args:
            target_ndc: NDC of the target drug
            claim_history: List of previous claims with ndc, service_date, days_supply
            service_date: Date of the claim being checked

        Returns:
            StepTherapyResult with satisfied status and details
        """
        # Filter history to lookback period
        lookback_start = service_date - timedelta(days=self.lookback_days)
        relevant_history = [
            c
            for c in claim_history
            if hasattr(c, "service_date") and c.service_date >= lookback_start
        ]

        completed_steps: list[int] = []
        failed_step: int | None = None
        required_drugs: list[str] = []

        for step in sorted(self.steps, key=lambda s: s.step_number):
            step_satisfied = False

            for req_drug in step.required_drugs:
                # Check for fills matching the required drug
                fills = [
                    c
                    for c in relevant_history
                    if hasattr(c, "ndc")
                    and (c.ndc == req_drug or c.ndc.startswith(req_drug))
                ]

                if not fills:
                    # Also check GPI if available
                    fills = [
                        c
                        for c in relevant_history
                        if hasattr(c, "gpi")
                        and (c.gpi == req_drug or c.gpi.startswith(req_drug))
                    ]

                if fills:
                    total_days = sum(
                        getattr(c, "days_supply", 0) for c in fills
                    )
                    if (
                        total_days >= step.minimum_days
                        and len(fills) >= step.minimum_fills
                    ):
                        step_satisfied = True
                        break

            if step_satisfied:
                completed_steps.append(step.step_number)
            else:
                failed_step = step.step_number
                required_drugs = step.required_drugs
                break

        all_satisfied = len(completed_steps) == len(self.steps)

        return StepTherapyResult(
            protocol_id=self.protocol_id,
            target_ndc=target_ndc,
            satisfied=all_satisfied,
            completed_steps=completed_steps,
            failed_step=failed_step,
            required_drugs=required_drugs,
            message=self._build_message(all_satisfied, failed_step, required_drugs),
        )

    def _build_message(
        self,
        satisfied: bool,
        failed_step: int | None,
        required_drugs: list[str],
    ) -> str:
        """Build result message."""
        if satisfied:
            return "Step therapy requirements satisfied"

        step_info = next(
            (s for s in self.steps if s.step_number == failed_step), None
        )
        if step_info:
            return (
                f"Step therapy not satisfied: {step_info.step_name} required. "
                f"Try one of: {', '.join(required_drugs)}"
            )
        return "Step therapy not satisfied"


class StepTherapyResult(BaseModel):
    """Result of step therapy check."""

    protocol_id: str
    target_ndc: str
    satisfied: bool

    completed_steps: list[int] = Field(default_factory=list)
    failed_step: int | None = None
    required_drugs: list[str] = Field(default_factory=list)

    message: str


class StepTherapyManager:
    """Manage step therapy protocols."""

    def __init__(self) -> None:
        self.protocols: dict[str, StepTherapyProtocol] = {}
        self._load_default_protocols()

    def _load_default_protocols(self) -> None:
        """Load common step therapy protocols."""
        # PPI Step Therapy
        self.add_protocol(
            StepTherapyProtocol(
                protocol_id="PPI-ST",
                protocol_name="PPI Step Therapy",
                description="Generic PPI required before brand PPI",
                target_drugs=[
                    "00186077831",  # Nexium
                    "00300606331",  # Prevacid
                    "64764081530",  # Protonix
                ],
                steps=[
                    StepTherapyStep(
                        step_number=1,
                        step_name="Generic PPI",
                        required_drugs=[
                            "4940001",  # Omeprazole GPI prefix
                            "4940002",  # Lansoprazole GPI prefix
                            "4940004",  # Pantoprazole GPI prefix
                        ],
                        minimum_days=30,
                        minimum_fills=1,
                        description="Must try generic PPI for 30 days",
                    )
                ],
            )
        )

        # TNF Inhibitor Step Therapy
        self.add_protocol(
            StepTherapyProtocol(
                protocol_id="TNF-ST",
                protocol_name="TNF Inhibitor Step Therapy",
                description="DMARDs required before TNF inhibitor",
                target_drugs=[
                    "00074320502",  # Humira
                    "59011035001",  # Enbrel
                    "00007414002",  # Remicade
                ],
                steps=[
                    StepTherapyStep(
                        step_number=1,
                        step_name="Methotrexate",
                        required_drugs=["6620001"],  # Methotrexate GPI prefix
                        minimum_days=90,
                        minimum_fills=3,
                        description="Must try methotrexate for 90 days",
                    ),
                    StepTherapyStep(
                        step_number=2,
                        step_name="Second DMARD",
                        required_drugs=[
                            "6640001",  # Sulfasalazine
                            "6640002",  # Leflunomide
                            "6640003",  # Hydroxychloroquine
                        ],
                        minimum_days=60,
                        minimum_fills=2,
                        description="Must try second DMARD for 60 days",
                    ),
                ],
            )
        )

        # GLP-1 Step Therapy
        self.add_protocol(
            StepTherapyProtocol(
                protocol_id="GLP1-ST",
                protocol_name="GLP-1 Step Therapy",
                description="Metformin required before GLP-1",
                target_drugs=[
                    "00169413512",  # Ozempic
                    "00169410112",  # Victoza
                    "00002146880",  # Trulicity
                    "00169017415",  # Wegovy
                ],
                steps=[
                    StepTherapyStep(
                        step_number=1,
                        step_name="Metformin",
                        required_drugs=["2710003"],  # Metformin GPI prefix
                        minimum_days=90,
                        minimum_fills=3,
                        description="Must try metformin for 90 days",
                    )
                ],
            )
        )

        # Statin Step Therapy
        self.add_protocol(
            StepTherapyProtocol(
                protocol_id="STATIN-ST",
                protocol_name="Brand Statin Step Therapy",
                description="Generic statin required before brand",
                target_drugs=[
                    "00069015430",  # Lipitor
                    "00006072631",  # Zocor
                    "00310075590",  # Crestor
                ],
                steps=[
                    StepTherapyStep(
                        step_number=1,
                        step_name="Generic Statin",
                        required_drugs=[
                            "3940001",  # Atorvastatin
                            "3940003",  # Simvastatin
                            "3940005",  # Pravastatin
                            "3940007",  # Rosuvastatin
                        ],
                        minimum_days=30,
                        minimum_fills=1,
                        description="Must try generic statin for 30 days",
                    )
                ],
            )
        )

    def add_protocol(self, protocol: StepTherapyProtocol) -> None:
        """Add a step therapy protocol."""
        self.protocols[protocol.protocol_id] = protocol

    def get_protocol(self, protocol_id: str) -> StepTherapyProtocol | None:
        """Get protocol by ID."""
        return self.protocols.get(protocol_id)

    def find_protocol_for_drug(self, ndc: str) -> StepTherapyProtocol | None:
        """Find step therapy protocol for a drug."""
        for protocol in self.protocols.values():
            for target in protocol.target_drugs:
                if ndc == target or ndc.startswith(target):
                    return protocol
        return None

    def check_step_therapy(
        self,
        ndc: str,
        claim_history: list,
        service_date: date,
    ) -> StepTherapyResult | None:
        """Check if step therapy is required and satisfied for a drug."""
        protocol = self.find_protocol_for_drug(ndc)
        if not protocol:
            return None

        return protocol.check_satisfied(ndc, claim_history, service_date)
