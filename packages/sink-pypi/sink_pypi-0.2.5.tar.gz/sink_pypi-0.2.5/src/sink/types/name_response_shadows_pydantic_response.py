# File generated from our OpenAPI spec by Stainless.

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["NameResponseShadowsPydanticResponse"]


class NameResponseShadowsPydanticResponse(BaseModel):
    parse_raw_: str = FieldInfo(alias="parse_raw")
