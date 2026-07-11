from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.jwt import SECRET_KEY, ALGORITHM
from app.database.session import get_db
from app.models.user import User


security = HTTPBearer(
    scheme_name="JWT"
)


def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
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

        user = (
            db.query(User)
            .filter(User.username == username)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        return user

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )