import librosa
import os
import numpy as np
import soundfile as sf

from tts import TTS, Voice

class AudioProcessing:
    
    def _decode_audio(audio):
        return sf.read(audio)
    
    def __init__(self, audio):
        self.audio = audio
        
    def modify(self, end_part, end_pitch, end_stretch, mid_part=0.1, mid_pitch=1, mid_stretch=1, name="modified.wav", accel = 1.5):
        y, sr = AudioProcessing._decode_audio(self.audio)
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
        
        # print(len(y))
        # print(len(y_ending))
        # print(len(y_mid))
        # print(len(unmodified_one))
        # print(len(unmodified_two))
        
        y_end_shifted = librosa.effects.pitch_shift(y_ending, sr, n_steps=end_pitch)
        y_end_shift_stretch = librosa.effects.time_stretch(y_end_shifted, end_stretch)
        y_mid_shifted = librosa.effects.pitch_shift(y_mid, sr, n_steps=mid_pitch)
        y_mid_shift_stretch = librosa.effects.time_stretch(y_mid_shifted, mid_stretch)
        
        y_modified = np.concatenate([unmodified_one, y_mid_shift_stretch, unmodified_two, y_end_shift_stretch])

        y_final = librosa.effects.time_stretch(y_modified, accel)
        
        librosa.output.write_wav(name, y_final, sr)
        