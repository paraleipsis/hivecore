from typing import Dict
from datetime import datetime, timedelta

from jose import jwt, JWTError
from auth.auth_config import (ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES)
from modules.exc.exceptions.exceptions_node_auth import NodeAuthError
from node_manager.schemas.schemas_node_auth import TokenData


def create_access_token(
        data: Dict,
        expire: int = ACCESS_TOKEN_EXPIRE_MINUTES
):
    to_encode = data.copy()

    if expire > 0:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update(
            {
                "expire": expire
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
) -> TokenData:
    try:
        payload = jwt.decode(
            token=token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        node_name = payload.get("node_name")
        server_pub_key = payload.get("server_pub_key")
        if node_name is None or server_pub_key is None:
            raise NodeAuthError('Invalid Token data')
    except JWTError:
        raise NodeAuthError('Invalid Token')

    return TokenData(
        node_name=node_name,
        server_pub_key=server_pub_key
    )
