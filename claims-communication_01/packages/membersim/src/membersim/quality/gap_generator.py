"""Generate care gap data for members."""

import random
from datetime import date, timedelta

from membersim.core.member import Member
from membersim.quality.hedis import HEDIS_MEASURES, get_measures_for_member
from membersim.quality.measure import GapStatus, MemberMeasureStatus


def _calculate_age(birth_date: date, as_of: date) -> int:
    """Calculate age as of a specific date."""
    age = as_of.year - birth_date.year
    if (as_of.month, as_of.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age


def _get_gender_code(member: Member) -> str:
    """Extract gender code from member."""
    # Member extends Person which has gender as Gender enum
    gender = member.gender
    gender_str = str(gender.value).upper() if hasattr(gender, "value") else str(gender).upper()

    if gender_str in ("M", "MALE"):
        return "M"
    elif gender_str in ("F", "FEMALE"):
        return "F"
    return "U"


def generate_measure_status(
    member: Member,
    measure_id: str,
    measure_year: int,
    gap_probability: float = 0.3,
    seed: int | None = None,
) -> MemberMeasureStatus:
    """
    Generate measure status for a single member/measure.

    Args:
        member: The member to evaluate
        measure_id: HEDIS measure ID
        measure_year: Measurement year
        gap_probability: Probability of having an open gap (0-1)
        seed: Random seed for reproducibility

    Returns:
        MemberMeasureStatus for this member/measure
    """
    if seed is not None:
        random.seed(seed)

    measure = HEDIS_MEASURES.get(measure_id)
    if not measure:
        return MemberMeasureStatus(
            member_id=member.member_id,
            measure_id=measure_id,
            measure_year=measure_year,
            in_denominator=False,
            gap_status=GapStatus.NOT_APPLICABLE,
        )

    # Member extends Person, so birth_date and gender are direct attributes
    age = _calculate_age(member.birth_date, date(measure_year, 12, 31))
    gender = _get_gender_code(member)

    # Check if member is in denominator
    in_denominator = True

    if measure.min_age and age < measure.min_age:
        in_denominator = False
    if measure.max_age and age > measure.max_age:
        in_denominator = False
    if measure.gender and measure.gender != gender:
        in_denominator = False

    if not in_denominator:
        return MemberMeasureStatus(
            member_id=member.member_id,
            measure_id=measure_id,
            measure_year=measure_year,
            in_denominator=False,
            gap_status=GapStatus.NOT_APPLICABLE,
        )

    # Check for exclusions (simplified - random for now)
    if random.random() < 0.05:  # 5% exclusion rate
        return MemberMeasureStatus(
            member_id=member.member_id,
            measure_id=measure_id,
            measure_year=measure_year,
            in_denominator=True,
            in_numerator=False,
            gap_status=GapStatus.EXCLUDED,
            exclusion_reason="Medical exclusion",
        )

    # Determine if gap is open or closed
    has_gap = random.random() < gap_probability

    if has_gap:
        return MemberMeasureStatus(
            member_id=member.member_id,
            measure_id=measure_id,
            measure_year=measure_year,
            in_denominator=True,
            in_numerator=False,
            gap_status=GapStatus.OPEN,
        )
    else:
        # Generate a random service date in the measurement period
        service_date = date(measure_year, 1, 1) + timedelta(days=random.randint(0, 364))
        return MemberMeasureStatus(
            member_id=member.member_id,
            measure_id=measure_id,
            measure_year=measure_year,
            in_denominator=True,
            in_numerator=True,
            gap_status=GapStatus.CLOSED,
            last_service_date=service_date,
        )


def generate_care_gaps(
    members: list[Member],
    measures: list[str] | None = None,
    gap_rate: float = 0.3,
    measure_year: int = 2024,
    seed: int | None = None,
) -> list[MemberMeasureStatus]:
    """
    Generate care gap data for a population.

    Args:
        members: List of members
        measures: List of measure IDs (None = all applicable)
        gap_rate: Target gap rate (0-1)
        measure_year: Measurement year
        seed: Random seed

    Returns:
        List of MemberMeasureStatus records
    """
    results = []

    for i, member in enumerate(members):
        member_seed = seed + i if seed else None
        age = _calculate_age(member.birth_date, date(measure_year, 12, 31))
        gender = _get_gender_code(member)

        # Determine applicable measures
        applicable = measures or get_measures_for_member(age, gender)

        for measure_id in applicable:
            status = generate_measure_status(
                member=member,
                measure_id=measure_id,
                measure_year=measure_year,
                gap_probability=gap_rate,
                seed=member_seed,
            )
            results.append(status)

    return results
