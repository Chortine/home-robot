import copy

# from projects.habitat_ovmm.utils.env_utils import
import pickle
from typing import TYPE_CHECKING

import cv2
import numpy as np
from habitat import make_dataset
from habitat.core.environments import get_env_class
from habitat.utils.gym_definitions import _get_env_name
from omegaconf import OmegaConf

import home_robot.core.interfaces
from home_robot.core.interfaces import (
    ContinuousFullBodyAction,
    ContinuousNavigationAction,
    DiscreteNavigationAction,
)
from home_robot_sim.env.habitat_ovmm_env.habitat_ovmm_env import (
    HabitatOpenVocabManipEnv,
)
import os, sys

current_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_ovmm_env_fn() -> HabitatOpenVocabManipEnv:
    """
    Creates an environment for the OVMM task.

    Creates habitat environment from config and wraps it into HabitatOpenVocabManipEnv.

    :param config: configuration for the environment.
    :return: environment instance.
    """

    with open(
        "/home/tianchu/Documents/code_qy/home-robot-new/my_scripts/habitat_config.pkl",
        "rb",
    ) as handle:
        config = pickle.load(handle)

    # =========== change your config here ================== #
    OmegaConf.set_readonly(config, False)
    config.habitat.dataset.data_path = os.path.join(current_root, 'data/datasets/ovmm/train/content/102344193.json.gz')
    config.habitat.dataset.split = "train"
    config.habitat.task.episode_init = False
    config.GROUND_TRUTH_SEMANTICS = 1

    # config.habitat.dataset.episode_ids = [128]
    # --------------- end changing config -------------------#

    habitat_config = config.habitat
    dataset = make_dataset(habitat_config.dataset.type, config=habitat_config.dataset)
    env_class_name = _get_env_name(config)
    env_class = get_env_class(env_class_name)
    habitat_env = env_class(config=habitat_config, dataset=dataset)
    habitat_env.seed(habitat_config.seed)
    env = HabitatOpenVocabManipEnv(habitat_env, config, dataset=dataset)
    return env


def try_env():
    # initialize an env here, and control it with kb
    my_ovmm_env = create_ovmm_env_fn()
    my_ovmm_env.reset()
    while True:
        """
        The action contains:
        1. the arm_action dim: 7
        2. the base_action dim: 5
        total dim: 12
        """

        observations, done, hab_info = my_ovmm_env.apply_action(
            action=DiscreteNavigationAction.TURN_LEFT, info=None
        )
        visualize_habitat_obs(observations)


def visualize_habitat_obs(observations):
    rgb = observations.rgb
    depth = observations.depth
    third_rgb = observations.third_person_image
    semantic = observations.semantic

    goal_name = observations.task_observations["goal_name"]
    goal_receptacle = observations.task_observations["place_recep_name"]
    start_receptacle = observations.task_observations["start_recep_name"]

    print(
        f"===== Pick {goal_name} from {start_receptacle} and place it to {goal_receptacle}"
    )

    cv2.imshow("rgb", rgb)
    cv2.imshow("depth", depth / 15.0)
    cv2.imshow("third_rgb", third_rgb)
    cv2.waitKey(1)


def try_env_kb():
    from utils.keyboard_handler import KB_Handler

    class my_kb_Hander(KB_Handler):
        def main_step(self, env, action):
            observations, done, hab_info = env.apply_action(action, info=None)
            visualize_habitat_obs(observations)
            return done
            # print('aaaaaaaa')
            # return obs_dict, done, info_dict

    kb = my_kb_Hander()
    my_ovmm_env = create_ovmm_env_fn()
    my_ovmm_env.reset()
    kb.keyboard_control_on_env(my_ovmm_env)


if __name__ == "__main__":
    # load_transform_matrix()
    try_env_kb()
