from dataclasses import dataclass

from repository import UserRepository
from schemas import UserLoginSchema, UserCreateSchema
from service.auth import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    def create_user(self, username: str, password: str) -> UserLoginSchema:
        create_user_data = UserCreateSchema(
            username=username,
            password=password
        )
        user = self.user_repository.create_user(create_user_data)
        access_token = self.auth_service.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)
