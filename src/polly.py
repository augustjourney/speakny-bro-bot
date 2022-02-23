import boto3
from settings import Config as config
import os
import sys
import ffmpeg
from contextlib import closing
import math
class Polly:
    def __init__(self, filename, text, voice, language_code):
        self.text = text
        self.voice = voice
        self.language_code = language_code
        self.filename = filename
        self.output = os.path.join(os.getcwd() + "/tmp/", self.filename)

    def synthesize(self):
        polly = boto3.client('polly', region_name="eu-central-1", aws_access_key_id = config.aws_access_key_id, aws_secret_access_key=config.aws_secret_access_key)
        try:
            response = polly.synthesize_speech(
                LanguageCode = self.language_code, 
                OutputFormat = 'ogg_vorbis', 
                Text = self.text, 
                VoiceId = self.voice
            )
        except Exception as e:
            print(e)
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                try:
                    with open(self.output + '.ogg', "wb") as file:
                        file.write(stream.read())          
                except IOError as error:
                    print(error)
                    sys.exit(-1)
            return True
    
    def convert_to_opus(self):
        try: 
            ffmpeg.input(self.output + '.ogg').output(self.output + '.opus').run(capture_stdout=True, capture_stderr=True)
            self.delete_file(self.filename + '.ogg')
            return self.output + '.opus'
        except ffmpeg.Error as e:
            print(e.stderr.decode(), file=sys.stderr)
            self.delete_file(self.filename + '.ogg')
            self.delete_file(self.filename + '.opus')
            sys.exit(1)

    def get_audio_duration(self, path_to_file):
        try:
            probe = ffmpeg.probe(path_to_file)
        except ffmpeg.Error as e:
            print(e.stderr, file=sys.stderr)
            sys.exit(1)
        
        audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
        if audio_stream is None:
            print('No stream found', file=sys.stderr)
            return 0
        f = float(audio_stream['duration'])
        duration = math.ceil(f)
        return duration

    def delete_file(self, filename):
        path_to_file = os.path.join(os.getcwd() + "/tmp/", filename)
        if os.path.isfile(path_to_file):
            os.remove(path_to_file)
