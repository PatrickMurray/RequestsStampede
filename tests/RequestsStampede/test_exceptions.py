# pylint: disable=redefined-outer-name

"""
Tests RequestsStampede built-in exceptions.
"""


import pytest

import RequestsStampede.exceptions


@pytest.fixture
def unsuccessful_request_attempt_exception():
    """
    TODO
    """
    return RequestsStampede.exceptions.UnsuccessfulRequestAttemptException()


def test_unsuccessful_request_attempt_exception(unsuccessful_request_attempt_exception):
    """
    Ensures that the UnsuccessfulRequestAttemptException functions properly.
    """
    assert isinstance(unsuccessful_request_attempt_exception, Exception)
