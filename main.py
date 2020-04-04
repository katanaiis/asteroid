from if3_game.engine import init, Layer, Sprite, Text
from game_objects import RESOLUTION, Spaceship, Asteroid, AsteroidGame

# vvv Nécessaire pour jouer des sons
import pyglet
import os
# On a besoin du répertoire correct du script pour le son
script_path = os.path.dirname(os.path.realpath(__file__))

pyglet.lib.load_library(script_path + '/avbin')
pyglet.have_avbin=True
# ^^^

init(RESOLUTION, "My super black screen")

game = AsteroidGame()

# Charger un fichier wav
music = pyglet.media.load(script_path + '/assets/music.wav')

# Créer un objet qui s'occupe de faire tourner le son en boucle
looper = pyglet.media.SourceGroup(music.audio_format, None)
looper.loop = True

# Ajouter la musique au loopeur
looper.queue(music)

# Créer un "lecteur de musique" qui va s'occuper de jouer notre musique
player = pyglet.media.Player()
# Attention, on ajoute le loopeur, pas la musique
player.queue(looper)
# On appuie sur play
player.play()

game.debug = True
game.run()