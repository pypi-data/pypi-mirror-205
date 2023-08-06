import math
from dataclasses import dataclass
from typing import Any

import numpy as np
from scipy import stats


@dataclass
class TolBand:
    ll: float
    ul: float


def simple_cm(data: list[float], tolerances: TolBand) -> np.floating[Any]:
    try:
        std = np.std(data, ddof=1)
        cm = (tolerances.ul - tolerances.ll) / (6 * std)
    except TypeError:
        raise TypeError
    if np.isnan(cm):
        raise ValueError("The data list cannot be empty")
    return cm


def cm_window(
    data: list[float], tolerances: TolBand
) -> tuple[np.floating[Any], np.floating[Any]]:
    n = len(data)
    if n == 1:
        raise ValueError
    cm = simple_cm(data, tolerances)
    cm_min = cm * math.sqrt(stats.chi2.ppf(0.025, n - 1) / (n - 1))
    cm_max = cm * math.sqrt(stats.chi2.ppf(1 - 0.025, n - 1) / (n - 1))
    return cm_min, cm_max
