"""
Defines abstract retry configuration models and sane (and aggressive) default
configuration values.
"""


import pathlib
import abc
import typing

import schema
import yaml

import RequestsStampede.exceptions
import RequestsStampede.policy.retry
import RequestsStampede.policy.backoff


class AbstractRetryConfig(abc.ABC):
    """
    The AbstractRetryConfig class is used throughout the RequestsStampede
    package to encapsulate the desired retry and backoff delay behavior.
    """

    retry_enabled: bool
    retry_policy: RequestsStampede.policy.retry.AbstractRetryPolicy

    backoff_enabled: bool
    backoff_policy: RequestsStampede.policy.backoff.AbstractBackoffPolicy

    def __init__(
        self,
        retry_enabled: typing.Optional[bool] = True,
        retry_policy: typing.Optional[
            RequestsStampede.policy.retry.AbstractRetryPolicy
        ] = None,
        backoff_enabled: typing.Optional[bool] = True,
        backoff_policy: typing.Optional[
            RequestsStampede.policy.backoff.AbstractBackoffPolicy
        ] = None,
    ):
        """
        A basic constructor for the object.

        :param retry_enabled: Whether or not request retries should be
                              attempted.
        :param retry_policy: An AbstractRetryPolicy object outlining the
                             desired request retry behavior.
        :param backoff_enabled: Whether or not a backoff delay should be
                                inserted after failed requests, prior to their
                                retry.
        :param backoff_policy: An AbstractBackoffPolicy object outlining the
                               desired backoff delay behavior.

        :type retry_enabled: bool
        :type retry_policy: RequestsStampede.policy.retry.AbstractRetryPolicy
        :type backoff_enabled: bool
        :type backoff_policy: RequestsStampede.policy.backoff.AbstractBackoffPolicy
        """

        if retry_enabled:
            self.retry_enabled = retry_enabled

        if retry_policy:
            self.retry_policy = retry_policy

        if backoff_enabled:
            self.backoff_enabled = backoff_enabled

        if backoff_policy:
            self.backoff_policy = backoff_policy

    def __repr__(self):
        return (
            "<{}.{} object at {} retry_enabled={} retry_policy={} "
            "backoff_enabled={} backoff_policy={}>"
        ).format(
            __class__.__module__,
            __class__.__name__,
            hex(id(self)),
            self.retry_enabled,
            self.retry_policy,
            self.backoff_enabled,
            self.backoff_policy,
        )


class DefaultRetryConfig(AbstractRetryConfig):
    """
    The default retry configuration uses a fixed retry policy, with a maximum
    of 5 retry attempts, and a fibonacci based backoff delay policy. For
    example, the intend request sequence will be as follows:

    Event | Title                  | Status
    ------|------------------------|--------
    0     | Request Attempt #1     | Failure
    1     | Backoff Delay: 0.0 sec |
    2     | Request Attempt #2     | Failure
    3     | Backoff Delay: 1.0 sec |
    4     | Request Attempt #3     | Failure
    5     | Backoff Delay: 1.0 sec |
    6     | Request Attempt #4     | Failure
    7     | Backoff Delay: 2.0 sec |
    8     | Request Attempt #5     | Failure
    """

    retry_policy = RequestsStampede.policy.retry.FixedRetryPolicy()
    backoff_policy = RequestsStampede.policy.backoff.FibonacciBackoffPolicy()


class RelaxedRetryConfig(DefaultRetryConfig):
    """
    Intended to be a more relaxed version of the default retry configuration.
    At the moment, the relaxed retry configuration is identical to the default
    configuration; however, this may change in the future.
    """

    backoff_policy = RequestsStampede.policy.backoff.FibonacciBackoffPolicy()


class AggressiveRetryConfig(AbstractRetryConfig):
    """
    The aggressive retry configuration is intended to prioritize receiving a
    successful HTTP response; rather, than prioritizing the stability of the
    upstream resource being requested.

    The usage of this retry configuration should be discouraged.

    The aggressive retry configuration will attempt a provided request
    indefinitely until a successful HTTP response is received. Furthermore, the
    backoff delay policy is fixed - a constant 5 second backoff delay will be
    inserted following all unsuccessful requests.
    """

    retry_policy = RequestsStampede.policy.retry.InfiniteRetryPolicy()
    backoff_policy = RequestsStampede.policy.backoff.FixedBackoffPolicy()


