# (generated with --quick)

import collections
import datetime
import gymnasium as gym
import numpy as np
import pathlib
import random
import torch as th
import traceback
from typing import Annotated, Any, Dict, Generator, List, Type

DictConfig: Any
IterableDataset: Any
Path: Type[pathlib.Path]
defaultdict: Type[collections.defaultdict]

class NStepReplayStorage(Any):
    __doc__: str
    _batch_size: int
    _discount: float
    _fetch_every: int
    _fetched_samples: int
    _n_step: int
    _num_workers: int
    _pin_memory: bool
    _replay_dir: pathlib.Path
    _replay_storage: ReplayStorage
    _save_snapshot: bool
    _storage_size: int
    _worker_eps_fn_pool: List[pathlib.Path]
    _worker_eps_pool: Dict[pathlib.Path, dict]
    _worker_max_size: int
    _worker_size: int
    get_batch_size: Annotated[int, 'property']
    get_num_workers: Annotated[int, 'property']
    get_pin_memory: Annotated[bool, 'property']
    def __init__(self, observation_space, action_space, device: str = ..., storage_size: int = ..., batch_size: int = ..., num_workers: int = ..., pin_memory: bool = ..., n_step: int = ..., discount: float = ..., fetch_every: int = ..., save_snapshot: bool = ...) -> None: ...
    def __iter__(self) -> Generator[tuple, Any, Any]: ...
    def _sample_episode(self) -> dict: ...
    def _store_episode(self, eps_fn: pathlib.Path) -> bool: ...
    def _try_fetch(self) -> None: ...
    def add(self, obs, action, reward, terminated, info, next_obs) -> None: ...
    def sample(self) -> tuple: ...

class ReplayStorage:
    __doc__: str
    _current_episode: collections.defaultdict[str, Any]
    _num_episodes: int
    _num_transitions: int
    _replay_dir: pathlib.Path
    num_episodes: Annotated[int, 'property']
    num_transitions: Annotated[int, 'property']
    def __init__(self, replay_dir: pathlib.Path) -> None: ...
    def _store_episode(self, episode: dict) -> None: ...
    def add(self, obs, action, reward: float, terminated: bool, discount: float) -> None: ...

def dump_episode(episode: dict, fn: pathlib.Path) -> None: ...
def episode_len(episode: dict) -> int: ...
def load_episode(fn: pathlib.Path) -> dict: ...
