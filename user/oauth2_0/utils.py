from httpx import AsyncClient

from user.oauth2_0.schemas import UserOauthInfo


async def get_google_profile(access_token: str) -> UserOauthInfo:
    async with AsyncClient() as c:
        resp = await c.get(
            "https://openidconnect.googleapis.com/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        data = resp.json()
    return UserOauthInfo.model_validate(data)
