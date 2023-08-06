# (generated with --quick)

import gymnasium as gym
import hsuanwu.common.engine.base_policy_trainer
import hsuanwu.common.engine.utils
import hydra
import numpy as np
import omegaconf
import pathlib
import torch as th
from typing import Annotated, Any, Dict, Iterable, Type

BasePolicyTrainer: Type[hsuanwu.common.engine.base_policy_trainer.BasePolicyTrainer]
Path: Type[pathlib.Path]
eval_mode: Type[hsuanwu.common.engine.utils.eval_mode]

class OffPolicyTrainer(hsuanwu.common.engine.base_policy_trainer.BasePolicyTrainer):
    __doc__: str
    _agent: Any
    _global_episode: int
    _global_step: int
    _num_init_steps: Any
    _replay_iter: Any
    _replay_loader: Any
    _replay_storage: Any
    _use_nstep_replay_storage: bool
    replay_iter: Annotated[Iterable, 'property']
    def __init__(self, cfgs, train_env, test_env = ...) -> None: ...
    def save(self) -> None: ...
    def test(self) -> Dict[str, float]: ...
    def train(self) -> None: ...

def worker_init_fn(worker_id) -> None: ...
