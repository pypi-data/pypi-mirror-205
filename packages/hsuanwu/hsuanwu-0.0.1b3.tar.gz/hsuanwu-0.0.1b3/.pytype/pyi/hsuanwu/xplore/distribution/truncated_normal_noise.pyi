# (generated with --quick)

import hsuanwu.xplore.distribution.base
import torch as th
from hsuanwu.xplore.distribution import utils
from torch import distributions as pyd
from typing import Annotated, Any, Type

BaseDistribution: Type[hsuanwu.xplore.distribution.base.BaseDistribution]

class TruncatedNormalNoise(hsuanwu.xplore.distribution.base.BaseDistribution):
    __doc__: str
    _mu: float
    _noiseless_action: Any
    _sigma: float
    _stddev_clip: float
    _stddev_schedule: str
    dist: Any
    mean: Annotated[Any, 'property']
    mode: Annotated[Any, 'property']
    def __init__(self, mu: float = ..., sigma: float = ..., stddev_schedule: str = ..., stddev_clip: float = ...) -> None: ...
    def entropy(self) -> Any: ...
    def log_prob(self, value) -> Any: ...
    def reset(self, noiseless_action, step: int = ...) -> None: ...
    def rsample(self, sample_shape = ...) -> Any: ...
    def sample(self, clip: bool = ..., sample_shape = ...) -> Any: ...
