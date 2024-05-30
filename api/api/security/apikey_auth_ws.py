import secrets

from fastapi import (
    status,
    WebSocketException, Query
)
from typing import Annotated


class APIKeyAuthWS:

    _api_key_header_name = "x-api-key"

    def __init__(self):
        """Initialize instance without valid key specification"""
        self.valid_key = None

    def __call__(
            self, x_api_key: Annotated[str, Query()] = ""
    ) -> bool:
        """
        Verify that an api key passed in a header matches the registered
        valid_key.
        """
        if self.valid_key is None:
            # Instance not properly set up
            raise AttributeError("No valid_key specified.")
        keys_match = secrets.compare_digest(self.valid_key, x_api_key)
        if not keys_match:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
        return True
