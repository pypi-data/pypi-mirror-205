# File generated from our OpenAPI spec by Stainless.

from ..types import github_user_preferences
from .._models import BaseModel

__all__ = ["GithubUser"]


class GithubUser(BaseModel):
    email: str
    """Someone's email address."""

    preferences: github_user_preferences.GithubUserPreferences
