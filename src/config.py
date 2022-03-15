from dotenv import load_dotenv
import os
import json

# Loading .env props
load_dotenv()

# Path to languages.json file
lanuages_path = os.path.join(os.getcwd() + "/src/languages.json")

# Loading languages from .json to a variable
with open(lanuages_path, 'r') as f:
    languages = json.load(f)

class Base:
    debug = False
    env = os.environ.get('ENV')
    db_url = os.environ.get('DB_URL')
    host = '127.0.0.1'
    port = 8000
    languages = languages
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_default_region = 'eu-central-1'

class Prod(Base):
    token = os.environ.get('BOT_TOKEN')
    bot_base_url = f'https://api.telegram.org/bot{token}'
    webhook_url = f"https://api.speakny.ru/bot/{token}/"
    origins = []

class Dev(Base):
    debug = True
    token = os.environ.get('BOT_DEV_TOKEN')
    bot_base_url = f'https://api.telegram.org/bot{token}'
    webhook_url = f"https://2c6f-185-210-142-156.ngrok.io/bot/{token}/"
    origins = ['http://localhost:3000']

if Base.env == 'prod':
    class Config(Prod):
        pass
else:
    class Config(Dev):
        pass