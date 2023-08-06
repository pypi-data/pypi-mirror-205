# (generated with --quick)

import numpy as np
from scipy import stats as sts
from typing import Any

class Comparison:
    __doc__: str
    num_runs_x: int
    num_runs_y: int
    num_tasks: int
    scores_x: np.ndarray[Any, np.dtype]
    scores_y: np.ndarray[Any, np.dtype]
    def __init__(self, scores_x: np.ndarray, scores_y: np.ndarray) -> None: ...
    def compute_poi(self) -> Any: ...
