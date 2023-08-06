from abc import ABC, abstractmethod
from typing import Dict, Tuple, Union

import gymnasium as gym
import torch as th
from omegaconf import DictConfig


class BaseAgent(ABC):
    """Base class of agent.

    Args:
        observation_space (Space or DictConfig): The observation space of environment. When invoked by Hydra,
            'observation_space' is a 'DictConfig' like {"shape": observation_space.shape, }.
        action_space (Space or DictConfig): The action space of environment. When invoked by Hydra,
            'action_space' is a 'DictConfig' like
            {"shape": (n, ), "type": "Discrete", "range": [0, n - 1]} or
            {"shape": action_space.shape, "type": "Box", "range": [action_space.low[0], action_space.high[0]]}.
        device (str): Device (cpu, cuda, ...) on which the code should be run.
        feature_dim (int): Number of features extracted by the encoder.
        lr (float): The learning rate.
        eps (float): Term added to the denominator to improve numerical stability.

    Returns:
        Base agent instance.
    """

    def __init__(
        self,
        observation_space: Union[gym.Space, DictConfig],
        action_space: Union[gym.Space, DictConfig],
        device: str,
        feature_dim: int,
        lr: float,
        eps: float,
    ) -> None:
        if isinstance(observation_space, gym.Space) and isinstance(action_space, gym.Space):
            self.obs_shape = observation_space.shape
            if action_space.__class__.__name__ == "Discrete":
                self.action_shape = (int(action_space.n),)  # type: ignore[attr-defined]
                self.action_type = "Discrete"
                self.action_range = [0, int(action_space.n) - 1]  # type: ignore[attr-defined]
            elif action_space.__class__.__name__ == "Box":
                self.action_shape = action_space.shape  # type: ignore[attr-defined, list-item, assignment]
                self.action_type = "Box"
                self.action_range = [
                    float(action_space.low[0]),  # type: ignore[attr-defined, list-item]
                    float(action_space.high[0]),  # type: ignore[attr-defined, list-item]
                ]
            else:
                raise NotImplementedError("Unsupported action type!")
        elif isinstance(observation_space, DictConfig) and isinstance(action_space, DictConfig):
            # by DictConfig
            self.obs_shape = observation_space.shape
            self.action_shape = action_space.shape
            self.action_type = action_space.type
            self.action_range = action_space.range
        else:
            raise NotImplementedError("Unsupported observation and action spaces!")

        self.device = th.device(device)
        self.feature_dim = feature_dim
        self.lr = lr
        self.eps = eps

        # placeholder for distribution, augmentation, and intrinsic reward function.
        self.encoder = None
        self.encoder_opt = None
        self.dist = None
        self.aug = None
        self.irs = None

    @abstractmethod
    def train(self, training: bool = True) -> None:
        """Set the train mode.

        Args:
            training (bool): True (training) or False (testing).

        Returns:
            None.
        """
        self.training = training

    @abstractmethod
    def act(self, obs: th.Tensor, training: bool = True, step: int = 0) -> Tuple[th.Tensor]:
        """Sample actions based on observations.

        Args:
            obs (Tensor): Observations.
            training (bool): training mode, True or False.
            step (int): Global training step.

        Returns:
            Sampled actions.
        """

    @abstractmethod
    def update(self, *kwargs) -> Dict[str, float]:
        """Update agent and return training metrics such as loss functions."""
