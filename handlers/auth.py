from fastapi import APIRouter, HTTPException
from typing import Annotated

from fastapi.params import Depends

from dependencies import get_auth_service
from exceptions import UserNotFoundException, UserNotCorrectPasswordException
from schemas import UserLoginSchema, UserCreateSchema
from service.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    path="/login",
    response_model=UserLoginSchema
)
async def login(
    body: UserCreateSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    try:
        return auth_service.login(body.username, body.password)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )
    except UserNotCorrectPasswordException as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )
