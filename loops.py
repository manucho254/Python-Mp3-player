import random
import pygame as pg
from tkinter.filedialog import askdirectory
import os


pg.mixer.pre_init(44100, -16, 2, 2048)
pg.init()
screen = pg.display.set_mode((640, 480))

# A list of the music file paths.
directory = askdirectory()
os.chdir(directory)
# it permits to change the current dir
song_list = os.listdir()

for music_index in song_list:
    music_index = 0
    pg.mixer.init()
    pg.mixer.music.load(song_list[music_index])
    pg.mixer.music.play()



#Here we create a custom event type (it's just an int).
SONG_FINISHED = pg.USEREVENT + 1
# When a song is finished, pygame will add the
# SONG_FINISHED event to the event queue.
pg.mixer.music.set_endevent(SONG_FINISHED)
# Load and play the first song.


clock = pg.time.Clock()
song_idx = 0  # The index of the current song.
done = False

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        elif event.type == pg.KEYDOWN:
            # Press right arrow key to increment the
            # song index. Modulo is needed to keep
            # the index in the correct range.
            if event.key == pg.K_RIGHT:
                print('Next song.')
                song_idx += 1
                song_idx %= len(song_list)
                pg.mixer.music.load(song_list[song_idx])
                pg.mixer.music.play(0)
        # When a song ends the SONG_FINISHED event is emitted.
        # Then just pick a random song and play it.
        elif event.type == SONG_FINISHED:
            print('Song finished. Playing random song.')
            pg.mixer.music.load(random.choice(song_list))
            pg.mixer.music.play(0)

    screen.fill((30, 60, 80))
    pg.display.flip()
    clock.tick(30)

