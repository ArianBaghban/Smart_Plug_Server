from datetime import datetime, timedelta
from jose import jwt


SECRET_KEY = "smart_plug_secret_key"
ALGORITHM = "HS256"


def create_token(data: dict):

    payload = data.copy()

    expire = datetime.utcnow() + timedelta(hours=24)

    payload["exp"] = expire

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )