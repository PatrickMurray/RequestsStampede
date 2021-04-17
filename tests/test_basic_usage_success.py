"""
TODO :)
"""


import requests

import RequestsStampede.horde


def test_basic_get_success():
    """
    Tests RequestsStampede.horde.RetryRequest.get()
    """
    horde = RequestsStampede.horde.RetryRequest()

    response = horde.get("https://httpbin.org/get")

    assert isinstance(response, requests.Response)
    assert response.ok

    json = response.json()

    assert isinstance(json, dict)
    assert "url" in json
    assert json.get("url") == "https://httpbin.org/get"


def test_basic_options_success():
    """
    Tests RequestsStampede.horde.RetryRequest.options()

    Not implemented.
    """


def test_basic_head_success():
    """
    Tests RequestsStampede.horde.RetryRequest.head()

    Not implemented.
    """


def test_basic_post_success():
    """
    Tests RequestsStampede.horde.RetryRequest.post()
    """
    horde = RequestsStampede.horde.RetryRequest()

    response = horde.post(
        "https://httpbin.org/post", data={"hello": "world", "foo": "bar"}
    )

    assert isinstance(response, requests.Response)
    assert response.ok

    json = response.json()

    assert isinstance(json, dict)
    assert "url" in json
    assert json.get("url") == "https://httpbin.org/post"

    assert "form" in json
    form = json.get("form")
    assert isinstance(form, dict)

    assert "hello" in form
    assert form.get("hello") == "world"

    assert "foo" in form
    assert form.get("foo") == "bar"


def test_basic_put_success():
    """
    Tests RequestsStampede.horde.RetryRequest.put()
    """
    horde = RequestsStampede.horde.RetryRequest()

    response = horde.put(
        "https://httpbin.org/put", data={"hello": "world", "foo": "bar"}
    )

    assert isinstance(response, requests.Response)
    assert response.ok

    json = response.json()

    assert isinstance(json, dict)
    assert "url" in json
    assert json.get("url") == "https://httpbin.org/put"

    assert "form" in json
    form = json.get("form")
    assert isinstance(form, dict)

    assert "hello" in form
    assert form.get("hello") == "world"

    assert "foo" in form
    assert form.get("foo") == "bar"


def test_basic_patch_success():
    """
    Tests RequestsStampede.horde.RetryRequest.patch()
    """
    horde = RequestsStampede.horde.RetryRequest()

    response = horde.patch("https://httpbin.org/patch")

    assert isinstance(response, requests.Response)
    assert response.ok

    json = response.json()

    assert isinstance(json, dict)
    assert "url" in json
    assert json.get("url") == "https://httpbin.org/patch"


def test_basic_delete_success():
    """
    Tests RequestsStampede.horde.RetryRequest.delete()
    """
    horde = RequestsStampede.horde.RetryRequest()

    response = horde.delete("https://httpbin.org/delete")

    assert isinstance(response, requests.Response)
    assert response.ok

    json = response.json()

    assert isinstance(json, dict)
    assert "url" in json
    assert json.get("url") == "https://httpbin.org/delete"
