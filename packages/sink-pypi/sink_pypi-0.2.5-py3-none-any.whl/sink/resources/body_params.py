# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import Any, cast, overload
from typing_extensions import Literal

from ..types import (
    BodyParamTopLevelAnyOfResponse,
    BodyParamTopLevelOneOfResponse,
    BodyParamUnionOverlappingPropResponse,
    body_param_top_level_any_of_params,
    body_param_top_level_one_of_params,
    body_param_with_model_property_params,
    body_param_read_only_properties_params,
    body_param_union_overlapping_prop_params,
)
from .._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from .._utils import required_args, maybe_transform
from .._resource import SyncAPIResource, AsyncAPIResource
from .._base_client import make_request_options

__all__ = ["BodyParams", "AsyncBodyParams"]


class BodyParams(SyncAPIResource):
    def read_only_properties(
        self,
        *,
        in_both: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` that sets `readOnly` to `true` on top level
        properties

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/body_params/read_only_properties",
            body=maybe_transform(
                {"in_both": in_both}, body_param_read_only_properties_params.BodyParamReadOnlyPropertiesParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    @overload
    def top_level_any_of(
        self,
        *,
        kind: Literal["VIRTUAL", "PHYSICAL"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> BodyParamTopLevelAnyOfResponse:
        """
        Endpoint with a `requestBody` making use of anyOf.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    def top_level_any_of(
        self,
        *,
        is_foo: bool,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> BodyParamTopLevelAnyOfResponse:
        """
        Endpoint with a `requestBody` making use of anyOf.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @required_args(["kind"], ["is_foo"])
    def top_level_any_of(
        self,
        *,
        is_foo: bool | NotGiven = NOT_GIVEN,
        kind: Literal["VIRTUAL", "PHYSICAL"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> BodyParamTopLevelAnyOfResponse:
        """
        Endpoint with a `requestBody` making use of anyOf.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return cast(
            BodyParamTopLevelAnyOfResponse,
            self._post(
                "/body_params/top_level_anyOf",
                body=maybe_transform(
                    {
                        "kind": kind,
                        "is_foo": is_foo,
                    },
                    body_param_top_level_any_of_params.BodyParamTopLevelAnyOfParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    idempotency_key=idempotency_key,
                ),
                cast_to=cast(
                    Any, BodyParamTopLevelAnyOfResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    @overload
    def top_level_one_of(
        self,
        *,
        kind: Literal["VIRTUAL", "PHYSICAL"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> BodyParamTopLevelOneOfResponse:
        """
        Endpoint with a `requestBody` making use of oneOf.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    def top_level_one_of(
        self,
        *,
        is_foo: bool,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> BodyParamTopLevelOneOfResponse:
        """
        Endpoint with a `requestBody` making use of oneOf.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @required_args(["kind"], ["is_foo"])
    def top_level_one_of(
        self,
        *,
        is_foo: bool | NotGiven = NOT_GIVEN,
        kind: Literal["VIRTUAL", "PHYSICAL"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> BodyParamTopLevelOneOfResponse:
        """
        Endpoint with a `requestBody` making use of oneOf.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return cast(
            BodyParamTopLevelOneOfResponse,
            self._post(
                "/body_params/top_level_oneOf",
                body=maybe_transform(
                    {
                        "kind": kind,
                        "is_foo": is_foo,
                    },
                    body_param_top_level_one_of_params.BodyParamTopLevelOneOfParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    idempotency_key=idempotency_key,
                ),
                cast_to=cast(
                    Any, BodyParamTopLevelOneOfResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    @overload
    def union_overlapping_prop(
        self,
        *,
        foo: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> BodyParamUnionOverlappingPropResponse:
        """
        Endpoint with a `requestBody` making use of anyOf where the same property is
        defined in both variants.

        Args:
          foo: FOO 1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    def union_overlapping_prop(
        self,
        *,
        foo: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> BodyParamUnionOverlappingPropResponse:
        """
        Endpoint with a `requestBody` making use of anyOf where the same property is
        defined in both variants.

        Args:
          foo: FOO 2

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    def union_overlapping_prop(
        self,
        *,
        foo: str | bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> BodyParamUnionOverlappingPropResponse:
        """
        Endpoint with a `requestBody` making use of anyOf where the same property is
        defined in both variants.

        Args:
          foo: FOO 1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/body_params/top_level_anyOf_overlapping_property",
            body=maybe_transform(
                {"foo": foo}, body_param_union_overlapping_prop_params.BodyParamUnionOverlappingPropParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BodyParamUnionOverlappingPropResponse,
        )

    def with_model_property(
        self,
        *,
        foo: str | NotGiven = NOT_GIVEN,
        my_model: body_param_with_model_property_params.MyModel | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a request body that contains a property that points to a model
        reference.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/body_params/with_model_property",
            body=maybe_transform(
                {
                    "my_model": my_model,
                    "foo": foo,
                },
                body_param_with_model_property_params.BodyParamWithModelPropertyParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )


class AsyncBodyParams(AsyncAPIResource):
    async def read_only_properties(
        self,
        *,
        in_both: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` that sets `readOnly` to `true` on top level
        properties

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/body_params/read_only_properties",
            body=maybe_transform(
                {"in_both": in_both}, body_param_read_only_properties_params.BodyParamReadOnlyPropertiesParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    @overload
    async def top_level_any_of(
        self,
        *,
        kind: Literal["VIRTUAL", "PHYSICAL"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> BodyParamTopLevelAnyOfResponse:
        """
        Endpoint with a `requestBody` making use of anyOf.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    async def top_level_any_of(
        self,
        *,
        is_foo: bool,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> BodyParamTopLevelAnyOfResponse:
        """
        Endpoint with a `requestBody` making use of anyOf.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @required_args(["kind"], ["is_foo"])
    async def top_level_any_of(
        self,
        *,
        is_foo: bool | NotGiven = NOT_GIVEN,
        kind: Literal["VIRTUAL", "PHYSICAL"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> BodyParamTopLevelAnyOfResponse:
        """
        Endpoint with a `requestBody` making use of anyOf.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return cast(
            BodyParamTopLevelAnyOfResponse,
            await self._post(
                "/body_params/top_level_anyOf",
                body=maybe_transform(
                    {
                        "kind": kind,
                        "is_foo": is_foo,
                    },
                    body_param_top_level_any_of_params.BodyParamTopLevelAnyOfParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    idempotency_key=idempotency_key,
                ),
                cast_to=cast(
                    Any, BodyParamTopLevelAnyOfResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    @overload
    async def top_level_one_of(
        self,
        *,
        kind: Literal["VIRTUAL", "PHYSICAL"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> BodyParamTopLevelOneOfResponse:
        """
        Endpoint with a `requestBody` making use of oneOf.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    async def top_level_one_of(
        self,
        *,
        is_foo: bool,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> BodyParamTopLevelOneOfResponse:
        """
        Endpoint with a `requestBody` making use of oneOf.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @required_args(["kind"], ["is_foo"])
    async def top_level_one_of(
        self,
        *,
        is_foo: bool | NotGiven = NOT_GIVEN,
        kind: Literal["VIRTUAL", "PHYSICAL"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> BodyParamTopLevelOneOfResponse:
        """
        Endpoint with a `requestBody` making use of oneOf.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return cast(
            BodyParamTopLevelOneOfResponse,
            await self._post(
                "/body_params/top_level_oneOf",
                body=maybe_transform(
                    {
                        "kind": kind,
                        "is_foo": is_foo,
                    },
                    body_param_top_level_one_of_params.BodyParamTopLevelOneOfParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    idempotency_key=idempotency_key,
                ),
                cast_to=cast(
                    Any, BodyParamTopLevelOneOfResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    @overload
    async def union_overlapping_prop(
        self,
        *,
        foo: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> BodyParamUnionOverlappingPropResponse:
        """
        Endpoint with a `requestBody` making use of anyOf where the same property is
        defined in both variants.

        Args:
          foo: FOO 1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    async def union_overlapping_prop(
        self,
        *,
        foo: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> BodyParamUnionOverlappingPropResponse:
        """
        Endpoint with a `requestBody` making use of anyOf where the same property is
        defined in both variants.

        Args:
          foo: FOO 2

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    async def union_overlapping_prop(
        self,
        *,
        foo: str | bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> BodyParamUnionOverlappingPropResponse:
        """
        Endpoint with a `requestBody` making use of anyOf where the same property is
        defined in both variants.

        Args:
          foo: FOO 1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/body_params/top_level_anyOf_overlapping_property",
            body=maybe_transform(
                {"foo": foo}, body_param_union_overlapping_prop_params.BodyParamUnionOverlappingPropParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BodyParamUnionOverlappingPropResponse,
        )

    async def with_model_property(
        self,
        *,
        foo: str | NotGiven = NOT_GIVEN,
        my_model: body_param_with_model_property_params.MyModel | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a request body that contains a property that points to a model
        reference.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/body_params/with_model_property",
            body=maybe_transform(
                {
                    "my_model": my_model,
                    "foo": foo,
                },
                body_param_with_model_property_params.BodyParamWithModelPropertyParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )
