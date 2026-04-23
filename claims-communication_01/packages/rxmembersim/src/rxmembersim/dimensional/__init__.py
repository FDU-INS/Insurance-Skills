"""RxMemberSim Dimensional Output.

Transforms RxMemberSim canonical models into dimensional (star schema) format
for analytics, reporting, and BI tools.
"""

from .transformer import RxMemberSimDimensionalTransformer

__all__ = ["RxMemberSimDimensionalTransformer"]
