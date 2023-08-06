# (generated with --quick)

import gymnasium as gym
import torch as th
from hsuanwu.xploit.agent import utils
from torch import nn
from torch.nn import functional as F
from typing import Any, Union

Distribution: Any

class ActorCritic(Any):
    class BoxActor(Any):
        __doc__: str
        actor_logstd: Any
        actor_mu: Any
        def __init__(self, action_shape, hidden_dim) -> None: ...
        def forward(self, obs, dist) -> Any: ...
    class DiscreteActor(Any):
        __doc__: str
        actor: Any
        def __init__(self, action_shape, hidden_dim) -> None: ...
        def forward(self, obs, dist) -> Any: ...
    __doc__: str
    aux_critic: Any
    base: Union[ActorCritic.BoxActor, ActorCritic.DiscreteActor]
    critic: Any
    dist: None
    trunk: Any
    def __init__(self, action_shape: tuple, action_type: str, feature_dim: int, hidden_dim: int, aux_critic: bool = ...) -> None: ...
    def get_action(self, obs) -> Any: ...
    def get_action_and_value(self, obs, actions = ...) -> tuple: ...
    def get_logits(self, obs) -> Any: ...
    def get_probs_and_aux_value(self, obs) -> tuple: ...
    def get_value(self, obs) -> Any: ...

class DeterministicActor(Any):
    __doc__: str
    dist: None
    policy: Any
    trunk: Any
    def __init__(self, action_space, feature_dim: int = ..., hidden_dim: int = ...) -> None: ...
    def get_action(self, obs, step: int) -> Any: ...

class DiscreteLSTMActor(Any):
    baseline: Any
    dist: None
    encoder: None
    lstm: Any
    num_actions: Any
    policy: Any
    use_lstm: bool
    def __init__(self, action_space, feature_dim, hidden_dim: int = ..., use_lstm: bool = ...) -> None: ...
    def get_action(self, inputs: dict, lstm_state: tuple = ..., training: bool = ...) -> Any: ...
    def init_state(self, batch_size: int) -> tuple: ...

class DoubleCritic(Any):
    Q1: Any
    Q2: Any
    __doc__: str
    def __init__(self, action_space, feature_dim: int = ..., hidden_dim: int = ...) -> None: ...
    def forward(self, obs, action) -> tuple: ...

class StochasticActor(Any):
    __doc__: str
    dist: None
    log_std_max: Any
    log_std_min: Any
    policy: Any
    def __init__(self, action_space, feature_dim: int = ..., hidden_dim: int = ..., log_std_range: tuple = ...) -> None: ...
    def get_action(self, obs, step: int) -> Any: ...
