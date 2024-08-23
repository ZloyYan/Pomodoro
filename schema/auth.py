from pydantic import BaseModel, Field


class GoogleUserData(BaseModel):
    id: int
    email: str
    verified_email: bool
    name: str
    access_token: str


class YandexUserData(BaseModel):
    id: str
    login: str
    name: str = Field(alias="real_name") # alias is written to use the field name "real_name" without changing the field name in the schema
    email: str = Field(alias="default_email") # alias is written to use the field name "default_email" but to keep field standardized as "email"
    access_token: str