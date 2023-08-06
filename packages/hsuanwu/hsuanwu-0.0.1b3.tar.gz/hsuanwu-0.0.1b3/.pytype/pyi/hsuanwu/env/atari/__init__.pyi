# (generated with --quick)

import gymnasium as gym
import hsuanwu.env.atari.wrappers
import hsuanwu.env.utils
import numpy as np
from typing import Any, Type

EpisodicLifeEnv: Type[hsuanwu.env.atari.wrappers.EpisodicLifeEnv]
FireResetEnv: Type[hsuanwu.env.atari.wrappers.FireResetEnv]
FrameStack: Any
GrayScaleObservation: Any
HsuanwuEnvWrapper: Type[hsuanwu.env.utils.HsuanwuEnvWrapper]
MaxAndSkipEnv: Type[hsuanwu.env.atari.wrappers.MaxAndSkipEnv]
NoopResetEnv: Type[hsuanwu.env.atari.wrappers.NoopResetEnv]
RecordEpisodeStatistics: Any
ResizeObservation: Any
SyncVectorEnv: Any
TransformReward: Any

def make_atari_env(env_id: str = ..., num_envs: int = ..., device: str = ..., seed: int = ..., frame_stack: int = ...) -> Any: ...
