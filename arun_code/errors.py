"""Structured error response formatting for Arun-Code.

Provides consistent, human-friendly error messages for NIM API failures
and configuration issues.
"""

from __future__ import annotations


def format_nim_error(status_code: int, detail: str) -> str:
    """Return a human-friendly error message for a NIM API failure."""
    if status_code == 404:
        return (
            f"NVIDIA NIM endpoint returned 404 Not Found. {detail}\n\n"
            "Troubleshooting steps:\n"
            "  1. Verify that NVIDIA_ENDPOINT in your .env file points to a valid URL.\n"
            "  2. Confirm the model name (NVIDIA_MODEL) is available on your account.\n"
            "  3. If using a custom function ID, ensure it matches your NVIDIA account.\n"
            "  4. Check the NVIDIA NIM status page for any service outages."
        )
    if status_code == 401:
        return (
            "NVIDIA NIM rejected the request: unauthorized.\n\n"
            "Troubleshooting steps:\n"
            "  1. Verify that NVIDIA_BEARER is set correctly in your .env file.\n"
            "  2. Make sure the API key has not expired.\n"
            "  3. Confirm the key has access to the requested model."
        )
    if status_code == 429:
        return (
            "NVIDIA NIM rate limit exceeded. Please wait a moment and try again.\n"
            "If this persists, check your API plan limits on the NVIDIA dashboard."
        )
    return f"NVIDIA NIM API error ({status_code}): {detail}"


def format_config_error(message: str) -> str:
    """Return a user-friendly message for configuration problems."""
    return (
        f"Configuration error: {message}\n"
        "Run 'cp .env.example .env' and fill in your NVIDIA API credentials."
    )
