from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

import models
from dependencies import LoggedInUser, RequireLoggedInUser

from dtos.auth import RegisterReq, RegisterRes, LoginReq, LoginRes
from services.auth import AuthServ
from utils.token import Token

router = APIRouter(
    prefix='/api/v1/auth',
    tags=['auth']
)

LoginForm = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.get('/account')
async def get_account(_account: RequireLoggedInUser):
    return _account


@router.post('/register')
async def register(req: RegisterReq, service: AuthServ) -> RegisterRes:
    user = models.AuthUser(**req.model_dump())
    service.register(user)
    return user


@router.post('/login/openapi')
async def login_open_api(req: LoginForm, service: AuthServ, _token: Token) -> LoginRes:
    access_token, user = service.login(req, _token)

    return {'access_token': access_token, 'account': user}


@router.post('/login')
async def login(req: LoginReq, service: AuthServ, _token: Token) -> LoginRes:
    access_token, user = service.login(req, _token)

    return {'access_token': access_token, 'account': user}


@router.post('/logout')
async def login(service: AuthServ, account: LoggedInUser):
    if account is not None:
        service.logout(account)

    return ""
