import requests
from enum import Enum
import io
import os
import base64

# https://docs.aws.amazon.com/polly/latest/dg/voicelist.html
class Voice:
    class Sex(Enum):
        male = "male"
        female = "female"

    class Language(Enum):
        enUS = 'en-US'
        enGB = 'en-GB'

    def __init__(self, lang, sex, name):
        self.lang = lang
        self.sex = sex
        self.name = name

class Cache:
    def __init__(self, path="_cache"):
        self.path = path
        if not os.path.isdir(self.path):
            os.makedirs(self.path)

    def _encode(voice, text):
        return base64.b64encode(f"{voice.lang};{voice.sex};{voice.name};{text}".encode())

    def _get_file_name(self, voice, text):
        return os.path.join(self.path, str(Cache._encode(voice, text), 'utf-8') + ".ogg")

    def put(self, voice, text, audio):
        filename = self._get_file_name(voice, text)
        with open(filename, "wb") as f:
            f.write(audio.read())
        audio.seek(0)

    def get(self, voice, text):
        filename = self._get_file_name(voice, text)
        if not os.path.isfile(filename):
            return None
        with open(filename, "rb") as f:
            audio = io.BytesIO(f.read())
        return audio


class TTS:
    url = "https://streamlabs.com/polly/speak"

    def _fetch_audio(url):
        response = requests.get(url)
        if response.status_code != requests.codes.ok:
            response.raise_for_status()
        return io.BytesIO(response.content)

    def __init__(self, voice):
        self.voice = voice
        self.cache = Cache()

    def speak(self, text):
        in_cache = self.cache.get(self.voice, text)
        if not in_cache is None:
            return in_cache
        body = {
            "text": text,
            "voice": self.voice.name
        }
        response = requests.post(TTS.url, json=body)
        if response.status_code != requests.codes.ok:
            response.raise_for_status()
        json_response = response.json()
        if not json_response['success']:
            raise Exception(json_response)
        audio_url = json_response['speak_url']
        audio = TTS._fetch_audio(audio_url)
        self.cache.put(self.voice, text, audio)
        return audio


