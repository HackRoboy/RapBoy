from tts import TTS, Voice
from postprocessing import AudioProcessing
from lyric_crawler import crawl_lyrics
from utils import prepare_text

# word = input('Insert a word: ')
word = 'wall'

ap = AudioProcessing()

for index, text in enumerate(crawl_lyrics(word)[:4]):
    text = prepare_text(text)
    print(text)
    tts = TTS(Voice(Voice.Language.enUS, Voice.Sex.male, "Justin"))
    ap.modify(tts.speak(text), 0.1, -1, 1, mid_part=0.05, mid_pitch=2, mid_stretch=1, accel=1.0)
    # os.system('mpv' + ' ' + str(index))
ap.insert_beat()
ap.write()