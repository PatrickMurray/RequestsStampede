# pylint: disable=redefined-outer-name

"""
Tests the retry configuration objects present in RequestsStampede.config
"""


import math

import pytest

import RequestsStampede.config
import RequestsStampede.policy.retry
import RequestsStampede.policy.backoff


@pytest.fixture
def default_retry_config():
    """
    TODO
    """
    return RequestsStampede.config.DefaultRetryConfig()


@pytest.fixture
def relaxed_retry_config():
    """
    TODO
    """
    return RequestsStampede.config.RelaxedRetryConfig()


@pytest.fixture
def aggressive_retry_config():
    """
    TODO
    """
    return RequestsStampede.config.AggressiveRetryConfig()


def test_default_retry_config_parameters(default_retry_config):
    """
    Ensures that the default retry configuration is valid and permitting a
    maximum of 5 retry attempts under a fibonacci backoff policy. The backoff
    policy will have an initial delay of 0 seconds with a maximum delay of 144
    seconds.
    """
    assert isinstance(default_retry_config, RequestsStampede.config.AbstractRetryConfig)

    # Validate enablement flags
    assert isinstance(default_retry_config.retry_enabled, bool)
    assert isinstance(default_retry_config.backoff_enabled, bool)
    assert default_retry_config.retry_enabled
    assert default_retry_config.backoff_enabled

    # Validate retry_policy and default values
    assert isinstance(
        default_retry_config.retry_policy,
        RequestsStampede.policy.retry.AbstractRetryPolicy,
    )
    assert isinstance(
        default_retry_config.retry_policy,
        RequestsStampede.policy.retry.FixedRetryPolicy,
    )
    assert isinstance(default_retry_config.retry_policy.attempts, int)
    assert default_retry_config.retry_policy.attempts == 5

    # Validate backoff_policy and default values
    assert isinstance(
        default_retry_config.backoff_policy,
        RequestsStampede.policy.backoff.AbstractBackoffPolicy,
    )
    assert isinstance(
        default_retry_config.backoff_policy,
        RequestsStampede.policy.backoff.FibonacciBackoffPolicy,
    )
    assert isinstance(default_retry_config.backoff_policy.initial_delay, float)
    assert isinstance(default_retry_config.backoff_policy.maximum_delay, float)
    assert default_retry_config.backoff_policy.initial_delay == 0.0
    assert default_retry_config.backoff_policy.maximum_delay == 144.0


def test_relaxed_retry_config_parameters(relaxed_retry_config):
    """
    Ensures that the relaxed retry configuration is valid. For the moment, the
    relaxed and default retry configuration are identical; however, that may
    change in the future.
    """
    assert isinstance(relaxed_retry_config, RequestsStampede.config.AbstractRetryConfig)
    assert isinstance(relaxed_retry_config, RequestsStampede.config.DefaultRetryConfig)

    # Validate enablement flags
    assert isinstance(relaxed_retry_config.retry_enabled, bool)
    assert isinstance(relaxed_retry_config.backoff_enabled, bool)
    assert relaxed_retry_config.retry_enabled
    assert relaxed_retry_config.backoff_enabled

    # Validate retry_policy and default values
    assert isinstance(
        relaxed_retry_config.retry_policy,
        RequestsStampede.policy.retry.AbstractRetryPolicy,
    )
    assert isinstance(
        relaxed_retry_config.retry_policy,
        RequestsStampede.policy.retry.FixedRetryPolicy,
    )
    assert isinstance(relaxed_retry_config.retry_policy.attempts, int)
    assert relaxed_retry_config.retry_policy.attempts == 5

    # Validate backoff_policy and default values
    assert isinstance(
        relaxed_retry_config.backoff_policy,
        RequestsStampede.policy.backoff.AbstractBackoffPolicy,
    )
    assert isinstance(
        relaxed_retry_config.backoff_policy,
        RequestsStampede.policy.backoff.FibonacciBackoffPolicy,
    )
    assert isinstance(relaxed_retry_config.backoff_policy.initial_delay, float)
    assert isinstance(relaxed_retry_config.backoff_policy.maximum_delay, float)
    assert relaxed_retry_config.backoff_policy.initial_delay == 0.0
    assert relaxed_retry_config.backoff_policy.maximum_delay == 144.0


def test_aggressive_retry_config_parameters(aggressive_retry_config):
    """
    Ensures that the aggressive retry configuration is valid and configured to
    expected parameters. An unmodified aggressive retry configuration will
    attempt an infinite number of retry attempts

    TODO
    """
    assert isinstance(
        aggressive_retry_config, RequestsStampede.config.AbstractRetryConfig
    )

    # Validate enablement flags
    assert isinstance(aggressive_retry_config.retry_enabled, bool)
    assert isinstance(aggressive_retry_config.backoff_enabled, bool)
    assert aggressive_retry_config.retry_enabled
    assert aggressive_retry_config.backoff_enabled

    # Validate retry_policy and default values
    assert isinstance(
        aggressive_retry_config.retry_policy,
        RequestsStampede.policy.retry.AbstractRetryPolicy,
    )
    assert isinstance(
        aggressive_retry_config.retry_policy,
        RequestsStampede.policy.retry.InfiniteRetryPolicy,
    )
    assert isinstance(aggressive_retry_config.retry_policy.attempts, float)
    assert aggressive_retry_config.retry_policy.attempts == math.inf

    # Validate backoff_policy and default values
    assert isinstance(
        aggressive_retry_config.backoff_policy,
        RequestsStampede.policy.backoff.AbstractBackoffPolicy,
    )
    assert isinstance(
        aggressive_retry_config.backoff_policy,
        RequestsStampede.policy.backoff.FixedBackoffPolicy,
    )
    assert isinstance(aggressive_retry_config.backoff_policy.constant_delay, float)
    assert aggressive_retry_config.backoff_policy.constant_delay == 5.0
