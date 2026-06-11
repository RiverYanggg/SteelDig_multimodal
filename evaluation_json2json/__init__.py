from __future__ import annotations

import sys

sys.modules.setdefault("evaluation", sys.modules[__name__])

from evaluation.framework import run_evaluation

__all__ = ["run_evaluation"]
