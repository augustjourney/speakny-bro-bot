from fastapi import APIRouter, Request
from telebot.types import Update
from src.bot import bot
from src.config import Config as config

# Initialising router with prefix bot
router = APIRouter(
    prefix="/bot",
    tags=["bot"],
    responses={404: {"description": "Not found"}},
)

@router.get('/', status_code=200)
def hello():
    return { "message":"Hi there!" }

@router.post('/' + config.token + '/', status_code=200)
async def webhook(request:Request):
    # Getting data from request
    data = await request.json()
    """
        When telegram sends update
        There should be update_id in the request object
    """
    if 'update_id' in data:
        # Using de_json function from telebot.Update lib
        # It just serialize the request data to turn it into update for bot
        update = Update.de_json(data)
        # Pass this update to bot
        bot.process_new_updates([update])
        
    return { 'status': 'ok' }