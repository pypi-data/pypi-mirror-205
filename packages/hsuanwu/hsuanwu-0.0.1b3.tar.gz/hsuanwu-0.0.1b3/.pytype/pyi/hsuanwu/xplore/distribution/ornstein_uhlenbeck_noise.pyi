# (generated with --quick)

import hsuanwu.xplore.distribution.base
import numpy as np
import torch as th
from hsuanwu.xplore.distribution import utils
from typing import Annotated, Any, Type

BaseDistribution: Type[hsuanwu.xplore.distribution.base.BaseDistribution]
_standard_normal: Any

class OrnsteinUhlenbeckNoise(hsuanwu.xplore.distribution.base.BaseDistribution):
    __doc__: str
    _dt: float
    _mu: float
    _noiseless_action: Any
    _sigma: Any
    _stddev_schedule: str
    _theta: float
    mean: Annotated[Any, 'property']
    mode: Annotated[Any, 'property']
    noise_prev: Any
    def __init__(self, mu: float = ..., sigma: float = ..., theta: float = ..., dt: float = ..., stddev_schedule: str = ...) -> None: ...
    def entropy(self) -> Any: ...
    def log_prob(self, value) -> Any: ...
    def reset(self, noiseless_action, step: int = ...) -> None: ...
    def rsample(self, sample_shape = ...) -> Any: ...
    def sample(self, clip: bool = ..., sample_shape = ...) -> Any: ...
