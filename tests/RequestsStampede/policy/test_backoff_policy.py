# pylint: disable=redefined-outer-name
"""
TODO
"""


import math
import statistics

import pytest
import scipy.stats

import RequestsStampede.policy.backoff


@pytest.fixture
def fixed_backoff_policy():
    """
    TODO
    """
    return RequestsStampede.policy.backoff.FixedBackoffPolicy()


@pytest.fixture
def random_backoff_policy():
    """
    TODO
    """
    return RequestsStampede.policy.backoff.RandomBackoffPolicy()


@pytest.fixture
def fibonacci_backoff_policy():
    """
    TODO
    """
    return RequestsStampede.policy.backoff.FibonacciBackoffPolicy()


def test_fixed_backoff_policy_default_parameters(fixed_backoff_policy):
    """
    Ensures that the default backoff policy has reasonable default parameters.
    """
    assert isinstance(
        fixed_backoff_policy, RequestsStampede.policy.backoff.AbstractBackoffPolicy
    )

    assert isinstance(fixed_backoff_policy.constant_delay, float)
    assert fixed_backoff_policy.constant_delay == 5.0


def test_fixed_backoff_policy_delay_sequence(fixed_backoff_policy):
    """
    TODO
    """
    for _ in range(1000):
        assert next(fixed_backoff_policy.delay()) == 5.0


def test_random_backoff_policy_default_parameters(random_backoff_policy):
    """
    Ensures that the random backoff policy has reasonable defaults and yields
    a statistically verifiable uniform random distribution.
    """
    assert isinstance(
        random_backoff_policy, RequestsStampede.policy.backoff.AbstractBackoffPolicy
    )

    assert isinstance(random_backoff_policy.minimum_delay, float)
    assert isinstance(random_backoff_policy.maximum_delay, float)
    assert random_backoff_policy.minimum_delay == 3.0
    assert random_backoff_policy.maximum_delay == 15.0


def test_random_backoff_policy_delay_sequence(random_backoff_policy):
    """
    TODO
    """
    sample_size = 10000
    sample = []

    for _ in range(sample_size):
        delay = next(random_backoff_policy.delay())

        sample.append(delay)

        assert isinstance(delay, float)

        assert delay >= random_backoff_policy.minimum_delay
        assert delay <= random_backoff_policy.maximum_delay

    sample_mean = statistics.mean(sample)
    sample_stddev = statistics.stdev(sample)

    print(f"Sample Size    = { sample_size }")
    print(f"Sample Mean    = { sample_mean }")
    print(f"Sample Std Dev = { sample_stddev }")

    population_mean = (
        random_backoff_policy.minimum_delay + random_backoff_policy.maximum_delay
    ) / 2
    population_variance = (
        (random_backoff_policy.maximum_delay - random_backoff_policy.minimum_delay) ** 2
    ) / 12
    population_stddev = math.sqrt(population_variance)

    print(f"Population Mean     = { population_mean }")
    print(f"Population Variance = { population_variance }")
    print(f"Population Std Dev  = { population_stddev }")

    # Z-Test
    z_score = (sample_mean - population_mean) / (
        population_stddev / math.sqrt(sample_size)
    )

    print(f"Z Score = { z_score }")

    # P-value
    p_value_one_side = scipy.stats.norm.sf(abs(z_score))
    # p_value_two_side = p_value_one_side ** 2

    print(f"P Value (One Side) = { p_value_one_side }")
    # print(f'P Value (Two Side) = { p_value_two_side }')

    confidence_interval = sample_stddev / math.sqrt(sample_size)
    confidence = 1 - confidence_interval

    print(f"Confidence Interval = { confidence_interval }")
    print(f"Confidence          = { confidence }")

    acceptable_confidence = 0.95

    assert confidence >= acceptable_confidence


def test_fibonacci_backoff_policy_default_parameters(fibonacci_backoff_policy):
    """
    Ensures that the fibonacci backoff policy has reasonable defaults and yield
    an accurate fibonacci sequence.
    """
    assert isinstance(
        fibonacci_backoff_policy, RequestsStampede.policy.backoff.AbstractBackoffPolicy
    )

    assert isinstance(fibonacci_backoff_policy.initial_delay, float)
    assert isinstance(fibonacci_backoff_policy.maximum_delay, float)
    assert fibonacci_backoff_policy.initial_delay == 0.0
    assert fibonacci_backoff_policy.maximum_delay == 144.0


def test_fibonacci_backoff_policy_delay_sequence(fibonacci_backoff_policy):
    """
    TODO
    """
    expected_fibonacci_sequence = [
        0.0,
        1.0,
        1.0,
        2.0,
        3.0,
        5.0,
        8.0,
        13.0,
        21.0,
        34.0,
        55.0,
        89.0,
        144.0,
        144.0,
        144.0,
        144.0,
        144.0,
    ]

    backoff_generator = fibonacci_backoff_policy.delay()

    for fibonacci in expected_fibonacci_sequence:
        delay = next(backoff_generator)

        assert isinstance(delay, float)
        assert delay == fibonacci
