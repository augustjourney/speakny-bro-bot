from dotenv import load_dotenv
import os
import json

load_dotenv()
print(os.getcwd())
lanuages_path = os.path.join(os.getcwd() + "/src/languages.json")
with open(lanuages_path, 'r') as f:
    languages = json.load(f)

class Base:
    debug = False
    env = os.environ.get('ENV')
    db_url = os.environ.get('DB_URL')
    host = '127.0.0.1'
    port = 5000
    languages = languages
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_default_region = 'eu-central-1'
    origins = ['http://localhost', 'http://localhost:3000']

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
    webhook_url = "https://9039-185-210-142-14.ngrok.io/bot/"

if Base.env == 'prod':
    class Config(Prod):
        pass
else:
    class Config(Dev):
        pass