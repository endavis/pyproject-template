"""Shared pytest configuration and Hypothesis profiles."""

import os

from hypothesis import HealthCheck, settings

# CI profile: fewer examples, relaxed deadline for slow CI runners
settings.register_profile(
    "ci",
    max_examples=50,
    deadline=500,
    suppress_health_check=[HealthCheck.too_slow],
)

# Default profile: more thorough exploration for local development
settings.register_profile(
    "default",
    max_examples=200,
)

settings.load_profile(os.environ.get("HYPOTHESIS_PROFILE", "default"))
