from settings import Config as config
import flask
import telebot
import time
from user import User
from voiceover import Voiceover
from keyboard import Keyboard

app = flask.Flask(__name__)
bot = telebot.TeleBot(config.token)

# Set bot commands
# Будет круто добавить еще команду — info, courses, telegram channel
bot.set_my_commands(commands=[
    telebot.types.BotCommand("/start", "начать"),
    telebot.types.BotCommand("/settings", "поменять язык, поменять носителя")
], language_code='ru')
bot.set_my_commands(commands=[
    telebot.types.BotCommand("/start", "start"),
    telebot.types.BotCommand("/settings", "change the language, change the native")
])

# Handle start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    usr = User(message.chat.id, message.from_user)
    user = usr.create_user()
    lang = user['settings']['language']
    msg = usr.start_message(lang)
    bot.send_message(message.chat.id, msg)

# Handle settings command
@bot.message_handler(commands=['settings'])
def send_settings(message):
    usr = User(message.chat.id, message.from_user)
    settings  = usr.get_settings()
    kb = Keyboard(settings['native'], settings['language'], settings['user_lang'])
    keyboard = kb.get_settings()
    text = kb.get_settings_text()
    bot.send_message(message.chat.id, text, reply_markup=keyboard)

# Update settings message on getting callback query
def update_settings(message):
    usr = User(message.chat.id, message.from_user)
    settings  = usr.get_settings()
    kb = Keyboard(settings['native'], settings['language'], settings['user_lang'])
    keyboard = kb.get_settings()
    text = kb.get_settings_text()
    bot.edit_message_text(chat_id = message.chat.id, message_id = message.id, text = text, reply_markup = keyboard)


# Handle text message to turn it into speech
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    usr = User(message.chat.id, message.from_user)
    settings = usr.get_settings()
    voiceover = Voiceover(message.chat.id, message.text, settings['language_code'], settings['native'])
    audio = voiceover.get_audio()
    if audio:
        voiceover.send_audio()
    voiceover.delete_audio(audio + '.opus')
    voiceover.create_speech()
    # Записать в базу данных это сообщение


# Handle callback query
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    chat_id = call.message.chat.id
    msg_id = call.message.id
    usr = User(chat_id, None)
    settings  = usr.get_settings()
    kb = Keyboard(settings['native'], settings['language'], settings['user_lang'])
    if call.data == 'change_language':
        text = kb.get_langs_text()
        keyboard = kb.get_languages()
        bot.edit_message_text(chat_id = chat_id, message_id = msg_id, text = text, reply_markup = keyboard)
    elif call.data == 'change_native':
        text = kb.get_natives_text()
        keyboard = kb.get_natives()
        bot.edit_message_text(chat_id = chat_id, message_id = msg_id, text = text, reply_markup = keyboard)
    elif call.data == 'back_to_settings':
        keyboard = kb.get_settings()
        text = kb.get_settings_text()
        bot.edit_message_text(chat_id = chat_id, message_id = msg_id, text = text, reply_markup = keyboard)
    elif call.data == 'save_settings':
        text = kb.get_saved_settings_text()
        bot.edit_message_text(chat_id = chat_id, message_id = msg_id, text = text)
    elif call.data.startswith('changetolanguage'):
        lang = call.data.split('-',1)[1]
        res = usr.update_language(lang)
        text = kb.get_lang_changed_text()
        bot.answer_callback_query(call.id, text=text)
        update_settings(call.message)
    elif call.data.startswith('changetonative'):
        cb = call.data.split('-',1)[1]
        data = cb.split('/')
        native = data[0]
        langcode = data[1]
        text = kb.get_native_changed_text()
        res = usr.update_native(native, langcode)
        bot.answer_callback_query(call.id, text=text)
        update_settings(call.message)
 

def create_app():
    app = flask.Flask(__name__)
    bot.remove_webhook()
    time.sleep(5)
    try:
        bot.set_webhook(url=config.webhook_url)
        print(bot.get_webhook_info())
    except Exception as e:
        print(e)
    
    # Empty webserver index, return nothing, just http 200
    @app.route('/', methods=['GET', 'HEAD'])
    def index():
        return 'Ok'

    # Process webhook calls
    @app.route('/webhook', methods=['POST'])
    def webhook():
        if flask.request.headers.get('content-type') == 'application/json':
            json_string = flask.request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            print('not made it')
            flask.abort(403)
    
    return app

if __name__ == '__main__':
    if config.env == 'dev':
        print("Starting bot...")
        try:
            bot.infinity_polling()
        except Exception as e:
            print(e)