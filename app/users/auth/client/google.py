
from dataclasses import dataclass

# import requests заменим на библиотеку httpx, которая позволяет работать с http запросами асинхронно
import httpx

from app.users.auth.schema import GoogleUserData
from settings import Settings


@dataclass
class GoogleClient:
    settings: Settings
    async_client: httpx.AsyncClient 
    

    async def get_user_info(self, code: str) -> dict:
        access_token = await self.get_user_access_token(code)
        async with self.async_client as client:
            user_info = await client.get(
                'https://www.googleapis.com/oauth2/v1/userinfo', 
                headers={'Authorization': f'Bearer {access_token}'}
            )
        return GoogleUserData(**user_info.json(), access_token=access_token)



    async def get_user_access_token(self, code: str) -> str:
        async with self.async_client as client:
            data = {
                'code': code,
                'client_id': self.settings.GOOGLE_CLIENT_ID,
                'client_secret': self.settings.GOOGLE_CLIENT_SECRET,
                'redirect_uri': self.settings.GOOGLE_REDIRECT_URI,
                'grant_type': 'authorization_code'
            }
            response = await client.post(self.settings.GOOGLE_TOKEN_URL, data=data)
        return response.json()['access_token']