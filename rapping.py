from tts import TTS, Voice
from postprocessing import AudioProcessing
from lyric_crawler import crawl_lyrics
from utils import prepare_text
from samples import eminem, fifty_cent

choice = input('Would you like to suggest a topic or should i pick from samples? ')
if choice in 'sample':
    choice = input('Choose from samples: \n 1-) Eminem \n 2-) 50 Cent')
    if choice == '1':
        lyrics = eminem
    elif choice == '2':
        lyrics = fifty_cent
else:
    limit = input("Set a line limit: ")
    lyrics = crawl_lyrics(choice)[:int(limit)]

ap = AudioProcessing()

for text in lyrics:
    text = prepare_text(text)
    tts = TTS(Voice(Voice.Language.enUS, Voice.Sex.male, "Justin"))
    ap.modify(tts.speak(text), 0.1, -1, 1, mid_part=0.05, mid_pitch=2, mid_stretch=1, accel=1.0)
aud, br = ap.insert_beat()
aud, br = ap.add_duet('Drop the beat DJ!', 0, 2)
aud, br = ap.add_duet('Aha. Yeah. Aha!', 3, 0.5)
ap.write(aud, br, name=choice)

