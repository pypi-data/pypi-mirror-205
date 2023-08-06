# (generated with --quick)

import gymnasium as gym
import hsuanwu.xploit.encoder.base
import torch as th
from torch import nn
from torch.nn import functional as F
from typing import Any, List, Tuple, Type

BaseEncoder: Type[hsuanwu.xploit.encoder.base.BaseEncoder]
DictConfig: Any

class EspeholtResidualEncoder(hsuanwu.xploit.encoder.base.BaseEncoder):
    __doc__: str
    linear: Any
    trunk: Any
    def __init__(self, observation_space, feature_dim: int = ..., net_arch: List[int] = ...) -> None: ...
    def forward(self, obs) -> Any: ...

class ResidualBlock(Any):
    __doc__: str
    conv0: Any
    conv1: Any
    def __init__(self, channels: int) -> None: ...
    def forward(self, x) -> Any: ...

class ResidualLayer(Any):
    __doc__: str
    _input_shape: tuple
    _out_channels: int
    conv: Any
    res_block0: ResidualBlock
    res_block1: ResidualBlock
    def __init__(self, input_shape: tuple, out_channels: int) -> None: ...
    def forward(self, x) -> Any: ...
    def get_output_shape(self) -> Tuple[int, Any, Any]: ...

def network_init(m) -> None: ...
