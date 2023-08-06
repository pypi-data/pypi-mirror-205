# (generated with --quick)

import gymnasium as gym
import hsuanwu.xploit.agent.base
import hsuanwu.xploit.agent.network
import hsuanwu.xploit.storage.vanilla_rollout_storage
import torch as th
from torch import nn
from typing import Any, Dict, List, Optional, Type, Union

ActorCritic: Type[hsuanwu.xploit.agent.network.ActorCritic]
BaseAgent: Type[hsuanwu.xploit.agent.base.BaseAgent]
DEFAULT_CFGS: Dict[str, Union[int, str, Dict[str, Optional[Union[float, int, str, Dict[nothing, nothing], Type[Union[int, str]]]]]]]
DictConfig: Any
MATCH_KEYS: Dict[str, Union[str, List[str]]]
Storage: Type[hsuanwu.xploit.storage.vanilla_rollout_storage.VanillaRolloutStorage]

class PPO(hsuanwu.xploit.agent.base.BaseAgent):
    __doc__: str
    ac: Any
    ac_opt: Any
    aug_coef: float
    clip_range: float
    ent_coef: float
    max_grad_norm: float
    n_epochs: int
    num_mini_batch: int
    training: bool
    vf_coef: float
    def __init__(self, observation_space, action_space, device: str, feature_dim: int, lr: float, eps: float, hidden_dim: int, clip_range: float, n_epochs: int, num_mini_batch: int, vf_coef: float, ent_coef: float, aug_coef: float, max_grad_norm: float) -> None: ...
    def act(self, obs, training: bool = ..., step: int = ...) -> tuple: ...
    def get_value(self, obs) -> Any: ...
    def train(self, training: bool = ...) -> None: ...
    def update(self, rollout_storage: hsuanwu.xploit.storage.vanilla_rollout_storage.VanillaRolloutStorage, episode: int = ...) -> Dict[str, float]: ...
