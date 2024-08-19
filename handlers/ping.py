from fastapi import APIRouter


router = APIRouter(prefix='/ping', tags=['ping-app, ping-db'])  # group API endpoints under "ping" tag


@router.get('/app')
async def ping_app(self):
    return {"message": "pong"}

@router.get('/db')
async def ping_db(self):
    return {"message": "pong"}