class CustomRetryConfig(DefaultRetryConfig):
    """
    A wrapper class around the default retry configuration wherein custom
    configuration files will be instantiated.
    """


def load() -> AbstractRetryConfig:
    """
    Determines the default behavior of RequestsStampede. If a configuration
    file is located, the contents of that file are parsed and returned. If no
    configuration file is located, the default retry configuration is returned.

    :return: A default, environment specific, retry configuration object.
    :rtype: AbstractRetryConfig
    """
    config_path = resolve_path()

    if config_path is not None:
        return parse(config_path)

    return DefaultRetryConfig()


def resolve_path(filename: str = "stampede.yml") -> pathlib.Path:
    """
    Attempts to locate a retry configuration in the file-system. If a file with
    the provided filename exists within the current working directory, a path
    to that file will be returned. If the file does not exist within the
    current directory, each parent directory will be inspected for a file of
    the same filename - returning a path to the first existing file
    encountered. If the root directory is reached without a result, the $HOME
    directory will be inspected. If the filename does not exist there, a None
    value will be returned.

    Example: Runtime CWD = /etc/application/

    1) /etc/application/stampede.yml
    2) /etc/stampede.yml
    3) /stampede.yml
    4) $HOME/stampede.yml

    :param filename: The expected retry configuration filename

    :type filename: str

    :return: A retry configuration file path, or None if none located.
    :rtype: pathlib.Path
    """

    # Begin at the current working directory
    dir_path = pathlib.Path.cwd()

    # Parent directory loop
    while True:
        file_path = dir_path / filename

        # If the file exists, return its path
        if file_path.is_file():
            return file_path

        # If we're at the root directory (i.e. both current dir and parent are
        # the same), than break out of the parent directory loop
        if dir_path == dir_path.parent:
            break

        # Examine the parent directory
        dir_path = dir_path.parent

    # Since a file has not been located yet, examine the effective user's home
    # directory
    dir_path = pathlib.Path.home()
    file_path = dir_path / filename

    if file_path.is_file():
        return file_path

    return None


def parse(path: pathlib.Path = None) -> CustomRetryConfig:
    """
    Parses the provided retry configuration path and returns an initialized
    CustomRetryConfig object.

    :param path: A retry configuration file path.

    :type path: pathlib.Path

    :return: An initialized CustomRetryConfig object.
    :rtype: CustomRetryConfig
    """

    # Define the retry configuration file schema
    config_schema = schema.Schema(
        {
            "retry_config": {
                schema.Optional("retry_enabled", default=True): bool,
                schema.Optional("retry_policy"): schema.Or(
                    {"type": "fixed", "attempts": int},
                    {"type": "infinite"},
                    only_one=True,
                ),
                schema.Optional("backoff_enabled", default=True): bool,
                schema.Optional("backoff_policy"): schema.Or(
                    {"type": "fixed", "delay": float},
                    {"type": "random", "minimum_delay": float, "maximum_delay": float},
                    {
                        "type": "fibonacci",
                        "initial_delay": float,
                        "maximum_delay": float,
                    },
                    only_one=True,
                ),
            }
        }
    )

    with open(path) as handler:
        config_dict = yaml.safe_load(handler)

        # Validate the configuration file
        try:
            config_schema.validate(config_dict)
        except schema.SchemaError as e:
            raise RequestsStampede.exceptions.InvalidRetryConfigFile(path, e)

        # Retrieve retry configuration values
        retry_config = config_dict.get("retry_config")

        retry_enabled = retry_config.get("retry_enabled")
        retry_policy = retry_config.get("retry_policy")
        backoff_enabled = retry_config.get("backoff_enabled")
        backoff_policy = retry_config.get("backoff_policy")

        # Build retry policies
        custom_retry_policy = RequestsStampede.policy.retry.CustomRetryPolicy(
            retry_policy
        )
        custom_backoff_policy = RequestsStampede.policy.backoff.CustomBackoffPolicy(
            backoff_policy
        )

        # Assemble final custom retry configuration
        return CustomRetryConfig(
            retry_enabled=retry_enabled,
            retry_policy=custom_retry_policy,
            backoff_enabled=backoff_enabled,
            backoff_policy=custom_backoff_policy,
        )
