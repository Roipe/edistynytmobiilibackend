from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

import models
# import old
from services.auth import AuthServ
from utils.token import Token

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login/openapi', auto_error=False)


def get_logged_in_user_optional(_token: Token, service: AuthServ,
                                authorization: Annotated[str, Depends(oauth_scheme)] = None):
    if authorization is not None:
        validated = _token.validate(authorization)
        if validated['type'] != 'access':
            raise HTTPException(status_code=401, detail='unauthorized')
        user = service.get_user_by_access_token_identifier(validated['sub'])

        if user is None:
            # pass
            raise HTTPException(status_code=401, detail='unauthorized')
        return user
    else:
        return None


def get_logged_in_user(_token: Token, service: AuthServ,
                       authorization: Annotated[str, Depends(oauth_scheme)] = None):
    if authorization is None:
        raise HTTPException(status_code=401, detail='unauthorized')

    validated = _token.validate(authorization)

    if validated['type'] != 'access':
        raise HTTPException(status_code=401, detail='unauthorized')

    user = service.get_user_by_access_token_identifier(validated['sub'])

    if user is None:
        # pass
        raise HTTPException(status_code=401, detail='unauthorized')
    return user


def require_admin(_token: Token, service: AuthServ,
                  authorization: Annotated[str, Depends(oauth_scheme)] = None):
    user = get_logged_in_user(_token, service, authorization)
    if user.auth_role_auth_role.role_name != 'admin':
        raise HTTPException(status_code=403, detail='forbidden')


LoggedInUser = Annotated[models.AuthUser, Depends(get_logged_in_user_optional)]
Admin = Annotated[models.AuthUser, Depends(require_admin)]
