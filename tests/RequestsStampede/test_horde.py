# pylint: disable=redefined-outer-name

"""
Tests the RequestsStampede horde module.
"""


import logging
import math

import pytest
import requests
import requests.structures

import RequestsStampede.horde
import RequestsStampede.config


@pytest.fixture
def retry_request_default():
    """
    TODO
    """
    return RequestsStampede.horde.RetryRequest()


@pytest.fixture
def retry_request_custom():
    """
    TODO
    """
    return RequestsStampede.horde.RetryRequest(
        retry_config=RequestsStampede.config.AggressiveRetryConfig(
            retry_policy=RequestsStampede.policy.retry.InfiniteRetryPolicy(),
            backoff_policy=RequestsStampede.policy.backoff.RandomBackoffPolicy(),
        ),
        session=requests.Session(),
    )


@pytest.fixture
def retry_session_default():
    """
    TODO
    """
    return RequestsStampede.horde.RetrySession()


@pytest.fixture
def retry_session_custom():
    """
    TODO
    """
    custom_session = requests.Session()
    custom_session.headers.update(
        {"User-Agent": "RonSwanson/1.0", "Authorization": "Bearer ICanDoWhatIWant"}
    )

    return RequestsStampede.horde.RetrySession(
        retry_config=RequestsStampede.config.AggressiveRetryConfig(
            retry_policy=RequestsStampede.policy.retry.InfiniteRetryPolicy(),
            backoff_policy=RequestsStampede.policy.backoff.RandomBackoffPolicy(),
        ),
        session=custom_session,
    )


def test_retry_request_default_parameters(retry_request_default):
    """
    Ensures that RetryRequest default parameters are reasonable.
    """
    assert isinstance(
        retry_request_default, RequestsStampede.horde.AbstractRetryRequest
    )
    assert isinstance(retry_request_default, RequestsStampede.horde.RetryRequest)

    # Validate retry_config
    retry_config = retry_request_default.retry_config
    assert isinstance(retry_config, RequestsStampede.config.AbstractRetryConfig)
    assert isinstance(retry_config, RequestsStampede.config.DefaultRetryConfig)
    assert isinstance(retry_config.retry_enabled, bool)
    assert isinstance(retry_config.backoff_enabled, bool)

    # Ensure retries and backoff delays are enabled
    assert retry_config.retry_enabled
    assert retry_config.backoff_enabled

    # Validate retry_config.retry_policy
    retry_policy = retry_config.retry_policy
    assert isinstance(retry_policy, RequestsStampede.policy.retry.AbstractRetryPolicy)
    assert isinstance(retry_policy, RequestsStampede.policy.retry.FixedRetryPolicy)
    assert isinstance(retry_policy.attempts, int)
    assert retry_policy.attempts == 5

    # Validate retry_config.backoff_policy
    backoff_policy = retry_config.backoff_policy
    assert isinstance(
        backoff_policy, RequestsStampede.policy.backoff.AbstractBackoffPolicy
    )
    assert isinstance(
        backoff_policy, RequestsStampede.policy.backoff.FibonacciBackoffPolicy
    )
    assert isinstance(backoff_policy.initial_delay, float)
    assert isinstance(backoff_policy.maximum_delay, float)
    assert backoff_policy.initial_delay == 0.0
    assert backoff_policy.maximum_delay == 144.0

    # Validate session
    assert retry_request_default.session is None

    # Validate logger
    assert isinstance(retry_request_default.logger, logging.Logger)


def test_retry_request_custom_parameters(retry_request_custom):
    """
    Ensures that a custom retry configuration passed to RetryRequest actually
    modifies the necessary instance parameters.
    """
    assert isinstance(retry_request_custom, RequestsStampede.horde.AbstractRetryRequest)
    assert isinstance(retry_request_custom, RequestsStampede.horde.RetryRequest)

    # Validate retry_config
    retry_config = retry_request_custom.retry_config
    assert isinstance(retry_config, RequestsStampede.config.AbstractRetryConfig)
    assert isinstance(retry_config, RequestsStampede.config.AggressiveRetryConfig)
    assert isinstance(retry_config.retry_enabled, bool)
    assert isinstance(retry_config.backoff_enabled, bool)

    # Ensure retries and backoff delays are enabled
    assert retry_config.retry_enabled
    assert retry_config.backoff_enabled

    # Validate retry_config.retry_policy
    retry_policy = retry_config.retry_policy
    assert isinstance(retry_policy, RequestsStampede.policy.retry.AbstractRetryPolicy)
    assert isinstance(retry_policy, RequestsStampede.policy.retry.InfiniteRetryPolicy)
    assert isinstance(retry_policy.attempts, float)
    assert retry_policy.attempts == math.inf

    # Validate retry_config.backoff_policy
    backoff_policy = retry_config.backoff_policy
    assert isinstance(
        backoff_policy, RequestsStampede.policy.backoff.AbstractBackoffPolicy
    )
    assert isinstance(
        backoff_policy, RequestsStampede.policy.backoff.RandomBackoffPolicy
    )
    assert isinstance(backoff_policy.minimum_delay, float)
    assert isinstance(backoff_policy.maximum_delay, float)
    assert backoff_policy.minimum_delay == 3.0
    assert backoff_policy.maximum_delay == 15.0

    # Validate session
    assert isinstance(retry_request_custom.session, requests.Session)

    # Validate logger
    assert isinstance(retry_request_custom.logger, logging.Logger)


def test_retry_session_default_parameters(retry_session_default):
    """
    Ensures that RetrySession default parameters are reasonable.
    """
    assert isinstance(
        retry_session_default, RequestsStampede.horde.AbstractRetryRequest
    )
    assert isinstance(retry_session_default, RequestsStampede.horde.RetryRequest)
    assert isinstance(retry_session_default, RequestsStampede.horde.RetrySession)

    # Validate retry_config
    retry_config = retry_session_default.retry_config
    assert isinstance(retry_config, RequestsStampede.config.AbstractRetryConfig)
    assert isinstance(retry_config, RequestsStampede.config.DefaultRetryConfig)
    assert isinstance(retry_config.retry_enabled, bool)
    assert isinstance(retry_config.backoff_enabled, bool)

    # Ensure retries and backoff delays are enabled
    assert retry_config.retry_enabled
    assert retry_config.backoff_enabled

    # Validate retry_config.retry_policy
    retry_policy = retry_config.retry_policy
    assert isinstance(retry_policy, RequestsStampede.policy.retry.AbstractRetryPolicy)
    assert isinstance(retry_policy, RequestsStampede.policy.retry.FixedRetryPolicy)
    assert isinstance(retry_policy.attempts, int)
    assert retry_policy.attempts == 5

    # Validate retry_config.backoff_policy
    backoff_policy = retry_config.backoff_policy
    assert isinstance(
        backoff_policy, RequestsStampede.policy.backoff.AbstractBackoffPolicy
    )
    assert isinstance(
        backoff_policy, RequestsStampede.policy.backoff.FibonacciBackoffPolicy
    )
    assert isinstance(backoff_policy.initial_delay, float)
    assert isinstance(backoff_policy.maximum_delay, float)
    assert backoff_policy.initial_delay == 0.0
    assert backoff_policy.maximum_delay == 144.0

    # Validate session
    assert isinstance(retry_session_default.session, requests.Session)

    # Validate logger
    assert isinstance(retry_session_default.logger, logging.Logger)


def test_retry_session_custom_parameters(retry_session_custom):
    """
    TODO
    """
    assert isinstance(retry_session_custom, RequestsStampede.horde.AbstractRetryRequest)
    assert isinstance(retry_session_custom, RequestsStampede.horde.RetryRequest)
    assert isinstance(retry_session_custom, RequestsStampede.horde.RetrySession)

    # Validate retry_config
    retry_config = retry_session_custom.retry_config
    assert isinstance(retry_config, RequestsStampede.config.AbstractRetryConfig)
    assert isinstance(retry_config, RequestsStampede.config.AggressiveRetryConfig)
    assert isinstance(retry_config.retry_enabled, bool)
    assert isinstance(retry_config.backoff_enabled, bool)

    # Ensure retries and backoff delays are enabled
    assert retry_config.retry_enabled
    assert retry_config.backoff_enabled

    # Validate retry_config.retry_policy
    retry_policy = retry_config.retry_policy
    assert isinstance(retry_policy, RequestsStampede.policy.retry.AbstractRetryPolicy)
    assert isinstance(retry_policy, RequestsStampede.policy.retry.InfiniteRetryPolicy)
    assert isinstance(retry_policy.attempts, float)
    assert retry_policy.attempts == math.inf

    # Validate retry_config.backoff_policy
    backoff_policy = retry_config.backoff_policy
    assert isinstance(
        backoff_policy, RequestsStampede.policy.backoff.AbstractBackoffPolicy
    )
    assert isinstance(
        backoff_policy, RequestsStampede.policy.backoff.RandomBackoffPolicy
    )
    assert isinstance(backoff_policy.minimum_delay, float)
    assert isinstance(backoff_policy.maximum_delay, float)
    assert backoff_policy.minimum_delay == 3.0
    assert backoff_policy.maximum_delay == 15.0

    # Validate session
    session = retry_session_custom.session
    assert isinstance(session, requests.Session)
    assert isinstance(session.headers, requests.structures.CaseInsensitiveDict)
    assert "User-Agent" in session.headers
    assert session.headers.get("User-Agent") == "RonSwanson/1.0"
    assert "Authorization" in session.headers
    assert session.headers.get("Authorization") == "Bearer ICanDoWhatIWant"

    # Validate logger
    assert isinstance(retry_session_custom.logger, logging.Logger)
