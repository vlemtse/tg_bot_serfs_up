import functools
import logging
import os
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from pydantic.v1.utils import deep_update, unique_list

from app.configs.constants import PROJECT_ROOT_PATH
from app.configs.config_yaml import load_yaml_with_envvars

logger = logging.getLogger(__name__)

_settings_folder = os.environ.get("TGBM_SETTINGS_FOLDER", PROJECT_ROOT_PATH)
_settings_folder = _settings_folder / "config"
# if running in unittest, use the test profile
test_profile = os.environ.get("TGB_TEST_PROFILE")
_test_profile = ["test"] if test_profile else []

active_profiles: list[str] = unique_list(
    ["default"]
    + [
        item.strip()
        for item in os.environ.get("TGBM_PROFILES", "").split(",")
        if item.strip()
    ]
    + _test_profile
)


def merge_settings(settings: Iterable[dict[str, Any]]) -> dict[str, Any]:
    return functools.reduce(deep_update, settings, {})


def load_settings_from_profile(profile: str) -> dict[str, Any]:
    if profile == "default":
        profile_file_name = "config.yaml"
    else:
        profile_file_name = f"config-{profile}.yaml"

    path = Path(_settings_folder) / profile_file_name
    with Path(path).open("r") as f:
        config = load_yaml_with_envvars(f)
    if not isinstance(config, dict):
        raise TypeError(f"Config file has no top-level mapping: {path}")
    return config


def load_active_settings() -> dict[str, Any]:
    """Load active profiles and merge them."""
    logger.info("Starting application with profiles=%s", active_profiles)
    loaded_profiles = [
        load_settings_from_profile(profile) for profile in active_profiles
    ]
    merged: dict[str, Any] = merge_settings(loaded_profiles)
    return merged
