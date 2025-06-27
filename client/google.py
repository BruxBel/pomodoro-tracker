from dataclasses import dataclass
import httpx
from config import Settings
from schemas import GoogleUserData


@dataclass
class GoogleClient:
    settings: Settings

    async def get_user_info(self, code: str) -> GoogleUserData:
        access_token = await self._get_user_access_token(code=code)
        async with httpx.AsyncClient() as client:
            user_info = await client.get(
                "https://openidconnect.googleapis.com/v1/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
        return GoogleUserData(**user_info.json(), access_token=access_token)

    async def _get_user_access_token(self, code: str) -> str:
        data = {
            "code": code,
            "client_id": self.settings.GOOGLE_CLIENT_ID,
            "project_id": self.settings.GOOGLE_PROJECT_ID,
            "client_secret": self.settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": self.settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.settings.GOOGLE_TOKEN_URI,
                data=data
            )
        return response.json()['access_token']
