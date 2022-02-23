from telebot.types import InlineKeyboardButton as btn
from telebot.types import InlineKeyboardMarkup as markup
from settings import Config as config
class Keyboard:
    def __init__(self, native, language, user_lang):
        self.native = native
        self.language = language
        self.user_lang = user_lang
    
    def get_settings(self):
        keyboard = markup()
        current_lang = self.get_lang()
        language = self.lang_btn(current_lang)
        keyboard.row(btn(text=language, callback_data='change_language'))
        native = self.native_btn()
        keyboard.row(btn(text = native, callback_data='change_native'))
        save_text = self.get_save_text()
        keyboard.row(btn(text=save_text, callback_data='save_settings'))
        return keyboard
    
    def lang_btn(self, current_lang):
        icon = f"{current_lang['icon']} " if current_lang['icon'] else ''
        name = f"[{current_lang['name']}]" if current_lang['name'] else ''
        text = self.get_change_language_text()
        return f"{icon} {text} {name}"
    
    def native_btn(self):
        name = f"[{self.native}]" if self.native else ''
        text = self.get_change_native_text()
        return f"👨‍🦰 {text} {name}"

    def get_lang(self):
        current_lang = config.languages[0]
        for lang in config.languages:
            if lang['slug'] == self.language:
                current_lang = lang
        return current_lang

    def get_languages(self):
        keyboard = markup()
        n = 2
        langs = config.languages
        langs_list = [langs[i:i + n] for i in range(0, len(langs), n)] 
        for lang in langs_list:            
            row = []
            for l in lang:
                text = f"{l['icon']} {l['name']}"
                cb_data = f"changetolanguage-{l['slug']}"
                col = btn(text = text, callback_data = cb_data)
                row.append(col)
            keyboard.row(*row)
        
        back_text = self.get_back_text()
        back = btn(text = back_text, callback_data = "back_to_settings")
        keyboard.row(back)
        return keyboard
    
    def get_natives(self):
        keyboard = markup()
        current_lang = self.get_lang()
        n = 2
        natives = current_lang['natives']
        if len(natives) == 3:
            n = 3
        natives_list = [natives[i:i + n] for i in range(0, len(natives), n)] 
        for native in natives_list:
            row = []
            for n in native:
                text = f"{n['country']} {n['name']}"
                cb_data = f"changetonative-{n['name']}/{n['langcode']}"
                col = btn(text = text, callback_data = cb_data)
                row.append(col)
            keyboard.row(*row)
        back_text = self.get_back_text()
        back = btn(text = back_text, callback_data = "back_to_settings")
        keyboard.row(back)
        return keyboard

    def get_settings_text(self):
        text = "⚙️ Settings"
        if self.user_lang == 'ru':
            text = "⚙️ Настройки"
        return text

    def get_natives_text(self):
        text = "⚙️ Settings — Select the native"
        if self.user_lang == 'ru':
            text = "⚙️ Настройки — Выберите носителя"
        return text
    
    def get_langs_text(self):
        text = "⚙️ Settings — Select the language"
        if self.user_lang == 'ru':
            text = "⚙️ Настройки — Выберите язык"
        return text

    def get_back_text(self):
        text = "⬅️ Back"
        if self.user_lang == 'ru':
            text = "⬅️ Назад"
        return text
    
    def get_change_native_text(self):
        text = "Change the native"
        if self.user_lang == 'ru':
            text = "Поменять носителя"
        return text
    
    def get_change_language_text(self):
        text = "Change the language"
        if self.user_lang == 'ru':
            text = "Поменять язык"
        return text
    
    def get_save_text(self):
        text = "✅ Save settings"
        if self.user_lang == 'ru':
            text = "✅ Сохранить настройки"
        return text
    
    def get_saved_settings_text(self):
        text = "👌 Settings saved"
        if self.user_lang == 'ru':
            text = "👌 Настройки сохранены"
        return text
    
    def get_lang_changed_text(self):
        text = "👌 Language changed"
        if self.user_lang == 'ru':
            text = "👌 Язык изменен"
        return text
    
    def get_native_changed_text(self):
        text = "👌 Native changed"
        if self.user_lang == 'ru':
            text = "👌 Носитель изменен"
        return text