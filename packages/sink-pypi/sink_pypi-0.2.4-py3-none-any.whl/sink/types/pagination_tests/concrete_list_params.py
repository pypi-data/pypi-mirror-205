# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["ConcreteListParams"]


class ConcreteListParams(TypedDict, total=False):
    limit: int

    my_cursor: str
