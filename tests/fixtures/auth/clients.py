from dataclasses import dataclass
import httpx
import pytest
from settings import Settings


@dataclass
class FakeGoogleClient:
    settings: Settings
    async_client: httpx.AsyncClient 
    

    async def get_user_info(self, code: str) -> dict:
        access_token = await self.get_user_access_token(code)
        return {"face_access_token": access_token}



    async def get_user_access_token(self, code: str) -> str:
        return f"fake_access_token {code}"
    

@dataclass
class FakeYandexClient:
    settings: Settings
    async_client: httpx.AsyncClient = None


    async def get_user_info(self, code: str) -> dict:
        access_token = await self.get_user_access_token(code)
        return {"face_access_token": access_token}
    
    async def get_user_access_token(self, code: str) -> str:
        return f"fake_access_token {code}"


@pytest.fixture
def google_client():
    return FakeGoogleClient(settings=Settings(), async_client=httpx.AsyncClient())

@pytest.fixture
def yandex_client():
    return FakeYandexClient(settings=Settings(), async_client=httpx.AsyncClient())




    