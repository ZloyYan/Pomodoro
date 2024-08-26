from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    username: str | None = None
    password: str | None = None
    email: str | None = None # str | None = None means that email can be either a string or None. Why None = None and not just None? Because in Pydantic, None is not a valid value for fields that are not optional, so we need to set standart value for optional fields to None to avoid validation errors.
    name: str | None = None  
    google_access_token: str | None = None
    yandex_access_token: str | None = None