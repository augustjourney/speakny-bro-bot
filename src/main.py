from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from .config import Config as config
from .router import router
from .bot import bot
import time

def create_bot():
    app = FastAPI()
    
    app.add_middleware(DBSessionMiddleware, db_url=config.db_url)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in config.origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
        
    app.include_router(router)

    bot.remove_webhook()
    time.sleep(5)
    bot.set_webhook(url=config.webhook_url)
    print(bot.get_webhook_info())

    return app