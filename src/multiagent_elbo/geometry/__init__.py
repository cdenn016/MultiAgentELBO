"""Typed finite and continuous geometry adapters."""

from .attention_gauge import (
    AttentionCovariantInputs,
    AttentionGaugeEvaluation,
    evaluate_attention,
    transform_attention_inputs,
)
from .finite_gauge import (
    FiniteGaugeResiduals,
    FinitePermutation,
    FiniteRelabelingResult,
    apply_site_relabeling,
)

__all__ = [
    "AttentionCovariantInputs",
    "AttentionGaugeEvaluation",
    "FiniteGaugeResiduals",
    "FinitePermutation",
    "FiniteRelabelingResult",
    "apply_site_relabeling",
    "evaluate_attention",
    "transform_attention_inputs",
]
