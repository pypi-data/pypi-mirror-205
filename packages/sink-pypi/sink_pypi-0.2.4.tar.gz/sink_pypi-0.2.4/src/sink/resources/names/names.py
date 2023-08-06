# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import TYPE_CHECKING

from .params import Params, AsyncParams
from ...types import NameResponseShadowsPydanticResponse
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._base_client import make_request_options

if TYPE_CHECKING:
    from ..._client import Sink, AsyncSink

__all__ = ["Names", "AsyncNames"]


class Names(SyncAPIResource):
    params: Params

    def __init__(self, client: Sink) -> None:
        super().__init__(client)
        self.params = Params(client)

    def response_shadows_pydantic(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
    ) -> NameResponseShadowsPydanticResponse:
        """Endpoint with a response model property that would clash with pydantic."""
        return self._get(
            "/names/response_property_shadows_pydantic",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NameResponseShadowsPydanticResponse,
        )


class AsyncNames(AsyncAPIResource):
    params: AsyncParams

    def __init__(self, client: AsyncSink) -> None:
        super().__init__(client)
        self.params = AsyncParams(client)

    async def response_shadows_pydantic(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | None | NotGiven = NOT_GIVEN,
    ) -> NameResponseShadowsPydanticResponse:
        """Endpoint with a response model property that would clash with pydantic."""
        return await self._get(
            "/names/response_property_shadows_pydantic",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NameResponseShadowsPydanticResponse,
        )
