"""
Built-in backoff policies and their abstract class.
"""


import abc
import typing
import random

import RequestsStampede.exceptions


class AbstractBackoffPolicy(abc.ABC):
    """
    An abstract class for use in implementing backoff policies.
    """

    @abc.abstractmethod
    def delay(self) -> typing.Iterable[float]:
        """
        All backoff policies will be interfaced via their .delay() method which
        returns a generator iterable which yields floats. These float values
        are the desired backoff delay, measured in seconds, to be added after
        an unsuccessful request attempt.

        :return: A generator of floats.
        :rtype: typing.Iterable[float]
        """


class FixedBackoffPolicy(AbstractBackoffPolicy):
    """
    Establishes constant backoff delay.
    """

    def __init__(self, delay: typing.Optional[float] = 5.0):
        """
        A basic constructor.

        :param delay: The constant delay to be attempted after every failed
                      request attempt.

        :type delay: float
        """
        assert isinstance(delay, float)
        assert delay >= 0.0

        self.constant_delay = delay

    def delay(self) -> typing.Iterable[float]:
        """
        Returns the backoff delay generator.

        :return: A generator of floats.
        :rtype: typing.Iterable[float]
        """
        while True:
            yield self.constant_delay

    def __repr__(self):
        return "<{}.{} object at {} constant_delay={}>".format(
            __class__.__module__,
            __class__.__name__,
            hex(id(self)),
            self.constant_delay,
        )


class RandomBackoffPolicy(AbstractBackoffPolicy):
    """
    Establishes a random and uniformly distributed backoff delay between two
    values.
    """

    def __init__(
        self,
        minimum_delay: typing.Optional[float] = 3.0,
        maximum_delay: typing.Optional[float] = 15.0,
    ):
        """
        A basic constructor.

        :param minimum_delay: The lower bound for the randomly generated delay.
        :param maximum_delay: THe upper bound for the randomly generated delay.

        :type minimum_delay: float
        :type maximum_delay: float
        """
        assert isinstance(minimum_delay, float)
        assert isinstance(maximum_delay, float)
        assert minimum_delay >= 0.0
        assert maximum_delay > minimum_delay

        self.minimum_delay = minimum_delay
        self.maximum_delay = maximum_delay

    def delay(self) -> typing.Iterable[float]:
        """
        Returns the backoff delay generator.

        :return: A generator of floats.
        :rtype: typing.Iterable[float]
        """
        while True:
            yield random.uniform(self.minimum_delay, self.maximum_delay)

    def __repr__(self):
        return "<{}.{} object at {} minimum_delay={} maximum_delay={}>".format(
            __class__.__module__,
            __class__.__name__,
            hex(id(self)),
            self.minimum_delay,
            self.maximum_delay,
        )


class FibonacciBackoffPolicy(AbstractBackoffPolicy):
    """
    Estabilishes a fibonacci-sequence backoff delay that grows, to a
    configurable upper bound, progressively as consecutive request attempts
    fail.
    """

    initial_delay: float
    maximum_delay: float

    def __init__(
        self,
        initial_delay: typing.Optional[float] = 0.0,
        maximum_delay: typing.Optional[float] = 144.0,
    ):
        """
        A basic constructor.

        :param initial_delay: The initial digit of the psuedo-fibonacci
                              sequence. For example, and initial delay of 3
                              would result in a sequence of: 3, 4, 7, 11, etc.
        :param maximum_delay: The maximum permissible delay. If the sequence
                              goes beyond this value, the sequence will be
                              ignored and the maximum delay returned instead.

        :type initial_delay: float
        :type maximum_delay: float
        """
        assert isinstance(initial_delay, float)
        assert isinstance(maximum_delay, float)
        assert maximum_delay > initial_delay

        self.initial_delay = initial_delay
        self.maximum_delay = maximum_delay

    def delay(self) -> typing.Iterable[float]:
        """
        Returns the backoff delay generator.

        :return: A generator of floats.
        :rtype: typing.Iterable[float]
        """
        fib_curr = self.initial_delay
        fib_next = self.initial_delay + 1.0

        while True:
            if fib_curr <= self.maximum_delay:
                yield fib_curr
            else:
                yield self.maximum_delay

            # Increment Sequence
            tmp = fib_curr
            fib_curr = fib_next
            fib_next += tmp

    def __repr__(self):
        return "<{}.{} object at {} initial_delay={} maximum_delay={}>".format(
            __class__.__module__,
            __class__.__name__,
            hex(id(self)),
            self.initial_delay,
            self.maximum_delay,
        )


class CustomBackoffPolicy(AbstractBackoffPolicy):
    """
    Establishes a custom file-based backoff policy.
    """

    _policy: AbstractBackoffPolicy

    def __init__(self, policy: dict):
        """
        Provided a policy definition, initializes a custom backoff policy based
        on the parameters defined therein.

        Example policies:

        {
            "type": "fixed",
            "delay": 5.0
        }

        {
            "type": "random",
            "minimum_delay": 5.0,
            "maximum_delay": 45.0
        }

        {
            "type": "fibonacci",
            "initial_delay": 3.0,
            "maximum_delay": 90.0
        }

        :param policy:

        :type policy:
        """

        policy_type = policy.get("type").lower()

        if policy_type == "fixed":
            delay = policy.get("delay")

            assert isinstance(delay, float)

            assert delay > 0.0

            self._policy = FixedBackoffPolicy(delay=delay)
        elif policy_type == "random":
            minimum_delay = policy.get("minimum_delay")
            maximum_delay = policy.get("maximum_delay")

            assert isinstance(minimum_delay, float)
            assert isinstance(maximum_delay, float)

            assert minimum_delay > 0.0
            assert maximum_delay > 0.0
            assert maximum_delay > minimum_delay

            self._policy = RandomBackoffPolicy(
                minimum_delay=minimum_delay, maximum_delay=maximum_delay
            )
        elif policy_type == "fibonacci":
            initial_delay = policy.get("initial_delay")
            maximum_delay = policy.get("maximum_delay")

            assert isinstance(initial_delay, float)
            assert isinstance(maximum_delay, float)

            assert initial_delay > 0.0
            assert maximum_delay > 0.0
            assert maximum_delay > initial_delay

            self._policy = FibonacciBackoffPolicy(
                initial_delay=initial_delay, maximum_delay=maximum_delay
            )
        else:
            raise RequestsStampede.exceptions.InvalidCustomBackoffPolicy(policy_type)

    def delay(self) -> typing.Iterable[float]:
        """
        Returns the backoff delay generator.

        :return: A generator of floats.
        :rtype: typing.Iterable[float]
        """
        return self._policy.delay()
