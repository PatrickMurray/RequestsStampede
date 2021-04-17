"""
Build-in retry policies and their abstract class.
"""


import abc
import typing
import math

import RequestsStampede.exceptions


class AbstractRetryPolicy(abc.ABC):
    """
    An abstract class for use in implementing retry policies.
    """

    attempts: int


class FixedRetryPolicy(AbstractRetryPolicy):
    """
    Establishes a constant retry policy.
    """

    def __init__(self, attempts: typing.Optional[int] = 5):
        """
        A basic constructor.

        :param attempts: The number of request retries to be attempted.

        :type attempts: int
        """
        assert isinstance(attempts, int)
        assert attempts > 0

        self.attempts = attempts

    def __repr__(self):
        return "<{}.{} object at {} attempts={}>".format(
            __class__.__module__,
            __class__.__name__,
            hex(id(self)),
            self.attempts,
        )


class InfiniteRetryPolicy(AbstractRetryPolicy):
    """
    Establishes an infinite retry policy.
    """

    def __init__(self):
        """
        A basic constructor that takes no parameters.
        """
        self.attempts = math.inf

    def __repr__(self):
        return "<{}.{} object at {} attempts={}>".format(
            __class__.__module__,
            __class__.__name__,
            hex(id(self)),
            self.attempts,
        )


class ConditionalRetryPolicy(AbstractRetryPolicy):
    """
    Establishes a conditional retry policy.

    Not Implemented.
    """

    def __init__(self):
        raise NotImplementedError


class CustomRetryPolicy(AbstractRetryPolicy):
    """
    Establishes a custom file-based retry policy.
    """

    def __init__(self, policy: dict):
        """
        Provided a policy definition, initializes a custom retry policy based
        on the parameters defined therein.

        Example policies:

        {
            "type": "fixed"
            "attempts" 10
        }

        {
            "type": "infinite"
        }

        :param policy: A retry policy definition.

        :type policy: dict
        """

        policy_type = policy.get("type").lower()

        if policy_type == "fixed":
            attempts = policy.get("attempts")

            assert isinstance(attempts, int)
            assert attempts > 0

            self.attempts = attempts
        elif policy_type == "infinite":
            self.attempts = math.inf
        else:
            raise RequestsStampede.exceptions.InvalidCustomRetryPolicy(policy_type)

    def __repr__(self):
        return "<{}.{} object at {} attempts={}>".format(
            __class__.__module__,
            __class__.__name__,
            hex(id(self)),
            self.attempts,
        )
