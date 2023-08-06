# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

import os
import json
from typing import Dict, Union, Mapping, Optional
from typing_extensions import Literal

import httpx

from . import resources as _resources
from ._qs import Querystring
from .types import APIStatus, Sta_563PostEmptyObjectResponse
from ._types import (
    NOT_GIVEN,
    Body,
    Omit,
    Query,
    Headers,
    Timeout,
    NoneType,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import coerce_float, coerce_boolean, coerce_integer
from ._version import __version__
from ._base_client import DEFAULT_LIMITS, DEFAULT_TIMEOUT, DEFAULT_MAX_RETRIES
from ._base_client import Stream as Stream
from ._base_client import AsyncStream as AsyncStream
from ._base_client import SyncAPIClient, AsyncAPIClient, make_request_options

__all__ = [
    "ENVIRONMENTS",
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "_resources",
    "Sink",
    "AsyncSink",
    "Client",
    "AsyncClient",
]

ENVIRONMENTS: Dict[str, str] = {
    "production": "https://demo.stainlessapi.com/",
    "sandbox": "https://demo-sanbox.stainlessapi.com/",
}


class Sink(SyncAPIClient):
    testing: _resources.Testing
    pagination_tests: _resources.PaginationTests
    resource_refs: _resources.ResourceRefs
    cards: _resources.Cards
    resources: _resources.Resources
    config_tools: _resources.ConfigTools
    company: _resources.CompanyResource
    sta_563: _resources.Sta_563
    sta_569: _resources.Sta_569
    sta_630: _resources.Sta_630
    parent: _resources.Parent
    sta_606: _resources.Sta_606
    envelopes: _resources.Envelopes
    types: _resources.Types
    names: _resources.Names
    widgets: _resources.Widgets
    sta_613: _resources.Sta_613
    responses: _resources.Responses
    path_params: _resources.PathParams
    query_params: _resources.QueryParams
    body_params: _resources.BodyParams
    header_params: _resources.HeaderParams
    decorator_tests: _resources.DecoratorTests
    tests: _resources.Tests
    deeply_nested: _resources.DeeplyNested

    # client options
    user_token: str | None
    username: str
    client_id: str | None
    client_secret: str | None
    some_boolean_arg: bool | None
    some_integer_arg: int | None
    some_number_arg: float | None
    client_path_param: str | None
    camel_case_path: str | None

    _environment: Literal["production", "sandbox"]

    def __init__(
        self,
        *,
        username: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = "hellosecret",
        some_boolean_arg: bool | None = True,
        some_integer_arg: int | None = 123,
        some_number_arg: float | None = 1.2,
        client_path_param: str | None = None,
        camel_case_path: str | None = None,
        environment: Literal["production", "sandbox"] = "production",
        base_url: Optional[str] = None,
        user_token: Optional[str] = None,
        timeout: Union[float, Timeout, None] = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # See httpx documentation for [custom transports](https://www.python-httpx.org/advanced/#custom-transports)
        transport: Optional[Transport] = None,
        # See httpx documentation for [proxies](https://www.python-httpx.org/advanced/#http-proxying)
        proxies: Optional[ProxiesTypes] = None,
        # See httpx documentation for [limits](https://www.python-httpx.org/advanced/#pool-limit-configuration)
        connection_pool_limits: httpx.Limits | None = DEFAULT_LIMITS,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous sink client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `username` from `SINK_USER`
        - `client_id` from `SINK_CLIENT_ID`
        - `client_secret` from `SINK_CLIENT_SECRET`
        - `some_boolean_arg` from `SINK_SOME_BOOLEAN_ARG`
        - `some_integer_arg` from `SINK_SOME_INTEGER_ARG`
        - `some_number_arg` from `SINK_SOME_NUMBER_ARG`
        - `user_token` from `SINK_CUSTOM_API_KEY_ENV`
        """
        user_token = user_token or os.environ.get("SINK_CUSTOM_API_KEY_ENV", "")

        self._environment = environment

        if base_url is None:
            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            transport=transport,
            proxies=proxies,
            limits=connection_pool_limits,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.user_token = user_token

        username_envvar = os.environ.get("SINK_USER", None)
        username = username or username_envvar or None
        if username is None:
            raise ValueError(
                "The username client option must be set either by passing username to the client or by setting the SINK_USER environment variable"
            )
        self.username = username

        client_id_envvar = os.environ.get("SINK_CLIENT_ID", None)
        self.client_id = client_id or client_id_envvar or None

        client_secret_envvar = os.environ.get("SINK_CLIENT_SECRET", None)
        self.client_secret = client_secret or client_secret_envvar or "hellosecret"

        some_boolean_arg_envvar = os.environ.get("SINK_SOME_BOOLEAN_ARG", None)
        self.some_boolean_arg = (
            some_boolean_arg
            or (some_boolean_arg_envvar is not None and coerce_boolean(some_boolean_arg_envvar))
            or True
        )

        some_integer_arg_envvar = os.environ.get("SINK_SOME_INTEGER_ARG", None)
        self.some_integer_arg = (
            some_integer_arg or (some_integer_arg_envvar is not None and coerce_integer(some_integer_arg_envvar)) or 123
        )

        some_number_arg_envvar = os.environ.get("SINK_SOME_NUMBER_ARG", None)
        self.some_number_arg = (
            some_number_arg or (some_number_arg_envvar is not None and coerce_float(some_number_arg_envvar)) or 1.2
        )

        self.client_path_param = client_path_param or None

        self.camel_case_path = camel_case_path or None

        self._idempotency_header = "Idempotency-Key"

        self.testing = _resources.Testing(self)
        self.pagination_tests = _resources.PaginationTests(self)
        self.resource_refs = _resources.ResourceRefs(self)
        self.cards = _resources.Cards(self)
        self.resources = _resources.Resources(self)
        self.config_tools = _resources.ConfigTools(self)
        self.company = _resources.CompanyResource(self)
        self.sta_563 = _resources.Sta_563(self)
        self.sta_569 = _resources.Sta_569(self)
        self.sta_630 = _resources.Sta_630(self)
        self.parent = _resources.Parent(self)
        self.sta_606 = _resources.Sta_606(self)
        self.envelopes = _resources.Envelopes(self)
        self.types = _resources.Types(self)
        self.names = _resources.Names(self)
        self.widgets = _resources.Widgets(self)
        self.sta_613 = _resources.Sta_613(self)
        self.responses = _resources.Responses(self)
        self.path_params = _resources.PathParams(self)
        self.query_params = _resources.QueryParams(self)
        self.body_params = _resources.BodyParams(self)
        self.header_params = _resources.HeaderParams(self)
        self.decorator_tests = _resources.DecoratorTests(self)
        self.tests = _resources.Tests(self)
        self.deeply_nested = _resources.DeeplyNested(self)

    @property
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    def auth_headers(self) -> dict[str, str]:
        user_token = self.user_token
        if user_token is None:
            return {}
        return {"Authorization": f"Bearer {user_token}"}

    @property
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "My-Api-Version": "11",
            "X-Enable-Metrics": "1",
            "X-Client-UserName": self.username,
            "X-Client-Secret": self.client_secret if self.client_secret is not None else Omit(),
            "X-Integer": str(self.some_integer_arg) if self.some_integer_arg is not None else Omit(),
            **self._custom_headers,
        }

    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        if self.user_token and headers.get("Authorization"):
            return
        if isinstance(custom_headers.get("Authorization"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected the user_token to be set. Or for the `Authorization` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        username: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        some_boolean_arg: bool | None = None,
        some_integer_arg: int | None = None,
        some_number_arg: float | None = None,
        client_path_param: str | None = None,
        camel_case_path: str | None = None,
        user_token: str | None = None,
        environment: Literal["production", "sandbox"] | None = None,
        base_url: str | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        connection_pool_limits: httpx.Limits | NotGiven = NOT_GIVEN,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
    ) -> Sink:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.

        It should be noted that this does not share the underlying httpx client class which may lead
        to performance issues.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        # TODO: share the same httpx client between instances
        return self.__class__(
            username=username or self.username,
            client_id=client_id or self.client_id,
            client_secret=client_secret or self.client_secret,
            some_boolean_arg=some_boolean_arg or self.some_boolean_arg,
            some_integer_arg=some_integer_arg or self.some_integer_arg,
            some_number_arg=some_number_arg or self.some_number_arg,
            client_path_param=client_path_param or self.client_path_param,
            camel_case_path=camel_case_path or self.camel_case_path,
            base_url=base_url or str(self.base_url),
            environment=environment or self._environment,
            user_token=user_token or self.user_token,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            connection_pool_limits=self._limits
            if isinstance(connection_pool_limits, NotGiven)
            else connection_pool_limits,
            max_retries=self.max_retries if isinstance(max_retries, NotGiven) else max_retries,
            default_headers=headers,
            default_query=params,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    def api_status(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
    ) -> APIStatus:
        """API status check"""
        return self.get(
            "/status",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIStatus,
        )

    api_status_alias = api_status

    def create_no_response(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> None:
        """Endpoint returning no response"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self.post(
            "/no_response",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def get_auth_url(
        self,
        *,
        print_data: bool,
        redirect_uri: str,
        client_id: str,
    ) -> str:
        """A top level custom method on the sink customer."""
        if print_data:
            # used to test imports
            print(json.dumps("foo"))  # noqa: T201

        return str(
            httpx.URL(
                "http://localhost:8000/auth",
                params={
                    "client_id": client_id,
                    "redirect_uri": redirect_uri,
                },
            )
        )

    def sta_563_post_empty_object(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> Sta_563PostEmptyObjectResponse:
        """
        Should not generate a named return type for object without defined properties;
        instead, it should simply use an `unknown` type or equivalent. In Java and Go,
        where we have fancier accessors for raw json stuff, we should generate a named
        type, but it should basically just have untyped additional properties. See
        https://linear.app/stainless/issue/STA-563/no-type-should-be-generated-for-endpoints-returning-type-object-schema.
        """
        return self.post(
            "/sta_563_empty_object",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=Sta_563PostEmptyObjectResponse,
        )

    def _get_client_path_param_param(self) -> str:
        from_client = self.client_path_param
        if from_client is not None:
            return from_client

        raise ValueError(
            "Missing client_path_param argument; Please provide it at the client level, e.g. Sink(client_path_param='abcd') or per method."
        )

    def _get_camel_case_path_param(self) -> str:
        from_client = self.camel_case_path
        if from_client is not None:
            return from_client

        raise ValueError(
            "Missing camel_case_path argument; Please provide it at the client level, e.g. Sink(camel_case_path='abcd') or per method."
        )


class AsyncSink(AsyncAPIClient):
    testing: _resources.AsyncTesting
    pagination_tests: _resources.AsyncPaginationTests
    resource_refs: _resources.AsyncResourceRefs
    cards: _resources.AsyncCards
    resources: _resources.AsyncResources
    config_tools: _resources.AsyncConfigTools
    company: _resources.AsyncCompanyResource
    sta_563: _resources.AsyncSta_563
    sta_569: _resources.AsyncSta_569
    sta_630: _resources.AsyncSta_630
    parent: _resources.AsyncParent
    sta_606: _resources.AsyncSta_606
    envelopes: _resources.AsyncEnvelopes
    types: _resources.AsyncTypes
    names: _resources.AsyncNames
    widgets: _resources.AsyncWidgets
    sta_613: _resources.AsyncSta_613
    responses: _resources.AsyncResponses
    path_params: _resources.AsyncPathParams
    query_params: _resources.AsyncQueryParams
    body_params: _resources.AsyncBodyParams
    header_params: _resources.AsyncHeaderParams
    decorator_tests: _resources.AsyncDecoratorTests
    tests: _resources.AsyncTests
    deeply_nested: _resources.AsyncDeeplyNested

    # client options
    user_token: str | None
    username: str
    client_id: str | None
    client_secret: str | None
    some_boolean_arg: bool | None
    some_integer_arg: int | None
    some_number_arg: float | None
    client_path_param: str | None
    camel_case_path: str | None

    _environment: Literal["production", "sandbox"]

    def __init__(
        self,
        *,
        username: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = "hellosecret",
        some_boolean_arg: bool | None = True,
        some_integer_arg: int | None = 123,
        some_number_arg: float | None = 1.2,
        client_path_param: str | None = None,
        camel_case_path: str | None = None,
        environment: Literal["production", "sandbox"] = "production",
        base_url: Optional[str] = None,
        user_token: Optional[str] = None,
        timeout: Union[float, Timeout, None] = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # See httpx documentation for [custom transports](https://www.python-httpx.org/advanced/#custom-transports)
        transport: Optional[Transport] = None,
        # See httpx documentation for [proxies](https://www.python-httpx.org/advanced/#http-proxying)
        proxies: Optional[ProxiesTypes] = None,
        # See httpx documentation for [limits](https://www.python-httpx.org/advanced/#pool-limit-configuration)
        connection_pool_limits: httpx.Limits | None = DEFAULT_LIMITS,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async sink client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `username` from `SINK_USER`
        - `client_id` from `SINK_CLIENT_ID`
        - `client_secret` from `SINK_CLIENT_SECRET`
        - `some_boolean_arg` from `SINK_SOME_BOOLEAN_ARG`
        - `some_integer_arg` from `SINK_SOME_INTEGER_ARG`
        - `some_number_arg` from `SINK_SOME_NUMBER_ARG`
        - `user_token` from `SINK_CUSTOM_API_KEY_ENV`
        """
        user_token = user_token or os.environ.get("SINK_CUSTOM_API_KEY_ENV", "")

        self._environment = environment

        if base_url is None:
            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            transport=transport,
            proxies=proxies,
            limits=connection_pool_limits,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.user_token = user_token

        username_envvar = os.environ.get("SINK_USER", None)
        username = username or username_envvar or None
        if username is None:
            raise ValueError(
                "The username client option must be set either by passing username to the client or by setting the SINK_USER environment variable"
            )
        self.username = username

        client_id_envvar = os.environ.get("SINK_CLIENT_ID", None)
        self.client_id = client_id or client_id_envvar or None

        client_secret_envvar = os.environ.get("SINK_CLIENT_SECRET", None)
        self.client_secret = client_secret or client_secret_envvar or "hellosecret"

        some_boolean_arg_envvar = os.environ.get("SINK_SOME_BOOLEAN_ARG", None)
        self.some_boolean_arg = (
            some_boolean_arg
            or (some_boolean_arg_envvar is not None and coerce_boolean(some_boolean_arg_envvar))
            or True
        )

        some_integer_arg_envvar = os.environ.get("SINK_SOME_INTEGER_ARG", None)
        self.some_integer_arg = (
            some_integer_arg or (some_integer_arg_envvar is not None and coerce_integer(some_integer_arg_envvar)) or 123
        )

        some_number_arg_envvar = os.environ.get("SINK_SOME_NUMBER_ARG", None)
        self.some_number_arg = (
            some_number_arg or (some_number_arg_envvar is not None and coerce_float(some_number_arg_envvar)) or 1.2
        )

        self.client_path_param = client_path_param or None

        self.camel_case_path = camel_case_path or None

        self._idempotency_header = "Idempotency-Key"

        self.testing = _resources.AsyncTesting(self)
        self.pagination_tests = _resources.AsyncPaginationTests(self)
        self.resource_refs = _resources.AsyncResourceRefs(self)
        self.cards = _resources.AsyncCards(self)
        self.resources = _resources.AsyncResources(self)
        self.config_tools = _resources.AsyncConfigTools(self)
        self.company = _resources.AsyncCompanyResource(self)
        self.sta_563 = _resources.AsyncSta_563(self)
        self.sta_569 = _resources.AsyncSta_569(self)
        self.sta_630 = _resources.AsyncSta_630(self)
        self.parent = _resources.AsyncParent(self)
        self.sta_606 = _resources.AsyncSta_606(self)
        self.envelopes = _resources.AsyncEnvelopes(self)
        self.types = _resources.AsyncTypes(self)
        self.names = _resources.AsyncNames(self)
        self.widgets = _resources.AsyncWidgets(self)
        self.sta_613 = _resources.AsyncSta_613(self)
        self.responses = _resources.AsyncResponses(self)
        self.path_params = _resources.AsyncPathParams(self)
        self.query_params = _resources.AsyncQueryParams(self)
        self.body_params = _resources.AsyncBodyParams(self)
        self.header_params = _resources.AsyncHeaderParams(self)
        self.decorator_tests = _resources.AsyncDecoratorTests(self)
        self.tests = _resources.AsyncTests(self)
        self.deeply_nested = _resources.AsyncDeeplyNested(self)

    @property
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    def auth_headers(self) -> dict[str, str]:
        user_token = self.user_token
        if user_token is None:
            return {}
        return {"Authorization": f"Bearer {user_token}"}

    @property
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "My-Api-Version": "11",
            "X-Enable-Metrics": "1",
            "X-Client-UserName": self.username,
            "X-Client-Secret": self.client_secret if self.client_secret is not None else Omit(),
            "X-Integer": str(self.some_integer_arg) if self.some_integer_arg is not None else Omit(),
            **self._custom_headers,
        }

    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        if self.user_token and headers.get("Authorization"):
            return
        if isinstance(custom_headers.get("Authorization"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected the user_token to be set. Or for the `Authorization` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        username: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        some_boolean_arg: bool | None = None,
        some_integer_arg: int | None = None,
        some_number_arg: float | None = None,
        client_path_param: str | None = None,
        camel_case_path: str | None = None,
        user_token: str | None = None,
        environment: Literal["production", "sandbox"] | None = None,
        base_url: str | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        connection_pool_limits: httpx.Limits | NotGiven = NOT_GIVEN,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
    ) -> AsyncSink:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.

        It should be noted that this does not share the underlying httpx client class which may lead
        to performance issues.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        # TODO: share the same httpx client between instances
        return self.__class__(
            username=username or self.username,
            client_id=client_id or self.client_id,
            client_secret=client_secret or self.client_secret,
            some_boolean_arg=some_boolean_arg or self.some_boolean_arg,
            some_integer_arg=some_integer_arg or self.some_integer_arg,
            some_number_arg=some_number_arg or self.some_number_arg,
            client_path_param=client_path_param or self.client_path_param,
            camel_case_path=camel_case_path or self.camel_case_path,
            base_url=base_url or str(self.base_url),
            environment=environment or self._environment,
            user_token=user_token or self.user_token,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            connection_pool_limits=self._limits
            if isinstance(connection_pool_limits, NotGiven)
            else connection_pool_limits,
            max_retries=self.max_retries if isinstance(max_retries, NotGiven) else max_retries,
            default_headers=headers,
            default_query=params,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    async def api_status(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
    ) -> APIStatus:
        """API status check"""
        return await self.get(
            "/status",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIStatus,
        )

    api_status_alias = api_status

    async def create_no_response(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> None:
        """Endpoint returning no response"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self.post(
            "/no_response",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def get_auth_url(
        self,
        *,
        print_data: bool,
        redirect_uri: str,
        client_id: str,
    ) -> str:
        """A top level custom method on the sink customer."""
        if print_data:
            # used to test imports
            print(json.dumps("foo"))  # noqa: T201

        return str(
            httpx.URL(
                "http://localhost:8000/auth",
                params={
                    "client_id": client_id,
                    "redirect_uri": redirect_uri,
                },
            )
        )

    async def sta_563_post_empty_object(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> Sta_563PostEmptyObjectResponse:
        """
        Should not generate a named return type for object without defined properties;
        instead, it should simply use an `unknown` type or equivalent. In Java and Go,
        where we have fancier accessors for raw json stuff, we should generate a named
        type, but it should basically just have untyped additional properties. See
        https://linear.app/stainless/issue/STA-563/no-type-should-be-generated-for-endpoints-returning-type-object-schema.
        """
        return await self.post(
            "/sta_563_empty_object",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=Sta_563PostEmptyObjectResponse,
        )

    def _get_client_path_param_param(self) -> str:
        from_client = self.client_path_param
        if from_client is not None:
            return from_client

        raise ValueError(
            "Missing client_path_param argument; Please provide it at the client level, e.g. AsyncSink(client_path_param='abcd') or per method."
        )

    def _get_camel_case_path_param(self) -> str:
        from_client = self.camel_case_path
        if from_client is not None:
            return from_client

        raise ValueError(
            "Missing camel_case_path argument; Please provide it at the client level, e.g. AsyncSink(camel_case_path='abcd') or per method."
        )


Client = Sink

AsyncClient = AsyncSink
