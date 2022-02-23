from dotenv import load_dotenv
import os
import json

load_dotenv()

lanuages_path = os.path.join(os.getcwd() + "/languages.json")
languages_file = open(lanuages_path)
languages = json.load(languages_file)
languages_file.close()

class Base:
    debug = False
    env = os.environ.get('ENV')
    host = '127.0.0.1'
    port = 5000
    languages = languages
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_default_region = 'eu-central-1'

class Prod(Base):
    token = os.environ.get('BOT_TOKEN')
    base_url = os.environ.get('SPEAKNY_API')
    bot_base_url = f'https://api.telegram.org/bot{token}'
    webhook_url = f"{base_url}/bot/speaknybro/webhook"
    hello_base_url = f"{base_url}/hello"

class Dev(Base):
    debug = True
    token = os.environ.get('BOT_DEV_TOKEN')
    bot_base_url = f'https://api.telegram.org/bot{token}'
    hello_base_url = "http://localhost:4001/hello"

if Base.env == 'prod':
    class Config(Prod):
        pass
else:
    class Config(Dev):
        pass