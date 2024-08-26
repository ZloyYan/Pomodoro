
from dataclasses import dataclass

# import requests заменим на библиотеку httpx, которая позволяет работать с http запросами асинхронно
import httpx

from app.users.auth.schema import YandexUserData
from settings import Settings


@dataclass
class YandexClient:
    # settings: Settings
    # async_client: httpx.AsyncClient
    

    # async def get_user_info(self, code: str) -> dict:
    #     access_token = await self.get_user_access_token(code)
    #     async with self.async_client as client:
    #         user_info = await client.get(
    #             'https://login.yandex.ru/info?format=json', 
    #             headers={'Authorization': f'OAuth {access_token}'}
    #         )
    #     return YandexUserData(**user_info.json(), access_token=access_token)



    # async def get_user_access_token(self, code: str) -> str:
    #     async with self.async_client as client:
    #         response = await client.post(
    #             self.settings.YANDEX_TOKEN_URL,
    #             data={
    #             'grant_type': 'authorization_code',
    #             'code': code,
    #             'client_id': self.settings.YANDEX_CLIENT_ID,
    #             'client_secret': self.settings.YANDEX_CLIENT_SECRET,
    #             },
    #             headers={
    #                 'Content-Type': 'application/x-www-form-urlencoded'
    #             }
    #         )

    #         response_data = response.json()
    #     return response_data['access_token']

    settings: Settings
    async_client: httpx.AsyncClient = None

    def __post_init__(self):
        # Создаем экземпляр клиента при создании объекта класса YandexClient
        self.async_client = httpx.AsyncClient()

    async def close(self):
        # Закрываем клиент когда объект уничтожается или когда явно вызывается этот метод
        if self.async_client:
            await self.async_client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def get_user_info(self, code: str) -> dict:
        access_token = await self.get_user_access_token(code)
        # Используем уже существующий экземпляр клиента
        response = await self.async_client.get(
            'https://login.yandex.ru/info?format=json', 
            headers={'Authorization': f'OAuth {access_token}'}
        )
        return YandexUserData(**response.json(), access_token=access_token)

    async def get_user_access_token(self, code: str) -> str:
        # Используем уже существующий экземпляр клиента
        response = await self.async_client.post(
            self.settings.YANDEX_TOKEN_URL,
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'client_id': self.settings.YANDEX_CLIENT_ID,
                'client_secret': self.settings.YANDEX_CLIENT_SECRET,
            },
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        response_data = response.json()
        return response_data['access_token']