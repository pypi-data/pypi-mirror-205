# (generated with --quick)

import gymnasium as gym
import hsuanwu.xploit.agent.base
import hsuanwu.xploit.agent.network
import torch as th
from hsuanwu.xploit.agent import utils
from torch.nn import functional as F
from typing import Any, Dict, List, Optional, Tuple, Type, Union

BaseAgent: Type[hsuanwu.xploit.agent.base.BaseAgent]
DEFAULT_CFGS: Dict[str, Union[int, str, Dict[str, Optional[Union[float, int, str, Dict[nothing, nothing], Type[Union[int, str]]]]]]]
DeterministicActor: Type[hsuanwu.xploit.agent.network.DeterministicActor]
DictConfig: Any
DoubleCritic: Type[hsuanwu.xploit.agent.network.DoubleCritic]
MATCH_KEYS: Dict[str, Union[str, List[str]]]

class DrQv2(hsuanwu.xploit.agent.base.BaseAgent):
    __doc__: str
    actor: Any
    actor_opt: Any
    critic: Any
    critic_opt: Any
    critic_target: Any
    critic_target_tau: float
    training: bool
    update_every_steps: int
    def __init__(self, observation_space, action_space, device: str, feature_dim: int, lr: float, eps: float, hidden_dim: int, critic_target_tau: float, update_every_steps: int) -> None: ...
    def act(self, obs, training: bool = ..., step: int = ...) -> Tuple[Any]: ...
    def train(self, training: bool = ...) -> None: ...
    def update(self, replay_iter: generator, step: int = ...) -> Dict[str, float]: ...
    def update_actor(self, obs, step: int) -> Dict[str, float]: ...
    def update_critic(self, obs, action, reward, discount, next_obs, step: int) -> Dict[str, float]: ...
