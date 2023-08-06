from math import floor
from typing import Dict
import jwt
from datetime import datetime


def extend_headers(
    original_headers: Dict[str, str], extra_headers: Dict[str, str]
) -> Dict[str, str]:
    return {**original_headers, **extra_headers}


def add_authentication_header(jwt_secret: str, headers: Dict[str, str] = {}):
    nonce = floor(datetime.now().timestamp())

    token = jwt.encode({"nonce": nonce}, jwt_secret)

    updated_headers = extend_headers(headers, {"Authorization": f"Bearer {token}"})

    return updated_headers
