"""
The main source code for the RequestsStampede package: contains the
RetryRequest and RetrySession wrapper classes that provide interfaces to invoke
HTTP GET, OPTIONS, HEAD, POST, PUT, PATCH, and DELETE requests.
"""


import abc
import typing
import logging
import time

import requests
import requests.exceptions

import RequestsStampede.config
import RequestsStampede.models
import RequestsStampede.exceptions


module_logger = logging.getLogger(__name__)


class AbstractRetryRequest(abc.ABC):
    """
    The AbstractRetryRequest object Provides a base constructor interface for
    use by the RetryRequest and RetrySession classes.
    """

    retry_config: RequestsStampede.config.AbstractRetryConfig
    session: requests.Session
    logger: logging.Logger

    def __init__(
        self,
        retry_config: typing.Optional[
            RequestsStampede.config.AbstractRetryConfig
        ] = None,
        session: typing.Optional[requests.Session] = None,
    ):
        """
        Default constructor for the RequestsStampede wrapper. Intended to be
        invoked by end-users within their source code prior to calling the HTTP
        verb wrappers implemented in RetryRequest below.

        :param retry_config: The retry configuration that RetryRequest or
                             RetrySession shall comply with.
        :param session: A requests Session object that shall be shared among
                        all transmitted HTTP requests.

        :type retry_config: RequestsStampede.config.AbstractRetryConfig
        :type session: requests.Session

        :type retry_config: RequestsStampede.config.AbstractRetryConfig
        :type session: requests.Session
        """

        if retry_config:
            self.retry_config = retry_config

        if session:
            self.session = session

        self.logger = module_logger


