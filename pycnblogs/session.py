"""Session management for PAT (Personal Access Token)."""

import os
from pathlib import Path
from typing import Optional
from .exceptions import AuthenticationError


def get_config_path() -> Path:
    """Get the configuration file path."""
    home = Path.home()
    return home / ".cnbrc"


def save_pat(pat: str) -> Path:
    """Save PAT to config file."""
    config_path = get_config_path()
    config_path.write_text(pat, encoding="utf-8")
    return config_path


def load_pat() -> str:
    """Load PAT from config file."""
    config_path = get_config_path()
    if not config_path.exists():
        raise AuthenticationError(
            f"Config file not found at {config_path}. Please login first."
        )
    return config_path.read_text(encoding="utf-8").strip()


def remove_pat() -> Path:
    """Remove PAT from config file."""
    config_path = get_config_path()
    if config_path.exists():
        config_path.unlink()
    return config_path
