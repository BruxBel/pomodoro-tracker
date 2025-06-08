from dataclasses import dataclass
import requests
from config import Settings


@dataclass
class GoogleClient:
    settings: Settings

    def get_user_info(self, code: str) -> dict:
        access_token = self._get_user_access_token(code=code)
        user_info = requests.get(
            "https://openidconnect.googleapis.com/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        print("Информация о пользователе:", user_info.json())
        return user_info.json()

    def _get_user_access_token(self, code: str) -> str:
        data = {
            "code": code,
            "client_id": self.settings.GOOGLE_CLIENT_ID,
            "project_id": self.settings.GOOGLE_PROJECT_ID,
            "client_secret": self.settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": self.settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        response = requests.post(self.settings.GOOGLE_TOKEN_URI, data=data)
        print("Json ответ:", response.json())
        return response.json()['access_token']
