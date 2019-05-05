import librosa
import soundfile as sf
import numpy as np
from math import floor
from tts import TTS, Voice

class AudioProcessing:

    def _decode_audio(audio):
        return sf.read(audio)
    
    def __init__(self):
        self.final_audio = np.empty(1)
        self.sr = 0

    def write(self, file, sr,name='rapboy/final.wav'):
        librosa.output.write_wav(name, file, sr)

    def modify(self, audio, end_part, end_pitch, end_stretch, mid_part=0.1, mid_pitch=1, mid_stretch=1, accel = 1.2):
        y, sr = AudioProcessing._decode_audio(audio)
        modif_size_end = int(len(y)*end_part)
        modif_size_mid = int(len(y)*mid_part)
        end_range_start = len(y) - modif_size_end
        mid_handle = int(end_range_start/2)
        end_indices = list(range(end_range_start, len(y)))
        y_ending = y[end_indices]
        mid_range_start = mid_handle - int(modif_size_mid/2)
        mid_range_end = mid_handle + int(modif_size_mid/2)
        mid_indices = list(range(mid_range_start, mid_range_end))
        y_mid = y[mid_indices]
        unmodified_one = y[:mid_range_start]
        unmodified_two = y[mid_range_end:end_range_start]

        y_end_shifted = librosa.effects.pitch_shift(y_ending, sr, n_steps=end_pitch)
        y_end_shift_stretch = librosa.effects.time_stretch(y_end_shifted, end_stretch)
        y_mid_shifted = librosa.effects.pitch_shift(y_mid, sr, n_steps=mid_pitch)
        y_mid_shift_stretch = librosa.effects.time_stretch(y_mid_shifted, mid_stretch)
        
        y_modified = np.concatenate([unmodified_one, y_mid_shift_stretch, unmodified_two, y_end_shift_stretch])

        y_final = librosa.effects.time_stretch(y_modified, accel)

        if self.final_audio.any():
            self.final_audio = np.append(self.final_audio, y_final)
        else:
            self.final_audio = y_final
        if not self.sr:
            self.sr = sr

    def asd(self):
        return

    def insert_beat(self):
        beat_audio, self.br = self.read_beat('beat.wav')
        beat_audio_frame = beat_audio[:int(beat_audio.size/2)]
        self.final_audio = self.final_audio.repeat(2, axis=0)
        self.sr = self.br
        self.times = floor(self.final_audio.size/beat_audio_frame.size)+2
        length_difference = self.times*beat_audio_frame.size - self.final_audio.size
        self.final_audio = np.append(self.final_audio, np.zeros(length_difference))
        final_beat = np.hstack([beat_audio_frame]*self.times)
        self.final_audio = self.final_audio + final_beat*0.6
        self.final_audio = self.normalize(self.final_audio)
        self.final_audio = self.append_beat(beat_audio_frame, self.final_audio, start=True, amount=2)
        return self.final_audio, self.br

    @staticmethod
    def normalize(aud):
        return aud/np.max(np.abs(aud))

    def add_duet(self, text, part, percentage=1.0):
        tts = TTS(Voice(Voice.Language.enUS, Voice.Sex.male, "Joey"))
        aud, dr = sf.read(tts.speak(text))
        aud = aud.repeat(2, axis=0)
        dr = dr * 2
        one_part_length = len(self.final_audio)/self.times
        if one_part_length < len(aud):
            print('Warning: Duet is longer than the beat!')
        start = int(one_part_length*part)
        length = len(aud)
        self.final_audio[start:start+length:] += aud*percentage
        return self.final_audio, self.sr


    def append_beat(self, beat_audio, original_audio, start=True, amount=2):
        self.times += amount
        for i in range(amount):
            if start:
                original_audio = np.append(beat_audio, original_audio)
            else:
                original_audio = np.append(original_audio, beat_audio)
        return original_audio

    @staticmethod
    def read_beat(file_name="beat.wav"):
        beat, br = sf.read(file_name)
        return np.mean(np.array(beat, dtype=float), axis=1), br