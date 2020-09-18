from pygame import mixer  # Load the popular external library

mixer.init()
mixer.music.load('SONG.mp3')
mixer.music.play()

class Car:
    def __init__ (self):
        self.name = ""
        self.colour = ""
        self.noise = "Vroooom"

    def move(self):
        print(self.name + " goes " + self.noise)
