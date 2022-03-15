from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from src.config import Config as config
from src.router import router
from src.bot import bot
import time

def create_app():
    # Initialising fastapi app
    app = FastAPI()  
    # Add sqlalchemy as middleware
    app.add_middleware(DBSessionMiddleware, db_url=config.db_url)  
    # Add cors middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in config.origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ) 
    # Include router
    app.include_router(router)
    # Remove current webhook in telegram bot
    bot.remove_webhook()
    # Wait a bit
    time.sleep(5)
    # Set a new webhook
    bot.set_webhook(url=config.webhook_url)
    # Showing info of this new webhook
    print(bot.get_webhook_info())

    return app
