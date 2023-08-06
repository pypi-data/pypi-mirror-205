# File generated from our OpenAPI spec by Stainless.

from ..types import custom_api_status_message
from .._models import BaseModel

__all__ = ["APIStatus"]


class APIStatus(BaseModel):
    message: custom_api_status_message.CustomAPIStatusMessage
