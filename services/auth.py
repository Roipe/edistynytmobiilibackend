import datetime
import time
import uuid
from typing import Annotated

from fastapi import HTTPException, Depends
from passlib.context import CryptContext

import models
from dtos.auth import LoginReq
from services.base import BaseService
from utils.token import Token

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class AuthService(BaseService):
    def __init__(self, db: models.Db):
        super(AuthService, self).__init__(db)

    def register(self, user: models.AuthUser):
        role = self.db.query(models.AuthRole).filter(models.AuthRole.role_name == 'user').first()
        if role is None:
            raise HTTPException(status_code=404, detail='role not found')
        check = self.db.query(models.AuthUser).filter(models.AuthUser.username == user.username)
        if check is not None:
            raise HTTPException(status_code=409, detail='user already exists')
        user.created_at = datetime.datetime.now()
        user.auth_role_auth_role = role
        user.password = bcrypt_context.hash(user.password)
        self.db.add(user)
        self.db.commit()

    def get_user_by_access_token_identifier(self, sub):

        user = self.db.query(models.AuthUser).filter(models.AuthUser.access_jti == sub).first()
        return user

    def logout(self, account):
        account.access_jti = None
        self.db.commit()

    def login(self, req: LoginReq, _token: Token):

        user = self.db.query(models.AuthUser).filter(models.AuthUser.username == req.username).first()
        if user is None:
            raise HTTPException(status_code=404, detail='user not found1')
        valid = bcrypt_context.verify(req.password, user.password)
        if not valid:
            raise HTTPException(status_code=404, detail='user not found2')

        access_token_sub = str(uuid.uuid4())

        access_token = _token.create({'type': 'access', 'sub': access_token_sub, 'exp': None, 'csrf': None})

        user.access_jti = access_token_sub

        self.db.commit()

        return access_token, user


def get_service(db: models.Db):
    return AuthService(db)


AuthServ = Annotated[AuthService, Depends(get_service)]
