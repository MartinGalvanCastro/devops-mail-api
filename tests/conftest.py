import os

import pytest


def str_to_bool(val: str) -> bool:
    """
    Convert a string value into a boolean.
    Recognizes "true", "1", "yes", "on" (case-insensitive) as True; otherwise False.
    """
    return val.strip().lower() in ("true", "1", "yes", "on")


@pytest.fixture(autouse=True)
def simulate_failure_check():
    """
    This fixture runs automatically for every test.
    It converts the SIMULATE_FAILURES environment variable to a Boolean.
    If SIMULATE_FAILURES is True, it forces a failure via an assertion (True == False).
    """
    simulate = str_to_bool(os.getenv("SIMULATE_FAILURES", "false"))
    # Force a simulated failure if the value is True.
    assert not simulate, "Simulated failure triggered: SIMULATE_FAILURES is True"
