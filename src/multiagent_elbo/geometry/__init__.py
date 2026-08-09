"""Typed finite and continuous geometry adapters."""

from .finite_gauge import (
    FiniteGaugeResiduals,
    FinitePermutation,
    FiniteRelabelingResult,
    apply_site_relabeling,
)

__all__ = [
    "FiniteGaugeResiduals",
    "FinitePermutation",
    "FiniteRelabelingResult",
    "apply_site_relabeling",
]
