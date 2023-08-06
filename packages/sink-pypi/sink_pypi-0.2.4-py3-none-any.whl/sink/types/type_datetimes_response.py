# File generated from our OpenAPI spec by Stainless.

from typing import List, Union, Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["TypeDatetimesResponse"]


class TypeDatetimesResponse(BaseModel):
    required_datetime: datetime

    required_nullable_datetime: Optional[datetime]

    list_datetime: Optional[List[datetime]]

    oneof_datetime: Optional[Union[datetime, int]]

    optional_datetime: Optional[datetime]
