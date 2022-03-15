from src.polly import Polly
from src.config import Config as config
import uuid
import requests
from src.speech_repo import SpeechRepo as _speech

class Speech:
    def __init__(self, chat_id, text, lang, native):
        self.text = text
        self.lang = lang
        self.native = native
        self.chat_id = chat_id
        self.filename = ""
        self.duration = ''
        self.file_path = ''        
        self.url = f'{config.bot_base_url}/sendVoice'

    # Getting audio out of text
    # Returns the file name, without its extension
    def get_audio(self):
        # Creating file name out of uuid
        self.get_filename()
        # Initialising the polly instance
        # Which will be used for text-to-speech converting
        pol = Polly(self.filename, self.text, self.native, self.lang)
        # Synthesize text with polly
        # It creates audio file with ogg extension
        synth = pol.synthesize()
        # Converting ogg to opus codec
        # It's necessary for telegram to display correctly as a voice message
        self.file_path = pol.convert_to_opus()
        # Getting audio duration
        self.duration = pol.get_audio_duration(self.file_path)
        # Returning just the name of the audio file
        return self.filename

    # Sending audio as a voice message to the user
    def send_audio(self):
        # Getting audio data by opening the file
        file = open(self.file_path, "rb")
        # Object with data to send
        data = {'chat_id' : self.chat_id, 'duration': int(self.duration)}      
        # Sending voice message via requests
        r = requests.post(self.url, files={'voice':file}, data=data)
        # Closing file
        file.close()
        return True

    # Deleting audio
    def delete_audio(self, filename):
        Polly.delete_file(None, filename)

    # Create a filename for future audio
    def get_filename(self):
        # Generating uuid and taking first 18 characters
        filename = str(uuid.uuid4())
        filename = filename[:18]
        self.filename = filename
        return filename
    
    # Save this speech to the database
    def create_speech(self):
        """
            Getting the lang by splitting
            Because self.lang is normally like this — en-US
            The structure — {language}-{country}
            Here we don't need the country
            So we just take the language, the first one out of split
        """
        lang = self.lang.split('-')[0]
        speech = _speech.create_speech(self.text, self.native, lang, self.chat_id)
        if speech:
            return True
        return False