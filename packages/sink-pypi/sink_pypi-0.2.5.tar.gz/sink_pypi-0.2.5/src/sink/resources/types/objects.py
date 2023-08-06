# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._resource import SyncAPIResource, AsyncAPIResource
from ...types.types import ObjectMixedKnownAndUnknownResponse
from ..._base_client import make_request_options

__all__ = ["Objects", "AsyncObjects"]


class Objects(SyncAPIResource):
    def mixed_known_and_unknown(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
    ) -> ObjectMixedKnownAndUnknownResponse:
        """
        Endpoint with a response schema object that contains a mix of known & unknown
        properties with the same value types.
        """
        return self._get(
            "/types/object/mixed_known_and_unknown",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectMixedKnownAndUnknownResponse,
        )


class AsyncObjects(AsyncAPIResource):
    async def mixed_known_and_unknown(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
    ) -> ObjectMixedKnownAndUnknownResponse:
        """
        Endpoint with a response schema object that contains a mix of known & unknown
        properties with the same value types.
        """
        return await self._get(
            "/types/object/mixed_known_and_unknown",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectMixedKnownAndUnknownResponse,
        )
