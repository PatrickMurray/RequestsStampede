# pylint: disable=redefined-outer-name

"""
TODO
"""


import math

import pytest

import RequestsStampede.policy.retry


@pytest.fixture
def fixed_retry_policy():
    """
    TODO
    """
    return RequestsStampede.policy.retry.FixedRetryPolicy()


@pytest.fixture
def infinite_retry_policy():
    """
    TODO
    """
    return RequestsStampede.policy.retry.InfiniteRetryPolicy()


@pytest.fixture
def conditional_retry_policy():
    """
    TODO
    """


def test_fixed_retry_policy_default_parameters(fixed_retry_policy):
    """
    Ensures that the fixed retry policy has reasonable default parameters.
    """
    assert isinstance(
        fixed_retry_policy, RequestsStampede.policy.retry.AbstractRetryPolicy
    )

    assert isinstance(fixed_retry_policy.attempts, int)
    assert fixed_retry_policy.attempts == 5


def test_infinite_retry_policy_default_parameters(infinite_retry_policy):
    """
    Ensures that the infinite retry policy is actually infinite.
    """
    assert isinstance(
        infinite_retry_policy, RequestsStampede.policy.retry.AbstractRetryPolicy
    )

    assert isinstance(infinite_retry_policy.attempts, float)
    assert infinite_retry_policy.attempts == math.inf


def test_conditional_retry_policy_default_parameters():
    """
    Ensures that the conditional retry policy has not been implemented.
    """
    try:
        RequestsStampede.policy.retry.ConditionalRetryPolicy()
    except NotImplementedError as e:
        assert isinstance(e, NotImplementedError)
    else:
        assert False
