"""
Internal models used within the RequestsStampede package.
"""


import typing
import logging
import math

import requests
import requests.exceptions

import RequestsStampede.config
import RequestsStampede.exceptions


module_logger = logging.getLogger(__name__)


class RequestParameters:
    """
    The goal of the RequestParameters model is to encapsulate all end-user
    parameters passed into the HTTP method wrapper functions in both the
    RetryRequest or RetrySession classes,
    """

    http_method: str
    url: str
    session: requests.Session
    kwargs: dict

    def __init__(
        self, http_method: str, url: str, session: requests.Session, kwargs: dict
    ):
        """
        A basic constructor for assigning instance object parameters.

        :param http_method: The desired request's HTTP verb (i.e. GET).
        :param url: The desired resource to request.
        :param session: A requests.Session object to use for the request.
        :param kwargs: Additional requests specific parameters to pass through.

        :type http_method: str
        :type url: str
        :type session: requests.Session
        :type kwargs: dict
        """

        self.http_method = http_method
        self.url = url
        self.session = session
        self.kwargs = kwargs

    def __repr__(self):
        return "<{}.{} object at {} http_method={} url={} session={} kwargs={}>".format(
            __class__.__module__,
            __class__.__name__,
            hex(id(self)),
            self.http_method,
            self.url,
            self.session,
            self.kwargs,
        )


class RequestAttemptSequence:
    """
    The RequestAttemptSequence class' goal is to generate a sequence,
    potentially infinite in length, of RequestAttempt objects. The resulting
    RequestAttempt objects will comply with the provided retry configuration
    (i.e. retry attempts, backoff delay, etc).
    """

    request_parameters: RequestParameters
    retry_config: RequestsStampede.config.AbstractRetryConfig

    def __init__(
        self,
        request_parameters: RequestParameters,
        retry_config: RequestsStampede.config.AbstractRetryConfig,
    ):
        """
        A basic constructor for parameters that will be necessary to generate
        an iterable sequence of RequestAttempt objects.

        :param request_parameters: Parameters detailing the desired request.
        :param retry_config: The retry configuration to be followed when
                             generating a request sequence.

        :type request_parameters: RequestsStampede.models.RequestParameters
        :type retry_config: RequestsStampede.config.AbstractRetryConfig
        """

        self.request_parameters = request_parameters
        self.retry_config = retry_config

    def attempts(self) -> typing.Iterator:
        """
        Returns a generator that yields RequestAttempt objects that can be
        executed within RequestsStampede.horde.RetryRequest or RetrySession.

        :return: A generator function the yields a RequestAttempt object in
                 compliance to the provided retry configuration.
        :rtype: Generator[RequestsStampede.models.RequestAttempt]
        """

        attempts_maximum = self.retry_config.retry_policy.attempts
        backoff_generator = self.retry_config.backoff_policy.delay()

        def __attempt_generator(attempt_num: int):
            """
            Generates a RequestAttempt object in compliance with the parent
            instance's retry configuration and policies.

            :param attempt_num: The request attempt's position with respect to
                                all prior attempts. Starting at 1 and
                                increasing.

            :type attempt_num: int

            :return: A request attempt object to be executed
            :rtype: RequestsStampede.models.RequestAttempt
            """
            backoff = None

            # If request retry attempts are disabled, do not return anything.
            # This case will be caught below and used to terminate the
            # generator
            if not self.retry_config.retry_enabled:
                return None

            # Likewise, if backoff delays are enabled and the request attempt
            # is below the maximum number of request retries (math.inf if
            # infinite), then we will fetch the backoff delay from the backoff
            # generator
            if self.retry_config.backoff_enabled:
                if attempt_num < attempts_maximum:
                    backoff = next(backoff_generator)

            return RequestAttempt(self.request_parameters, attempt_num, backoff)

        # If the RequestsStampede.policy.retry.InfiniteRetryPolicy is used, the
        # generator will continue forever
        if attempts_maximum == math.inf:
            attempt_num = 1
            while True:
                attempt = __attempt_generator(attempt_num)

                # Catch instances where retry_enabled may be disabled in the
                # configuration
                if attempt is None:
                    return

                yield attempt
                attempt_num += 1
        else:
            # Otherwise, the maximum number of attempts is finite.
            for attempt_num in range(1, attempts_maximum + 1):
                attempt = __attempt_generator(attempt_num)

                # Catch instances where retry_enabled may be disabled in the
                # configuration
                if attempt is None:
                    return

                yield attempt

    def __repr__(self):
        return "<{}.{} object at {} request_parameters={} retry_config={}>".format(
            __class__.__module__,
            __class__.__name__,
            hex(id(self)),
            self.request_parameters,
            self.retry_config,
        )


class RequestAttempt:
    """
    A data model for storing all details surrounding a request attempt and it's
    execution. The RequestAttempt class contains all the information necessary
    to execute a request, including the request parameters as well as useful
    metadata such as the attempt number and desired backoff delay. When
    executed, the class will store the request's response.

    TODO - Add response time monitoring.
    """

    request: requests.Request
    session: requests.Session
    response: requests.Response

    attempt: int
    backoff: float

    def __init__(
        self,
        request_parameters: RequestParameters,
        attempt: typing.Optional[int] = None,
        backoff: typing.Optional[float] = None,
    ):
        """
        A basic constructor.

        :param request_parameters: The potential request to be executed.
        :param attempt: The request's attempt number.
        :param backoff: The desired request backoff delay.

        :type request_parameters: RequestsStampede.models.RequestParameters
        :type attempt: int
        :type backoff: float
        """

        self.request_parameters = request_parameters

        self.request = requests.Request(
            request_parameters.http_method,
            request_parameters.url,
            **request_parameters.kwargs
        )

        self.session = request_parameters.session
        self.response = None

        self.attempt = attempt
        self.backoff = backoff

    def execute(self) -> requests.Response:
        """
        Executes the request attempt.

        :return: The request's response.
        :rtype: requests.Response
        """

        prepared_request = self.session.prepare_request(self.request)

        response = self.session.send(prepared_request)

        self.response = response

        return response

    def __repr__(self):
        return (
            "<{}.{} object at {} request={} session={} response={} attempt={} "
            "backoff={}>"
        ).format(
            __class__.__module__,
            __class__.__name__,
            hex(id(self)),
            self.request,
            self.session,
            self.response,
            self.attempt,
            self.backoff,
        )
