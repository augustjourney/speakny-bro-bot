from .config import Config as config
from sqlalchemy import create_engine

engine = create_engine(config.db_url)
connection = engine.connect()