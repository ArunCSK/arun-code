"""Configuration loader for Arun-Code.

Reads environment variables from .env file and exposes them as a typed object.
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class NIMConfig:
    """Configuration for NVIDIA NIM API access."""

    endpoint: str
    api_key: str
    model: str
    max_tokens: int
    temperature: float


def load_config() -> NIMConfig:
    """Load configuration from environment variables.

    Raises ValueError if required NVIDIA_BEARER is missing.
    """
    load_dotenv()

    api_key = os.environ.get("NVIDIA_BEARER", "")
    if not api_key:
        raise ValueError(
            "NVIDIA_BEARER environment variable is required. "
            "Copy .env.example to .env and set your API key."
        )

    return NIMConfig(
        endpoint=os.environ.get(
            "NVIDIA_ENDPOINT",
            "https://integrate.api.nvidia.com/v1/chat/completions",
        ),
        api_key=api_key,
        model=os.environ.get("NVIDIA_MODEL", "google/diffusiongemma-26b-a4b-it"),
        max_tokens=int(os.environ.get("NVIDIA_MAX_TOKENS", "4096")),
        temperature=float(os.environ.get("NVIDIA_TEMPERATURE", "0.7")),
    )
