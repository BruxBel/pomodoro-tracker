from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    user_id: int
    access_token: str


class UserCreateSchema(BaseModel):
    username: str | None = None
    password: str | None = None
    google_access_token: str | None = None
    email: str | None = None
    name: str | None = None
