# -*- coding: utf-8 -*-
"""Evironment variable utils."""

import os


class MissingEnvironmentVariable(Exception):
    """Raised when an environment variable is missing."""

    def __init__(self, variable_name: str):
        """Initialize."""
        super().__init__(f"Environment variable {variable_name} is missing.")


def is_mocking_auth() -> bool:
    """Return whether the env variable MOCK_AUTH is set to true. Returns false if unset, raises ValueError if set and neither true/false.

    Raises:
        ValueError,
        MissingEnvironmentVariable
    """
    try:
        mock_auth = get_env("MOCK_AUTH").lower()
    except MissingEnvironmentVariable:
        return False

    if mock_auth == "true":
        return True
    elif mock_auth == "false":
        return False
    else:
        raise ValueError(f"Invalid MOCK_AUTH value. Expected 'true'/'false', found {mock_auth}.")


def get_env(variable_name: str) -> str:
    """Get environment variable if it exists.

    Raises:
        MissingEnvironmentVariable
    """
    env_var = os.getenv(variable_name)
    if os.getenv(variable_name) is not None:
        return str(env_var)
    else:
        raise MissingEnvironmentVariable(variable_name)
