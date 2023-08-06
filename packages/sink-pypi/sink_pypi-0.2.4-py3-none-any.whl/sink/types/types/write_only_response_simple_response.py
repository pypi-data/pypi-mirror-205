# File generated from our OpenAPI spec by Stainless.

from typing import Optional

from ..._models import BaseModel

__all__ = ["WriteOnlyResponseSimpleResponse"]


class WriteOnlyResponseSimpleResponse(BaseModel):
    should_never_show_up: Optional[str]
    """
    This should never be generated as it is a `writeOnly` property used in a
    response type.
    """
