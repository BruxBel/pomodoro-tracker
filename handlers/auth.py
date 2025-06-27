from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.responses import RedirectResponse

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


@router.get(
    path="/google/login",
    response_class=RedirectResponse
)
async def google_login(
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    redirect_url = auth_service.get_google_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)


@router.get(
    path="/google/auth"
)
async def google_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    code: str
):
    return await auth_service.google_auth(code=code)
