from fastapi import APIRouter, Request
from telebot.types import Update
from .bot import bot
router = APIRouter(
    prefix="/bot",
    tags=["bot"],
    responses={404: {"description": "Not found"}},
)

@router.get('/', status_code=200)
def hello():
    return { "message":"Hi there!" }

@router.post('/', status_code=200)
async def webhook(request:Request):
    data = await request.json()
    if 'update_id' in data:
        update = Update.de_json(data)
        bot.process_new_updates([update])
        return { 'status': 'ok' }
    else:
        return {}