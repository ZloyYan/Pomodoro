from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from fastapi.responses import RedirectResponse

from schema import UserLoginSchema, UserCreateSchema
from service import AuthService
from dependency import get_auth_service
from exceptions import UserNotFoundException, UserNotCorrectPasswordException


router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login', response_model=UserLoginSchema)
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
    "/login/google",
    response_class=RedirectResponse
)
async def google_login(
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    redirect_url =  auth_service.get_google_redirect_url()
    print(redirect_url)  # Выводим ссылку для перенап
    return RedirectResponse(url=redirect_url)


# Хэндлер, который возвращает код авторизации через Google
@router.get(
    "/google"
)
async def google_auth(
    code: str,
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    return auth_service.google_auth(code=code)




@router.get(
    "/login/yandex",
    response_class=RedirectResponse
)
async def yandex_login(
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    redirect_url =  auth_service.get_yandex_redirect_url()
    print(redirect_url)  # Выводим ссылку для перенап
    return RedirectResponse(url=redirect_url)



@router.get(
    "/yandex",
)
async def yandex_auth(
    code: str,
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    return auth_service.yandex_auth(code=code)
