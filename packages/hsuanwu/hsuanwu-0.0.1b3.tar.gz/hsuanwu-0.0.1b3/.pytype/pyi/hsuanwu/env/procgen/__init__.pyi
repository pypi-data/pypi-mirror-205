# (generated with --quick)

import gymnasium as gym
import hsuanwu.env.utils
import numpy as np
from typing import Any, List, Tuple, Type

Box: Any
HsuanwuEnvWrapper: Type[hsuanwu.env.utils.HsuanwuEnvWrapper]
NormalizeReward: Any
ProcgenEnv: Any
RecordEpisodeStatistics: Any
TransformObservation: Any
TransformReward: Any

class AdapterEnv(Any):
    __doc__: str
    envs: List[int]
    is_vector_env: bool
    single_action_space: Any
    single_observation_space: Any
    def __init__(self, env, num_envs: int) -> None: ...
    def reset(self, **kwargs) -> Tuple[np.ndarray, dict]: ...
    def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, dict]: ...

def make_procgen_env(env_id: str = ..., num_envs: int = ..., gamma: float = ..., num_levels: int = ..., start_level: int = ..., distribution_mode: str = ..., device: str = ...) -> Any: ...
