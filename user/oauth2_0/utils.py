from httpx import AsyncClient
from joserfc import jwt, jwk
from user.oauth2_0.schemas import UserOauthInfo


async def get_google_profile(id_token: str) -> UserOauthInfo:
    async with AsyncClient() as c:
        certs = (await c.get("https://www.googleapis.com/oauth2/v3/certs")).json()
    claims = jwt.decode(id_token, jwk.KeySet(certs)).claims
    return UserOauthInfo.model_validate(claims)
