<img src="docs/img/requests_stampede_banner.png" alt="Requests Stampede Banner" width="420" />


## Overview

The Requests Stampede library is a wrapper around the [Requests library](https://github.com/psf/requests)
that provides request retry logic and backoff delays. The goal of the project
is to improve upstream service stability and time to recovery following an
outage and influx of retry requests. The library provides various default
configurations with sane parameters; however, behavior is configurable via both
programmatic declarations and configuration files.


## Inspiration

The Request Stampede library was largely inspired by the [2021-01-15 Signal
messaging service outage](https://twitter.com/signalapp/status/1350118809860886528)
wherein a service disruption was worsened by [their mobile app retry-logic
inflicting a self-induced DDoS attack](https://twitter.com/NovakDaniel/status/1350471722034745348)
on their systems. The project implementes many of the [recommendations outlined
in Google Cloud's blog post on the subject](https://cloud.google.com/blog/products/gcp/how-to-avoid-a-self-inflicted-ddos-attack-cre-life-lessons).


## Usage

### Basic

```python3
import RequestsStampede.horde

horde = RequestsStampede.horde.RetryRequest()

response = horde.get("https://www.example.com/")
print(response)
```

```python3
import RequestsStampede.horde

session = RequestsStampede.horde.RetrySession()

response = session.post(
    "https://www.example.com/login",
    data={
        'username': 'johndoe',
        'password': 'hunter2'
    }
)
print(response)

response = session.get("https://www.example.com/profile")
print(response)
```


### Intermediate

```python3
import requests.session
import RequestsStampede.horde

session = RequestsStampede.horde.RetrySession(
    session=requests.session.Session(
        headers={
            "Authorization": "Bearer <TOKEN>"
        }
    )
)

response = session.post("https://www.example.com/resource")
print(response)

response = session.get("https://www.example.com/resource")
print(response)
```


### Advanced


#### Configuration

`stampede.yml`

```yaml
retry_config:
  retry_enabled: True
  retry_policy:
    type: infinite

  backoff_enabled: True
  backoff_policy:
    type: fibonacci
    initial_delay: 0.0
    maximum_delay: 144.0
```

```python3
import requests.session
import RequestsStampede.horde

session = RequestsStampede.horde.RetrySession(
    session=requests.session.Session(
        headers={
            "Authorization": "Bearer <TOKEN>"
        }
    )
)

response = session.post("https://www.example.com/resource")
print(response)

response = session.get("https://www.example.com/resource")
print(response)
```


## Features


### HTTP Methods

The Requests Stampede library supports all HTTP methods currently supported by
the [Requests library](https://github.com/psf/requests/blob/c2674158826050ad8e134da3e09546f36466777b/requests/api.py#L64-L159):

- [`GET`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET)
- [`OPTIONS`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/OPTIONS)
- [`HEAD`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD)
- [`POST`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST)
- [`PUT`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT)
- [`PATCH`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH)
- [`DELETE`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/DELETE)


### Retry Configuration

When an HTTP request is unsuccessful, that request may be retried depending on
the configured retry policy. Following an unsuccessful request or retry
attempt, a backoff delay may be introduced in an effort to reduce congestion
and system load on the upstream resource.


#### Retry Policies

##### Fixed

The fixed retry policy will attempt to retransmit a request until the maximum
number of attempts has been reached. Upon exhaustion of all retry attempts, the
request will be discarded.

##### Infinite

The infinite retry policy will indefinitely retransmit a request until a
successful response is received.


#### Backoff Policies

##### Fixed

Following a failed request, a fixed backoff policy will introduce a constant
delay between the next attempted transmission. For example, a delay of 5
seconds may be introduced between request attempts.

##### Random

Following a failed request, a random backoff policy will introduce a random,
normally distributed, delay between two configurable bounds prior to the next
attempted transmission. For example, a random delay between 5 and 15 seconds
may be introduced between request attempts.

##### Fibonacci

Following a failed request, a series of [fibonacci](https://en.wikipedia.org/wiki/Fibonacci_number)
delays will be introduced in between subsequent transmission attempts. For
example, a retry attempt sequence may follow the pattern below:

```
No | Event
---|------
0  | Initial Request, Failure
1  | Backoff, 0 sec
2  | Retry Request, Failure
3  | Backoff, 1 sec
4  | Retry Request, Failure
5  | Backoff, 1 sec
6  | Retry Request, Failure
7  | Backoff, 2 sec
8  | Retry Request, Failure
9  | Backoff, 3 sec
...
```


#### Configuration Methods

##### Programatic

The `RetryRequest` and `RetrySession` classes accept parameters to configure
both the desired retry configuration and request session object.

##### Configuration File

If configuration parameters are not provided to `RetryRequest` or
`RetrySession`, RequestsStampede will traverse the file-system for a
configuration file, `stampede.yml`. For example, given an application running
in `/etc/application`, RequestsStampede will traverse the following paths and
select the first configuration file encountered:

1. `/etc/application/stampede.yml`
2. `/etc/stampede.yml`
3. `/stampede.yml`
4. `$HOME/stampede.yml`

If no configuration file is located, a default retry configuration will be
utilized.


### Request Interfaces

Requests Stampede exposes two interfaces within the `RequestsStampede.horde`
sub-module, whether you choose `RetryRequest` or `RetrySession` is entirely
dependent on whether or not you require session persistence across multiple
requests.

#### Non-Persistent Session

For basic applications, such as unauthenticated web scraping, `RetryRequest` is
likely suffient. The interface does not offer session persistence across
multiple requests by default.

#### Persistent Session

For more complex use-cases, your application may require session persistence to
properly authenticate with an upstream resource. The `RetrySession` interface
is best suited for this use case as it will use one session for all requests.


### Logging

The `logging` module is used for all logging interfaces within the
RequestsStampede module. Logs may be exposed by raising the logging level (i.e.
`logging.basicConfig(level=logging.DEBUG)`).


## Development

### Virtual Environment

```bash
virtualenv --python=python3 venv
source venv/bin/activate
```

### Local Installation

```bash
pip3 install .
```

### Development Dependencies

```bash
pip3 install -r dev-requirements.txt
```

### Code Formatting & Linting

```bash
black .
pylint RequestsStampede
pylint tests
```

### Tests

```bash
pytest
```


## Contributors

1. Patrick Murray
2. Zachary Barden


## Attribution

1. The Requests Stampede icon and banner graphics use content created by
   [Game-icons.net](https://game-icons.net/) which was licensed under a
   [Creative Commons 3.0 license](https://creativecommons.org/licenses/by/3.0/).
   Minor modifications were made to the content for use by the Requests
   Stampede project.
