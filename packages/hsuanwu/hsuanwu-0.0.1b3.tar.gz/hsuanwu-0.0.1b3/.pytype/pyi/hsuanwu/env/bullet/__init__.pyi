# (generated with --quick)

import gym as old_gym
import gymnasium as gym
import hsuanwu.env.utils
import numpy as np
from typing import Any, Tuple, Type

HsuanwuEnvWrapper: Type[hsuanwu.env.utils.HsuanwuEnvWrapper]
RecordEpisodeStatistics: Any
SyncVectorEnv: Any

class AdapterEnv(Any):
    __doc__: str
    action_space: Any
    observation_space: Any
    def __init__(self, env) -> None: ...
    def reset(self, **kwargs) -> Tuple[np.ndarray, dict]: ...
    def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, dict]: ...

def make_bullet_env(env_id: str = ..., num_envs: int = ..., device: str = ..., seed: int = ...) -> Any: ...
