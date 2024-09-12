import pytest
from jose import jwt
from datetime import datetime as dt, timedelta
import datetime


from app.users.auth.service import AuthService
from settings import Settings


pytestmark = pytest.mark.asyncio # mark the test as an asynchronous test

async def test_get_google_rediect_url__success(auth_service: AuthService, settings: Settings):
    settings_google_redirect_url = settings.google_redirect_url

    auth_service_google_redirect_url = auth_service.get_google_redirect_url()

    assert settings_google_redirect_url == auth_service_google_redirect_url

async def test_get_yandex_rediect_url__success(auth_service: AuthService, settings: Settings):
    settings_yandex_redirect_url = settings.yandex_redirect_url

    auth_service_yandex_redirect_url = auth_service.get_yandex_redirect_url()

    assert settings_yandex_redirect_url == auth_service_yandex_redirect_url

async def test_get_google_rediect_url__fail(auth_service: AuthService):
    settings_google_redirect_url = "https://fake_google_redirect_url.com"

    auth_service_google_redirect_url = auth_service.get_google_redirect_url()

    assert settings_google_redirect_url != auth_service_google_redirect_url    


async def test_generate_access_token__success(auth_service: AuthService, settings: Settings):
    user_id = str(1)

    access_token = auth_service.generate_access_token(user_id=user_id)
    decode_access_token = jwt.decode(
        access_token, 
        settings.JWT_SECRET_KEY, 
        algorithms=[settings.JWT_ENCODE_ALGORITHM]
    )
    decoded_user_id = decode_access_token['user_id']
    decoded_token_expire = dt.fromtimestamp(decode_access_token['expire'], tz=datetime.timezone.utc)

    assert user_id == decoded_user_id
    assert (decoded_token_expire - dt.now(tz=datetime.timezone.utc)) > datetime.timedelta(days=6)


async def test_get_user_id_from_access_token__success(auth_service: AuthService, settings: Settings):   
    user_id = str(1)

    access_token = auth_service.generate_access_token(user_id=user_id)
    user_id_from_access_token = auth_service.get_user_id_from_access_token(access_token=access_token)

    assert user_id == user_id_from_access_token