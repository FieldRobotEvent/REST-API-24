import secrets

from fastapi import Depends, status, HTTPException
from fastapi.security import APIKeyHeader


class APIKeyAuth:

    _api_key_header_name = "x-api-key"

    def __init__(self):
        """Initialize instance without valid key specification"""
        self.valid_key = None

    def __call__(
            self, key: str = Depends(APIKeyHeader(name=_api_key_header_name))
    ) -> None:
        """
        Verify that an api key passed in a header matches the registered
        valid_key.
        """
        if self.valid_key is None:
            # Instance not properly set up
            raise AttributeError("No valid_key specified.")
        keys_match = secrets.compare_digest(self.valid_key, key)
        if not keys_match:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate api key.",
                headers={"WWW-Authenticate": self._api_key_header_name},
            )
        return True
