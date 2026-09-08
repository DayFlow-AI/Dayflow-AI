from typing import Annotated

from fastapi import Security
from fastapi_jwt import JwtAuthorizationCredentials

from user.utils import access_security, refresh_security

RefreshCredentials = Annotated[JwtAuthorizationCredentials, Security(refresh_security)]
AccessCredentials = Annotated[JwtAuthorizationCredentials, Security(access_security)]
