# (generated with --quick)

import collections
import gymnasium as gym
import hsuanwu.xploit.agent.base
import hsuanwu.xploit.agent.network
import omegaconf
import threading
import torch as th
from torch import nn
from torch.nn import functional as F
from typing import Any, Dict, List, NamedTuple, Optional, Type, Union

BaseAgent: Type[hsuanwu.xploit.agent.base.BaseAgent]
DEFAULT_CFGS: Dict[str, Union[int, str, Dict[str, Optional[Union[float, int, str, Dict[nothing, nothing], Type[Union[int, str]]]]]]]
DictConfig: Any
DiscreteLSTMActor: Type[hsuanwu.xploit.agent.network.DiscreteLSTMActor]
MATCH_KEYS: Dict[str, Union[str, List[str]]]

class IMPALA(hsuanwu.xploit.agent.base.BaseAgent):
    __doc__: str
    actor: hsuanwu.xploit.agent.network.DiscreteLSTMActor
    baseline_coef: float
    discount: float
    ent_coef: float
    learner: hsuanwu.xploit.agent.network.DiscreteLSTMActor
    max_grad_norm: float
    training: bool
    def __init__(self, observation_space, action_space, device: str, feature_dim: int, lr: float, eps: float, use_lstm: bool, ent_coef: float, baseline_coef: float, max_grad_norm: float, discount: float) -> None: ...
    def act(self, *kwargs) -> None: ...
    def train(self, training: bool = ...) -> None: ...
    @staticmethod
    def update(cfgs, actor_model, learner_model, batch: dict, init_actor_states: tuple, optimizer, lr_scheduler, lock = ...) -> Dict[str, tuple]: ...

class VTrace:
    __doc__: str
    from_importance_weights: Any
    def __init__(self) -> None: ...
    def action_log_probs(self, policy_logits, actions) -> Any: ...
    def from_logits(self, behavior_policy_logits, target_policy_logits, actions, discounts, rewards, values, bootstrap_value, clip_rho_threshold = ..., clip_pg_rho_threshold = ...) -> VTraceFromLogitsReturns: ...

class VTraceFromLogitsReturns(NamedTuple):
    vs: Any
    pg_advantages: Any
    log_rhos: Any
    behavior_action_log_probs: Any
    target_action_log_probs: Any

class VTraceReturns(NamedTuple):
    vs: Any
    pg_advantages: Any
