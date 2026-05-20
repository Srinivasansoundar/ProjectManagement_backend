from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.utils.decode_token import decode_token
from src.core.exception.custom_exception import (
    ForbiddenException
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def require_roles(*allowed_roles):

    async def role_checker(
        token: str = Depends(oauth2_scheme)
    ):

        payload = decode_token(token)

        user_role = payload.get("role")

        if user_role not in allowed_roles:

            raise ForbiddenException(
                "You do not have permission to perform this action"
            )

        return payload

    return role_checker