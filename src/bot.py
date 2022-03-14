from .config import Config as config
import telebot
from .user import User
from .keyboard import Keyboard
from .speech import Speech
# Initialising the bot instance
bot = telebot.TeleBot(config.token)

# Set bot commands if user's telegram is in Russian
bot.set_my_commands(commands=[
    telebot.types.BotCommand("/start", "начать"),
    telebot.types.BotCommand("/settings", "поменять язык, поменять носителя")
], language_code='ru')

# Set bot commands if user's telegram is not in Russian
bot.set_my_commands(commands=[
    telebot.types.BotCommand("/start", "start"),
    telebot.types.BotCommand("/settings", "change the language, change the native")
])

# Handle start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Initialising the user instance
    usr = User(message.chat.id, message.from_user)
    # Creating a new user or just getting if exists
    user = usr.create_user()
    # Getting the user's language from settings
    lang = user['settings']['language']
    # Getting the message text based on user's language
    msg = usr.start_message(lang)
    # Sending the message
    bot.send_message(message.chat.id, msg)

# Handle settings command
@bot.message_handler(commands=['settings'])
def send_settings(message):
    # Initialising the user instance
    usr = User(message.chat.id, message.from_user)
    # Getting user's settings
    settings = usr.get_settings()
    # Initialising the keyaboard instance
    kb = Keyboard(settings['native'], settings['language'], settings['user_lang'])
    # Creating keyaboard buttons to send
    keyboard = kb.get_settings()
    # Getting text of message
    text = kb.get_settings_text()
    # Sending the message
    bot.send_message(message.chat.id, text, reply_markup=keyboard)

# Update settings message after changing settings
"""
    When user changes their language or native in settings
    We save the changed settings in the database
    And then send to the user the settings from beginning
    And they just get the settings keyboard back.
    So they don't have to get back manually
"""
def update_settings(message):
    # Initialising the user instance
    usr = User(message.chat.id, message.from_user)
    # Getting the user's settings
    settings  = usr.get_settings()
    # Initialising the keyaboard instance
    kb = Keyboard(settings['native'], settings['language'], settings['user_lang'])
    # Creating keyaboard buttons to send
    keyboard = kb.get_settings()
    # Getting the settings text which will be the message
    text = kb.get_settings_text()
    # Editing the current message with new one
    bot.edit_message_text(chat_id = message.chat.id, message_id = message.id, text = text, reply_markup = keyboard)

# Handle callback query
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # Saving chat id and message id to the variables
    chat_id = call.message.chat.id
    msg_id = call.message.id
    # Initialising the user instance
    usr = User(chat_id, None)
    # Getting user's settings
    settings  = usr.get_settings()
    # Initialising the keyaboard instance
    kb = Keyboard(settings['native'], settings['language'], settings['user_lang'])
    
    # When user wants to change the language
    # Sending the keyboard with list of languages to choose the language
    if call.data == 'change_language':
        # Getting text for message
        text = kb.get_langs_text()
        # Getting keyboard with the list of languages
        keyboard = kb.get_languages()
        # Updating this message with the new keyboard
        bot.edit_message_text(chat_id = chat_id, message_id = msg_id, text = text, reply_markup = keyboard)
    
    # When user wants to change the native
    # Sending the keyboard with list of natives to choose the native
    elif call.data == 'change_native':
        # Getting text for message
        text = kb.get_natives_text()
        # Getting keyboard with the list of natives
        keyboard = kb.get_natives()
        # Updating this message with the new keyboard
        bot.edit_message_text(chat_id = chat_id, message_id = msg_id, text = text, reply_markup = keyboard)
    
    # When user wants to get back to the beginning of settings
    # Sending the keyboard with settings
    elif call.data == 'back_to_settings':
        # Getting the settings keyboard
        keyboard = kb.get_settings()
        # Getting the text for message
        text = kb.get_settings_text()
        # Answer the cb query to stop displaying the progress in user's telegram
        bot.answer_callback_query(call.id, text=text)
        # Editing the message with the new keyboard
        bot.edit_message_text(chat_id = chat_id, message_id = msg_id, text = text, reply_markup = keyboard)
    
    # After changing settings is done show the message about it
    elif call.data == 'save_settings':
        # Getting the message text based on user's interface language
        text = kb.get_saved_settings_text()
        # Answer the cb query to stop displaying the progress in user's telegram
        bot.answer_callback_query(call.id, text=text)
        # Editing the same message where the settings keyboard was
        bot.edit_message_text(chat_id = chat_id, message_id = msg_id, text = text)
    
    # Handling the change of user's language in settings
    elif call.data.startswith('changetolanguage'):
        # Getting the language to change to from the callback query text
        lang = call.data.split('-',1)[1]
        # Updating the language in the database
        usr.update_language(lang)
        # Getting the text for message to inform about language changing
        text = kb.get_lang_changed_text()
        # Answer the cb query to stop displaying the progress in user's telegram
        bot.answer_callback_query(call.id, text=text)
        # Going back to all settings
        update_settings(call.message)
    
    # Handling the change of user's native in settings
    elif call.data.startswith('changetonative'):
        # Getting the native to change to from the callback query text
        # CB query text will be like this: changetonative-Nicole/en-AU
        # Here's the structure — changetonative-{Native}/{Langcode}
        cb = call.data.split('-',1)[1]
        data = cb.split('/')
        native = data[0]
        langcode = data[1]
        # Getting the message text
        text = kb.get_native_changed_text()
        # Updating user settings with new native
        usr.update_native(native, langcode)
        # Answer the cb query to stop displaying the progress in user's telegram
        bot.answer_callback_query(call.id, text=text)
        # Going back to all settings
        update_settings(call.message)


# Handle text message to turn it into speech
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    # Initialising the user instance
    usr = User(message.chat.id, message.from_user)
    # Getting the user's settings
    settings = usr.get_settings()
    # Initialising the speech instance
    speech = Speech(message.chat.id, message.text, settings['language_code'], settings['native'])
    # Converting text to audio
    audio = speech.get_audio()
    if audio:
        # Sending audio to user
        speech.send_audio()
    # Deleting audio file after sending it to the user
    speech.delete_audio(audio + '.opus')
    # Adding this speech to the database
    speech.create_speech()