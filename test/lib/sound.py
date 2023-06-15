import board
import audiocore
import audiopwmio
import time
import pwmio

MARIO = [
  ('E7', 2), ('E7', 2), ('C7', 2), ('E7', 2), ('G7', 2), (None, 6), ('G6', 2),
  (None, 6), ('C7', 2), (None, 4), ('G6', 2), (None, 4), ('E6', 2), (None, 4),
  ('A6', 2), (None, 2), ('B6', 2), (None, 2), ('A#6', 2), ('A6', 2), (None, 2),
  ('G6', 2), ('E7', 2), (None, 2), ('G7', 2), ('A7', 2), (None, 2), ('F7', 2),
  ('G7', 2), (None, 2), ('E7', 2), (None, 2), ('C7', 2), ('D7', 2), ('B6', 2),
]

JINGLE_BELLS = [
  ("e5", 2), ("e5", 2), ("e5", 4), ("e5", 2), ("e5", 2), ("e5", 4),
  ("e5", 2), ("g5", 2), ("c5", 4), ("d5", 1), ("e5", 6), (None, 2),
  ("f5", 2), ("f5", 2), ("f5", 3), ("f5", 1), ("f5", 2), ("e5", 2),
  ("e5", 2), ("e5", 1), ("e5", 1), ("e5", 2), ("d5", 2), ("d5", 2),
  ("e5", 2), ("d5", 4), ("g5", 2), (None, 2),
  ("e5", 2), ("e5", 2), ("e5", 4), ("e5", 2), ("e5", 2), ("e5", 4),
  ("e5", 2), ("g5", 2), ("c5", 4), ("d5", 1), ("e5", 6), (None, 2),
  ("f5", 2), ("f5", 2), ("f5", 3), ("f5", 1), ("f5", 2), ("e5", 2),
  ("e5", 2), ("e5", 1), ("e5", 1), ("g5", 2), ("g5", 2), ("f5", 2),
  ("d5", 2), ("c5", 6), (None, 2)
]

HANUKKAH = [
  ("g5", 2), ("e5", 2), ("g5", 4), ("g5", 2), ("e5", 2), ("g5", 4),
  ("e5", 2), ("g5", 2), ("c6", 2), ("b5", 2), ("a5", 8),
  ("f5", 2), ("d5", 2), ("f5", 4), ("f5", 2), ("d5", 2), ("f5", 4),
  ("d5", 2), ("f5", 2), ("b5", 2), ("a5", 2), ("g5", 8),
  ("g5", 2), ("e5", 2), ("g5", 4), ("g5", 2), ("e5", 2), ("g5", 4),
  ("e5", 2), ("g5", 2), ("c6", 2), ("b5", 2), ("a5", 8),
  ("b5", 2), ("b5", 2), ("b5", 4), ("b5", 2), ("b5", 2), ("b5", 4),
  ("b5", 2), ("g5", 2), ("a5", 2), ("b5", 2), ("c6", 8),
]

class Audio:
    def __init__(self, left=board.GP18, right=board.GP19):
        self._left = left
        self._right = right
        
    def note(self, name):
        print(name)
        octave = int(name[-1])
        PITCHES = "c,c#,d,d#,e,f,f#,g,g#,a,a#,b".split(",")
        pitch = PITCHES.index(name[:-1].lower())
        return 440 * 2 ** ((octave - 4) + (pitch - 9) / 12.)
    
    def tone(self, note):
        if note is None:
            self.buzzer.duty_cycle = 0
        else:
            self.buzzer.frequency = int(self.note(note))
            self.buzzer.duty_cycle = 19660
    
    def play_song(self, song):
        for (tone, duration) in song:
            self.tone(tone)
            time.sleep(duration/10)
            self.tone(None)

    def buzzer_init(self):
        self.buzzer = pwmio.PWMOut(self._left, variable_frequency=True)
    
    def play(self, filename, sleep_for=3):
        self.buzzer.deinit()
        data = open(filename, "rb")
        wav = audiocore.WaveFile(data)
        dac = audiopwmio.PWMAudioOut(self._left,right_channel=self._right)
        dac.play(wav)
        time.sleep(sleep_for)
        dac.stop()
        dac.deinit()
        self.buzzer_init()

if __name__ == '__main__':
    audio = Audio()
    audio.buzzer_init()
    audio.play_song(MARIO)

