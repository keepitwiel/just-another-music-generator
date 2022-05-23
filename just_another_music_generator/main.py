from sequence import Sequence
from tone import Tone

s = Sequence()

tone = Tone(start_time=0.0, duration=1.0, pitch=440, volume=0.5)
s.add(tone)

a = s.render(44100)

