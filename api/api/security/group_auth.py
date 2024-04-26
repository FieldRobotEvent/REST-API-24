import secrets

from fastapi import Depends, status, HTTPException
from fastapi.security import APIKeyHeader


class GroupAuth:

    _api_key_header_name = "x-api-key"

    def __init__(self):
        """Initialize instance without valid group specification"""
        self.valid_groups = None

    def __call__(
            self, key: str = Depends(APIKeyHeader(name=_api_key_header_name))
    ) -> str | None:
        """
        Verify that an api key passed in a header matches the registered
        valid_key.
        """
        if not self.valid_groups:
            # Instance not properly set up
            raise AttributeError("No valid_groups specified.")
        for valid_group in self.valid_groups:
            key_match = secrets.compare_digest(valid_group.apikey, key)
            if key_match:
                return valid_group.name
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate api key.",
            headers={"WWW-Authenticate": self._api_key_header_name},
        )
