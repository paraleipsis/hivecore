from typing import Dict
from datetime import datetime, timedelta

from jose import jwt, JWTError
from auth.auth_config import (ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES)
from modules.exc.exceptions.exceptions_node_auth import NodeAuthError


def create_access_token(
        data: Dict,
        expire: int = ACCESS_TOKEN_EXPIRE_MINUTES
):
    to_encode = data.copy()

    if expire > 0:
        expire = datetime.now() + timedelta(minutes=expire)
        to_encode.update(
            {
                "expire": int(expire.timestamp())
            }
        )

    encoded_jwt = jwt.encode(
        claims=to_encode,
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


def verify_node_access_token(
        token: str
) -> bool:
    try:
        payload = jwt.decode(
            token=token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        node_name = payload.get("node_name")
        server_pub_key = payload.get("server_pub_key")
        expire = payload.get("expire")
        if node_name is None or server_pub_key is None:
            raise NodeAuthError('Invalid Token data')
        if expire:
            current_time = datetime.now()
            if int(current_time.timestamp()) > int(expire):
                raise NodeAuthError('Token has expired')
    except JWTError:
        raise NodeAuthError('Invalid Token')

    return True
