from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from app.core.jwt import SECRET_KEY, ALGORITHM


security = HTTPBearer(
    scheme_name="JWT"
)


def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security)
):

    try:

        payload = jwt.decode(
            token.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("username")

        if not username:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return username


    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )