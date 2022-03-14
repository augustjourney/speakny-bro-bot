import boto3
from .config import Config as config
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
        self.output = os.path.join(os.getcwd() + "/src/tmp/", self.filename)

    def synthesize(self):
        # Initialising boto3 client
        polly = boto3.client('polly', region_name="eu-central-1", aws_access_key_id = config.aws_access_key_id, aws_secret_access_key=config.aws_secret_access_key)
        
        # Synthesize speech with this polly client
        try:
            response = polly.synthesize_speech(
                LanguageCode = self.language_code, 
                OutputFormat = 'ogg_vorbis', 
                Text = self.text, 
                VoiceId = self.voice
            )
        except Exception as e:
            print(e)
        
        # There will be audio stream in polly's response
        # Saving it to audio ogg file
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                try:
                    with open(self.output + '.ogg', "wb") as file:
                        file.write(stream.read())          
                except IOError as error:
                    print(error)
                    sys.exit(-1)
            return True

        return False
    
    # Converting audio ogg file to opus codec
    def convert_to_opus(self):
        try: 
            # Using ffmpeg convert audio to opus without any other changes
            ffmpeg.input(self.output + '.ogg').output(self.output + '.opus').run(capture_stdout=True, capture_stderr=True)
            # Having covereted it, deleting audio ogg file
            self.delete_file(self.filename + '.ogg')
            # And return the audio name with extension .opus
            return self.output + '.opus'
        
        # If errors, delete .ogg and .opus files
        except ffmpeg.Error as e:
            print(e.stderr.decode(), file=sys.stderr)
            self.delete_file(self.filename + '.ogg')
            self.delete_file(self.filename + '.opus')
            sys.exit(1)

    # Getting audio duration out of audio stream
    def get_audio_duration(self, path_to_file):
        # Getting audio info using ffmpeg probe function 
        try:
            probe = ffmpeg.probe(path_to_file)
        except ffmpeg.Error as e:
            print(e.stderr, file=sys.stderr)
            sys.exit(1)
        
        # Probe returns list of audiostreams
        # Find that one that has codec_type audio
        audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
        
        if audio_stream is None:
            print('No stream found', file=sys.stderr)
            return 0
        
        # Converting duration to float
        f = float(audio_stream['duration'])
        
        # And getting the ceiling of that float
        duration = math.ceil(f)
        
        return duration

    # General function to delete file by filename
    def delete_file(self, filename):
        # All files are temporarily store in this tmp folder
        path_to_file = os.path.join(os.getcwd() + "/src/tmp/", filename)
        # If there's file there — delete it
        if os.path.isfile(path_to_file):
            os.remove(path_to_file)
