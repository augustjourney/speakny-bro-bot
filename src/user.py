from .config import Config as config
from .users_repo import UsersRepo as _users

class User:
    def __init__(self, chat_id, from_user):
        # User's chat_id
        self.chat_id = chat_id
        # User's first name
        self.first_name = ""
        # User's language code of telegram client interface
        self.language_code = "en"
        # User's username in telegram, may be empty
        self.username = ""

        if from_user:
            self.first_name = from_user.first_name
            self.language_code = from_user.language_code
            self.username = from_user.username

    # Create a new user
    def create_user(self):
        # Find this user
        user = self.get_user()
        # Create if not exists
        if user == None:
            # Default user's settings
            settings = {
                'language': 'english',
                'native': 'Kimberly',
                'language_code': 'en-US'
            }
            # Creating the user
            created_user = _users.create_user(self.chat_id, self.username, self.first_name, self.language_code, settings)
            
            # If created — return it. Otherwise — return None
            if created_user:
                return created_user
            return None
        
        # Return the user if already exists without creating
        return user

    # Get the user from the database
    def get_user(self):
        return _users.get_user(self.chat_id)

    # Getting the latest user's settings
    def get_settings(self):
        # Getting this user from the database
        user = self.get_user()

        # Initial settings that a new user is created with
        default_settings = {
            "language_code": 'en-US', 
            "native": 'Matthew', 
            "language": 'english', 
            "user_lang": 'en'
        }
        
        # If this user exists and has settings, return them
        if user and 'settings' in user:
            return {
                "language_code": user['settings']['language_code'], 
                "native": user['settings']['native'], 
                "language": user['settings']['language'], 
                "user_lang": user['language_code']
            }
        
        return default_settings

    # Getting new user's language and saving it to the database
    def update_language(self, lang):
        # Getting from languages list in config file
        current_lang = self.get_lang(lang)

        if current_lang:
            # After getting the language, settings will be like this
            settings = {
                "language_code": current_lang['natives'][0]['langcode'],
                "native": current_lang['natives'][0]['name'],
                "language": lang
            }
            # Updating and returning this user with basic info
            return _users.update_user_settings(self.chat_id, settings)
        
        return False

    # Getting new user's native and saving it to the database
    def update_native(self, native, langcode):
        # Getting newest settings of user
        settings = self.get_settings()

        # Updated settings object
        updated_settings = {
            "language_code": langcode,
            "native": native,
            "language": settings['language']
        }
        
        # Updating and returning this user with basic info
        return _users.update_user_settings(self.chat_id, updated_settings)
    
    def get_lang(self, lang):
        current_lang = {}
        # Going through list of languages from config file
        # And finding the one where slug is equal to the gotten lang
        for l in config.languages:
            if l['slug'] == lang:
                current_lang = l
        # This language will have name, slug, natives list, icon, language code
        return current_lang

    def start_message(self, lang):
        # Getting the language from the config file languages list 
        # It has a name of a language, not just a slug
        current_lang = self.get_lang(lang)
        
        # The default message for everyone
        msg = f"Hey ✌️\n\nSend me a word or text up to 300 characters. \n\nI'll turn it into lifelike speech and send you back a voice message.\n\nYour current language is {current_lang['name']}. In this language you'll get voice messages. If you want to change the language and native speakers, use the command — /settings"
        
        # If the user's telegram language is Russian, the message will be:
        if self.language_code == 'ru':
            msg = f"Привет ✌️\n\nПришлите мне слово или текст до 300 символов. \n\nЯ преобразую его в естественную речь и в ответ пришлю голосовое сообщение.\n\nВаш текущий язык — {current_lang['name']}. На этом языке буду присылать голосовые. Если хотите поменять язык и носителей, используйте комманду — /settings"
        
        return msg
