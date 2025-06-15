from pydantic import BaseModel


class GoogleUserData(BaseModel):
    sub: int
    name: str
    access_token: str
    email: str
    email_verified: bool
