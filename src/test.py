import winsound
import random
import math
from pysine import sine
# from threading import Thread
import multiprocessing

# winsound.Beep(freq, duration)
# freq: Hz, 37-32767
# duration: milliseconds

#winsound.Beep(440, 2000)

f0 = 440.0
a = math.pow(2, 1/12)

# fn = f0 * a^n

NOTES = [f0 * math.pow(a, x) for x in range(-30, 30, 1)]

MIN_NOTE_LENGTH = 100
MAX_NOTE_LENGTH = 1000
NOTE_LENGTH_STEP = 50

# for n in notes:
#     print(n)


class Note:
    """docstring for ."""

    def __init__(self, frequency, duration):
        self.frequency = frequency
        self.duration = duration

    def play(self):
        sine(frequency=self.frequency, duration=self.duration)
        # print("N: {}".format(self.duration))


class Phrase:

    def __init__(self, length, max_time_length):
        self.notes = []
        self.length = length
        self.max_time_length = max_time_length
        self.time_length = 0
        self.seed = random.choice(range(3, len(NOTES)-3, 1))
        self.note_set = NOTES[self.seed-3:self.seed+4]

    def is_full(self):
        # return len(self.notes) >= self.length
        return self.time_remaining() <= 0

    def add_note(self, frequency, duration):
        if self.time_remaining() < MIN_NOTE_LENGTH/1000:
            new_note_duration = duration + self.time_remaining()
            self.notes.append(Note(frequency, new_note_duration))
            self.time_length += new_note_duration
        elif duration > self.time_remaining():
            new_note_duration = self.time_remaining()
            self.notes.append(Note(frequency, new_note_duration))
            self.time_length += new_note_duration
        else:
            self.notes.append(Note(frequency, duration))
            self.time_length += duration

    def play(self):
        total = 0.0
        for n in self.notes:
            n.play()
            print("N: {}".format(n.duration))
            total += n.duration
            print("TOTAL: {}".format(total))
        print("END OF PHRASE")
        # print(NOTES[self.seed])
        # print(self.note_set)

    def time_remaining(self):
        return self.max_time_length - self.time_length

    def pick_note(self):
        return random.choice(self.note_set)


NUMBER_OF_PHRASES = 4
PHRASE_LENGTH = range(5, 10, 1)


def play_voice():

    phrases = []
    for i in range(NUMBER_OF_PHRASES):

        p = Phrase(random.choice(PHRASE_LENGTH), 5.0)
        # freq = random.randrange(100, 1000, 1)
        while not p.is_full():

            # freq = random.choice(NOTES)
            freq = p.pick_note()
            dur = random.randrange(MIN_NOTE_LENGTH, MAX_NOTE_LENGTH, NOTE_LENGTH_STEP)/1000.0
            p.add_note(freq, dur)
            # sine(frequency=freq, duration=dur)
        phrases.append(p)
    #    winsound.Beep(freq, dur)

    for p in phrases:
        p.play()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    # multiprocessing.set_start_method('spawn')
    p = multiprocessing.Process(target=play_voice)
    p.start()
    play_voice()
    p.join()

# t1 = Thread(target=play_voice)
# t2 = Thread(target=play_voice)
# t1.start()
# t2.start()

#sine(frequency=440.0, duration=2.0)
