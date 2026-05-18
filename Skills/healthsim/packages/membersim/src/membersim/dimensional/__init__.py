"""MemberSim Dimensional Output.

Transforms MemberSim canonical models into dimensional (star schema) format
for analytics, reporting, and BI tools.
"""

from .transformer import MemberSimDimensionalTransformer

__all__ = ["MemberSimDimensionalTransformer"]
