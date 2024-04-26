from fastapi import APIRouter
from ..data_management.infomessage import InfoMessage, InfoMessageEnum

tags_metadata = [
    {
        "name": "Health",
        "description": "Endpoint for health checks"
    }
]

router = APIRouter(tags=["Health"])


@router.get("/ping", status_code=200)
def ping() -> InfoMessage:
    """
    Send a ping message to the server to test if API is reachable.
    """
    return InfoMessage(msg=InfoMessageEnum.ok)
