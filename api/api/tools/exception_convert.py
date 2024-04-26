from fastapi import status, HTTPException
from ..database.database import DatabaseError


def database_error_to_http_exception(e: DatabaseError) -> None:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"DatabaseError: {e.backend_name}: {e.message}"
    )
