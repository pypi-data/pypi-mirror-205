# Sink Python API Library

[![PyPI version](https://img.shields.io/pypi/v/sink-pypi.svg)](https://pypi.org/project/sink-pypi/)

The Sink Python library provides convenient access to the Sink REST API from any Python 3.7+
application. It includes type definitions for all request params and response fields,
and offers both synchronous and asynchronous clients powered by [httpx](https://github.com/encode/httpx).

## Documentation

The API documentation can be found [here](https://stainlessapi.com).

## Installation

```sh
pip install sink-pypi
```

## Usage

```python
from sink import Sink

sink = Sink(
    # defaults to os.environ.get("SINK_CUSTOM_API_KEY_ENV")
    user_token="my user token",
    # defaults to "production".
    environment="sandbox",
    username="Robert",
)

card = sink.cards.create(
    type="SINGLE_USE",
    not_="TEST",
)
print(card.token)
```

While you can provide a `user_token` keyword argument, we recommend using [python-dotenv](https://pypi.org/project/python-dotenv/)
and adding `SINK_CUSTOM_API_KEY_ENV="my user token"` to your `.env` file so that your user token is not stored in source control.

## Async Usage

Simply import `AsyncSink` instead of `Sink` and use `await` with each API call:

```python
from sink import AsyncSink

sink = AsyncSink(
    # defaults to os.environ.get("SINK_CUSTOM_API_KEY_ENV")
    user_token="my user token",
    # defaults to "production".
    environment="sandbox",
    username="Robert",
)


async def main():
    card = await sink.cards.create(
        type="SINGLE_USE",
        not_="TEST",
    )
    print(card.token)


asyncio.run(main())
```

Functionality between the synchronous and asynchronous clients is otherwise identical.

## Using Types

Nested request parameters are [TypedDicts](https://docs.python.org/3/library/typing.html#typing.TypedDict), while responses are [Pydantic](https://pydantic-docs.helpmanual.io/) models. This helps provide autocomplete and documentation within your editor.

If you would like to see type errors in VS Code to help catch bugs earlier, set `python.analysis.typeCheckingMode` to `"basic"`.

## Pagination

List methods in the Sink API are paginated.

This library provides auto-paginating iterators with each list response, so you do not have to request successive pages manually:

```python
import sink

sink = Sink(
    username="Robert",
)

all_offsets = []
# Automatically fetches more pages as needed.
for offset in sink.pagination_tests.offset.list():
    # Do something with offset here
    all_offsets.append(offset)
print(all_offsets)
```

Or, asynchronously:

```python
import asyncio
import sink

sink = AsyncSink(
    username="Robert",
)


async def main() -> None:
    all_offsets = []
    # Iterate through items across all pages, issuing requests as needed.
    async for offset in sink.pagination_tests.offset.list():
        all_offsets.append(offset)
    print(all_offsets)


asyncio.run(main())
```

Alternatively, you can use the `.has_next_page()`, `.next_page_info()`, or `.get_next_page()` methods for more granular control working with pages:

```python
first_page = await sink.pagination_tests.offset.list()
if first_page.has_next_page():
    print(f"will fetch next page using these details: {first_page.next_page_info()}")
    next_page = await first_page.get_next_page()
    print(f"number of items we just fetched: {len(next_page.data)}")

# Remove `await` for non-async usage.
```

Or just work directly with the returned data:

```python
first_page = await sink.pagination_tests.offset.list()

print(
    f"the current start offset for this page: {first_page.offset}"
)  # => "the current start offset for this page: 1"
for offset in first_page.data:
    print(offset.bar)

# Remove `await` for non-async usage.
```

## Nested params

Nested parameters are dictionaries, typed using `TypedDict`, for example:

```py
from sink import Sink

sink = Sink(
    username="Robert",
)

sink.cards.create(
    foo={
        "bar": True
    },
)
```

## Handling errors

When the library is unable to connect to the API (e.g., due to network connection problems or a timeout), a subclass of `sink.APIConnectionError` is raised.

When the API returns a non-success status code (i.e., 4xx or 5xx
response), a subclass of `sink.APIStatusError` will be raised, containing `status_code` and `response` properties.

All errors inherit from `sink.APIError`.

```python
from sink import Sink

sink = Sink(
    username="Robert",
)

try:
    sink.cards.create(
        type="an_incorrect_type",
    )
except sink.APIConnectionError as e:
    print("The server could not be reached")
    print(e.__cause__)  # an underlying Exception, likely raised within httpx.
except sink.RateLimitError as e:
    print("A 429 status code was received; we should back off a bit.")
except sink.APIStatusError as e:
    print("Another non-200-range status code was received")
    print(e.status_code)
    print(e.response)
```

Error codes are as followed:

| Status Code | Error Type                 |
| ----------- | -------------------------- |
| 400         | `BadRequestError`          |
| 401         | `AuthenticationError`      |
| 403         | `PermissionDeniedError`    |
| 404         | `NotFoundError`            |
| 422         | `UnprocessableEntityError` |
| 429         | `RateLimitError`           |
| >=500       | `InternalServerError`      |
| N/A         | `APIConnectionError`       |

### Retries

Certain errors will be automatically retried 2 times by default, with a short exponential backoff.
Connection errors (for example, due to a network connectivity problem), 409 Conflict, 429 Rate Limit,
and >=500 Internal errors will all be retried by default.

You can use the `max_retries` option to configure or disable this:

```python
from sink import Sink

# Configure the default for all requests:
sink = Sink(
    # default is 2
    max_retries=0,
    username="Robert",
)

# Or, configure per-request:
sink.with_options(max_retries=5).cards.list(
    page_size=10,
)
```

### Timeouts

Requests time out after 60 seconds by default. You can configure this with a `timeout` option,
which accepts a float or an [`httpx.Timeout`](https://www.python-httpx.org/advanced/#fine-tuning-the-configuration):

```python
from sink import Sink

# Configure the default for all requests:
sink = Sink(
    # default is 60s
    timeout=20.0,
    username="Robert",
)

# More granular control:
sink = Sink(
    timeout=httpx.Timeout(60.0, read=5.0, write=10.0, connect=2.0),
    username="Robert",
)

# Override per-request:
sink.with_options(timeout=5 * 1000).cards.list(
    page_size=10,
)
```

On timeout, an `APITimeoutError` is thrown.

Note that requests which time out will be [retried twice by default](#retries).

## Default Headers

We automatically send the following headers with all requests.

| Header             | Value |
| ------------------ | ----- |
| `My-Api-Version`   | `11`  |
| `X-Enable-Metrics` | `1`   |

If you need to, you can override these headers by setting default headers per-request or on the client object.

```python
from sink import Sink

sink = Sink(
    default_headers={"My-Api-Version": My - Custom - Value},
    username="Robert",
)
```

## Advanced: Configuring custom URLs, proxies, and transports

You can configure the following keyword arguments when instantiating the client:

```python
import httpx
from sink import Sink

sink = Sink(
    # Use a custom base URL
    base_url="http://my.test.server.example.com:8083",
    proxies="http://my.test.proxy.example.com",
    transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    username="Robert",
)
```

See the httpx documentation for information about the [`proxies`](https://www.python-httpx.org/advanced/#http-proxying) and [`transport`](https://www.python-httpx.org/advanced/#custom-transports) keyword arguments.

## Status

This package is in beta. Its internals and interfaces are not stable and subject to change without a major semver bump;
please reach out if you rely on any undocumented behavior.

We are keen for your feedback; please email us at [dev@stainlessapi.com](mailto:dev@stainlessapi.com) or open an issue with questions,
bugs, or suggestions.

## Requirements

Python 3.7 or higher.