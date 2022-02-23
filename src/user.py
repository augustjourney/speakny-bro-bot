from settings import Config as config
import requests
class User:
    def __init__(self, chat_id, from_user):
        self.chat_id = chat_id
        self.first_name = ""
        self.language_code = "en"
        self.username = ""

        if from_user:
            self.first_name = from_user.first_name
            self.language_code = from_user.language_code
            self.username = from_user.username

    def create_user(self):
        url = f"{config.hello_base_url}/speaknybro/users/new-user"
        data = {
			"chat_id": self.chat_id,
			"username": self.username,
			"first_name": self.first_name,
			"language_code": self.language_code
		}
        res = requests.post(url, json=data)
        res_data = res.json()
        user = res_data['user']
        return user

    def get_user(self):
        url = f"{config.hello_base_url}/speaknybro/users/{self.chat_id}"
        res = requests.get(url)
        data = res.json()
        user = data['user']
        return user

    def get_settings(self):
        user = self.get_user()
        user_lang = 'en'
        language_code = 'en-US'
        native = 'Matthew'
        language = 'english'
        if user and user['settings'] and user['settings']['language_code'] and user['settings']['native']:
            language_code = user['settings']['language_code']
            native = user['settings']['native']
            language = user['settings']['language']
        if user['language_code']:
            user_lang = user['language_code']
        settings = {
            "language_code": language_code, 
            "native": native, 
            "language": language, 
            "user_lang": user_lang
        }
        return settings

    def update_language(self, lang):
        current_lang = self.get_lang(lang)
        url = f"{config.hello_base_url}/speaknybro/users/update-user-language"
        if current_lang:
            data = {
                "chat_id": self.chat_id,
                "language": lang,
                "native": current_lang['natives'][0]['name'],
                "language_code": current_lang['natives'][0]['langcode']
            }
            res = requests.post(url, json=data)
            return res.json()
        else:
            return False

    def update_native(self, native, langcode):
        url = f"{config.hello_base_url}/speaknybro/users/update-user-native"
        data = {
			"chat_id": self.chat_id,
			"native": native,
			"language_code": langcode
		}
        res = requests.post(url, json=data)
        return res.json()
    
    def get_lang(self, lang):
        current_lang = {}
        for l in config.languages:
            if l['slug'] == lang:
                current_lang = l
        return current_lang

    def start_message(self, lang):
        current_lang = self.get_lang(lang)
        msg = f"Hey ✌️\n\nSend me a word or text up to 300 characters. \n\nI'll turn it into lifelike speech and send you back a voice message.\n\nYour current language is {current_lang['name']}. In this language you'll get voice messages. If you want to change the language and native speakers, use the command — /settings"
        if self.language_code == 'ru':
            msg = f"Привет ✌️\n\nПришлите мне слово или текст до 300 символов. \n\nЯ преобразую его в естественную речь и в ответ пришлю голосовое сообщение.\n\nВаш текущий язык — {current_lang['name']}. На этом языке буду присылать голосовые. Если хотите поменять язык и носителей, используйте комманду — /settings"
        return msg