class RetryRequest(AbstractRetryRequest):
    """
    The RetryRequest object provides wrapper functions that intend to mimic the
    high-level behavior of the requests and requests.Session classes. The
    following HTTP methods have been implemented:
      - GET
      - OPTIONS
      - HEAD
      - POST
      - PUT
      - PATCH
      - DELETE

    As is the case with requests' implementation for these HTTP methods, a URL
    is the only required argument - all other parameters are passed through to
    an underlying requests.Request object in the form of a keyword argument
    (kwarg). Parameter interoperability is intended; however, thorough test
    coverage of all of the requests package's parameters is not feasible. If
    any bugs or lapses in feature functionality are discovered, please document
    and report your findings in a Github Issue:

    https://github.com/PatrickMurray/RequestsStampede/issues/new
    """

    retry_config = RequestsStampede.config.load()
    session = None
    logger = module_logger.getChild("RetryRequest")

    def _request_handler(
        self, http_method: str, url: str, kwargs: dict
    ) -> requests.Response:
        """
        An internal function to make a best-effort attempt at transmitting the
        desired HTTP request in compliance with the established retry
        configuration. This is accomplished via the following steps:

        1) Input arguments are incapsulated within a
           RequestsStampede.models.RequestParameters object for ease of use
           throughout the codebase.

        2) An iterator attempt sequence object is constructed in accordance to
           the provided retry configuration using the
           RequestsStampede.models.RequestAttemptSequence class. Depending on
           the retry configuration, a request will be attempeted a certain
           number of times (or only once if desired) and a backoff delay will
           be inserted between request attempts to reduce the impact on the
           requested resource.

        3) Finally, request attempts will begin to be executed. If a request's
           response status code is satisfactory, the request's
           requests.Response object will be returned. If the request was
           unsuccessful, a backoff delay will be inserted (if enabled) and
           subsequenct request attempts will be invoked.

        :param http_method: The desired HTTP method for the request (i.e. GET).
        :param url: The desired resource to request.
        :param kwargs: Additional keyword arguments to be provided to
                       requests.Request

        :type http_method: str
        :type url: str
        :type kwargs: dict

        :return: Upon the first successful request, its requests.Response
                 object will be returned. If all request attempts are
                 unsuccessful, None will be returned.
        :rtype: requests.Response
        """

        # Wrap requests parameters in a model to make passing them around
        # simpler
        request_parameters = RequestsStampede.models.RequestParameters(
            http_method=http_method,
            url=url,
            session=self._request_session(),
            kwargs=kwargs,
        )

        self.logger.info("Attempting to fulfill request: %r", request_parameters)

        # Construct a sequence of requests that may be transmitted in the event
        # of consecutive request failures
        attempt_sequence = RequestsStampede.models.RequestAttemptSequence(
            request_parameters, self.retry_config
        )

        # Begin attempting requests on the desired resource
        for attempt in attempt_sequence.attempts():
            try:
                self.logger.debug("Executing request attempt: %r", attempt)

                # Execute request
                response = attempt.execute()

                self.logger.debug("Request response received: %r", response)

                # Check response status code
                if response.ok:
                    self.logger.info("Request respone successful: %r", response)
                    return response

                self.logger.warning("Request response unsuccessful: %r", response)
                raise RequestsStampede.exceptions.UnsuccessfulRequestAttemptException(
                    attempt
                )
            except (
                requests.exceptions.RequestException,
                RequestsStampede.exceptions.UnsuccessfulRequestAttemptException,
            ) as exception:
                self.logger.info("Caught unsuccessful request attempt: %r", attempt)
                self.logger.debug("Request exception = %r", exception)

                if attempt.backoff is not None:
                    self.logger.info(
                        "Backoff delay enabled, inserting a %r second delay between request "
                        "attempts",
                        attempt.backoff,
                    )

                    # Insert backoff delay between request attempts
                    time.sleep(attempt.backoff)

                    self.logger.info(
                        "Backoff delay complete, proceeding with next request attempt"
                    )
                else:
                    self.logger.info(
                        "Backoff delay disabled, proceeding immediately with next request attempt"
                    )

        self.logger.error("Unable to fulfill request: %r", request_parameters)

        return None

    def _request_session(self) -> requests.Session:
        """
        Returns a requests.Session object for use in the invokation of an HTTP
        request. If a session object has been provided during the construction
        of the class, the provided session object will be returned; otherwise,
        a new session object will be created for each request.

        :return: A requests.Session object to be used in the fulfillment of an
                 HTTP request.
        :rtype: requests.Session
        """
        if self.session is None:
            return requests.Session()

        return self.session

    def get(self, url: str, **kwargs) -> requests.Response:
        """
        A wrapper for requests.get()

        :param url: URL of the resource to request

        :type url: str

        :return: Request response object.
        :rtype: requests.Response
        """
        return self._request_handler("GET", url, kwargs)

    def options(self, url, **kwargs) -> requests.Response:
        """
        A wrapper for requests.options()

        :param url: URL of the resource to request

        :type url: str

        :return: Request response object.
        :rtype: requests.Response
        """
        return self._request_handler("OPTIONS", url, kwargs)

    def head(self, url, **kwargs) -> requests.Response:
        """
        A wrapper for requests.head()

        :param url: URL of the resource to request

        :type url: str

        :return: Request response object.
        :rtype: requests.Response
        """
        return self._request_handler("HEAD", url, kwargs)

    def post(self, url, **kwargs) -> requests.Response:
        """
        A wrapper for requests.post()

        :param url: URL of the resource to request

        :type url: str

        :return: Request response object.
        :rtype: requests.Response
        """
        return self._request_handler("POST", url, kwargs)

    def put(self, url, **kwargs) -> requests.Response:
        """
        A wrapper for requests.put()

        :param url: URL of the resource to request

        :type url: str

        :return: Request response object.
        :rtype: requests.Response
        """
        return self._request_handler("PUT", url, kwargs)

    def patch(self, url, **kwargs) -> requests.Response:
        """
        A wrapper for requests.patch()

        :param url: URL of the resource to request

        :type url: str

        :return: Request response object.
        :rtype: requests.Response
        """
        return self._request_handler("PATCH", url, kwargs)

    def delete(self, url, **kwargs) -> requests.Response:
        """
        A wrapper for requests.delete()

        :param url: URL of the resource to request

        :type url: str

        :return: Request response object.
        :rtype: requests.Response
        """
        return self._request_handler("DELETE", url, kwargs)


class RetrySession(RetryRequest):
    """
    The RetrySession class is a child of the RetryRequest class. It's
    functionality is identical except all requests will share a
    requests.Session object. As is the case in both the RetrySession and
    RetryRequest classes, the end-user can provide a requests.Session object to
    be used instead of a newly initialized object.
    """

    session = requests.Session()
    logger = module_logger.getChild("RetrySession")
