"""
TODO :)
"""


import time

import RequestsStampede.horde


def test_basic_get_failure():
    """
    Tests RequestsStampede.horde.RetryRequest.get()'s default behavior during
    request failures.
    """
    start_time = time.perf_counter()

    horde = RequestsStampede.horde.RetryRequest()

    response = horde.get("https://httpstat.us/500")

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    # The default retry configuration attempts 5 retries with fibonacci backoff
    # delays. As such, the elapsed time should be greater than 4 seconds:
    # sum([0, 1, 1, 2, 0])
    assert elapsed_time > 4.0
    assert response is None


def test_basic_options_failure():
    """
    Tests RequestsStampede.horde.RetryRequest.options()'s default behavior
    during request failures.
    """
    start_time = time.perf_counter()

    horde = RequestsStampede.horde.RetryRequest()

    response = horde.options("https://httpstat.us/500")

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    # The default retry configuration attempts 5 retries with fibonacci backoff
    # delays. As such, the elapsed time should be greater than 4 seconds:
    # sum([0, 1, 1, 2, 0])
    assert elapsed_time > 4.0
    assert response is None


def test_basic_head_failure():
    """
    Tests RequestsStampede.horde.RetryRequest.head()'s default behavior during
    request failures.
    """
    start_time = time.perf_counter()

    horde = RequestsStampede.horde.RetryRequest()

    response = horde.head("https://httpstat.us/500")

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    # The default retry configuration attempts 5 retries with fibonacci backoff
    # delays. As such, the elapsed time should be greater than 4 seconds:
    # sum([0, 1, 1, 2, 0])
    assert elapsed_time > 4.0
    assert response is None


def test_basic_post_failure():
    """
    Tests RequestsStampede.horde.RetryRequest.post()'s default behavior during
    request failures.
    """
    start_time = time.perf_counter()

    horde = RequestsStampede.horde.RetryRequest()

    response = horde.post("https://httpstat.us/500")

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    # The default retry configuration attempts 5 retries with fibonacci backoff
    # delays. As such, the elapsed time should be greater than 4 seconds:
    # sum([0, 1, 1, 2, 0])
    assert elapsed_time > 4.0
    assert response is None


def test_basic_put_failure():
    """
    Tests RequestsStampede.horde.RetryRequest.put()'s default behavior during
    request failures.
    """
    start_time = time.perf_counter()

    horde = RequestsStampede.horde.RetryRequest()

    response = horde.put("https://httpstat.us/500")

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    # The default retry configuration attempts 5 retries with fibonacci backoff
    # delays. As such, the elapsed time should be greater than 4 seconds:
    # sum([0, 1, 1, 2, 0])
    assert elapsed_time > 4.0
    assert response is None


def test_basic_patch_failure():
    """
    Tests RequestsStampede.horde.RetryRequest.patch()'s default behavior during
    request failures.
    """
    start_time = time.perf_counter()

    horde = RequestsStampede.horde.RetryRequest()

    response = horde.patch("https://httpstat.us/500")

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    # The default retry configuration attempts 5 retries with fibonacci backoff
    # delays. As such, the elapsed time should be greater than 4 seconds:
    # sum([0, 1, 1, 2, 0])
    assert elapsed_time > 4.0
    assert response is None


def test_basic_delete_failure():
    """
    Tests RequestsStampede.horde.RetryRequest.delete()'s default behavior during
    request failures.
    """
    start_time = time.perf_counter()

    horde = RequestsStampede.horde.RetryRequest()

    response = horde.delete("https://httpstat.us/500")

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    # The default retry configuration attempts 5 retries with fibonacci backoff
    # delays. As such, the elapsed time should be greater than 4 seconds:
    # sum([0, 1, 1, 2, 0])
    assert elapsed_time > 4.0
    assert response is None
