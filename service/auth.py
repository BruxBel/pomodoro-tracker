from dataclasses import dataclass
from datetime import datetime, timedelta, UTC

from jose import jwt, JWTError

from client import GoogleClient
from db import UserModel
from exceptions import UserNotFoundException, UserNotCorrectPasswordException, \
    TokenExpiredException
from exceptions.auth import TokenNotCorrectException
from repository import UserRepository
from schemas import UserLoginSchema

from config import Settings


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient

    def get_google_redirect_url(self):
        return self.settings.google_redirect_url

    def google_auth(self, code: str):
        user_data = self.google_client.get_user_info(code)
        print("Аутентификация через GOOGLE", user_data)

    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    @staticmethod
    def _validate_auth_user(user: UserModel, password: str):
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException

    def generate_access_token(self, user_id: int) -> str:
        expires_date_unix = (
                datetime.now(UTC) +
                timedelta(days=self.settings.JWT_EXPIRE_DAYS)
        ).timestamp()
        token = jwt.encode(
            claims={
                'user_id': user_id,
                'expire': expires_date_unix
            },
            key=self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.JWT_ENCODE_ALGORITHM
        )
        return token

    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(
                token=access_token,
                key=self.settings.JWT_SECRET_KEY,
                algorithms=[self.settings.JWT_ENCODE_ALGORITHM]
            )
        except JWTError:
            raise TokenNotCorrectException
        payload_expire = datetime.fromtimestamp(payload['expire'],
                                                tz=UTC)
        if payload_expire < datetime.now(UTC):
            raise TokenExpiredException
        print(payload['user_id'])
        return payload['user_id']
