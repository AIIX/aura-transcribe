import os
import subprocess

from mycroft.configuration import Configuration
from mycroft.session import SessionManager
from mycroft.stt import MycroftSTT
from mycroft.skills.core import MycroftSkill, intent_handler, intent_file_handler
from mycroft.messagebus.message import Message
from mycroft.util.log import LOG
from speech_recognition import WavFile, AudioData

class AuraTranscribe(MycroftSkill):
    
    def __init__(self):
        super(AuraTranscribe, self).__init__(name="AuraTranscribe")
    
    def initialize(self):
        print("AuraTranscribe Skill Initalized")
        self.add_event("aura.browser.request.stt", self.transcribe_audio)
        self.stt = MycroftSTT()

    def transcribe_audio(self, message):
        audio_file = message.data["file"]
        audio_wav_file = "/tmp/aura_in.wav"
        subprocess.call(["sox","-r","16000", "-t", "sw", "-e", "signed", "-c", "1", "-b", "16", audio_file, audio_wav_file])
        audio = self.get_audio_data(audio_wav_file)
        text = self.stt.execute(audio, self.lang)
        self.bus.emit(Message("aura.browser.request.result", {"result": text}))
        
    def get_audio_data(self, audiofile):
        wavfile = WavFile(audiofile)
        with wavfile as source:
            return AudioData(source.stream.read(), wavfile.SAMPLE_RATE, wavfile.SAMPLE_WIDTH)

        
def create_skill():
    return AuraTranscribe()
