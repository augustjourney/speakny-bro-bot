from polly import Polly
from settings import Config as config
import uuid
import requests
class Voiceover:
    def __init__(self, chat_id, text, lang, native):
        self.text = text
        self.lang = lang
        self.native = native
        self.chat_id = chat_id
        self.filename = ""
        self.duration = ''
        self.file_path = ''        
        self.url = f'{config.bot_base_url}/sendVoice'

    def get_audio(self):
        self.get_filename()
        pol = Polly(self.filename, self.text, self.native, self.lang)
        synth = pol.synthesize()
        self.file_path = pol.convert_to_opus()
        self.duration = pol.get_audio_duration(self.file_path)
        return self.filename

    def send_audio(self):
        file = open(self.file_path, "rb")
        data = {'chat_id' : self.chat_id, 'duration': int(self.duration)}
        r = requests.post(self.url, files={'voice':file}, data=data)
        file.close()
        return True

    def delete_audio(self, filename):
        Polly.delete_file(None, filename)

    def get_filename(self):
        id = uuid.uuid4()
        filename = str(id)
        filename = filename[:18]
        self.filename = filename
        return filename
    
    def create_speech(self):
        url = f"{config.hello_base_url}/speaknybro/speech/new-speech"
        lang = self.lang.split('-')
        lang = lang[0]
        data = {
            "text": self.text,
            "native": self.native,
            "language": lang,
            "chat_id": self.chat_id
        }
        res = requests.post(url, json=data)
        return res.json()