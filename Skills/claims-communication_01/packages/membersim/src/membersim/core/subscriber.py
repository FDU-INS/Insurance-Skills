"""Subscriber (primary policy holder) model."""

from datetime import date

from pydantic import Field

from membersim.core.member import Member


class Subscriber(Member):
    """Primary policy holder with dependents."""

    dependents: list[Member] = Field(
        default_factory=list, description="Family members on this policy"
    )
    employer_id: str = Field(..., description="Employer/sponsor identifier")
    hire_date: date = Field(..., description="Employment start date")
    benefit_class: str = Field("EMPLOYEE", description="Employee benefit tier")

    @property
    def family_size(self) -> int:
        """Total family size including subscriber."""
        return 1 + len(self.dependents)

    def get_all_members(self) -> list[Member]:
        """Get subscriber and all dependents as a list."""
        return [self] + self.dependents
