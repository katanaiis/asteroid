from if3_game.engine import Sprite, Game, Layer, Text, AnimatedSprite
from random import randint
from pyglet.window.key import symbol_string
from math import sin, cos, radians
import os

RESOLUTION = (1280, 720)

class AsteroidGame(Game):
    def __init__(self):
        super().__init__()
        self.make_title_screen()
        self.score = 0

    def make_title_screen(self):
        title_layer = TitleLayer(self)
        image = Sprite("assets/title_screen.png")
        title_layer.add(image)

        anim = AnimatedSprite(os.path.dirname(os.path.realpath(__file__)) + "/assets/animation.gif")
        #anim = AnimatedSprite("assets/animation.gif")
        title_layer.add (anim)
        self.add(title_layer)

    def make_gameplay_screen(self):
        self.remove_all_layers()

        background_layer = Layer()
        background = Sprite("assets/background.png")
        background_layer.add(background)

        text = Text("RAD!!!", (640, 360))
        background_layer.add(text)
        text.element.text = "Something else"

        self.add(background_layer)

        game_layer = CustomLayer(self)
        spaceship = Spaceship(position=(200, 350))
        game_layer.add(spaceship)

        asteroid = Asteroid(position=(200, 600), initial_speed=(-100, 100))
        game_layer.add(asteroid)

        self.add(game_layer)

        ui_layer = UILayer(spaceship)
        self.add(ui_layer)

class CustomLayer(Layer):

    def __init__(self, game):
        super().__init__()
        self.game = game

class TitleLayer(CustomLayer):
    
    def on_key_press(self, key, modifiers):
        super().on_key_press(key, modifiers)
        self.game.make_gameplay_screen()

class UILayer(Layer):

    def __init__(self, ship):
        super().__init__()
        self.spaceship = ship
        self.sprites = []
        for i in range(self.spaceship.lives):
            life = Sprite("assets/life.png", (100 + i * 50, 650))
            self.add(life)
            self.sprites.append(life)
    
    def update(self, dt):
        super().update(dt)
        if self.spaceship.lives < len(self.sprites):
            to_destroy = self.sprites[-1]
            self.sprites.remove(to_destroy)
            to_destroy.destroy()
            # En une ligne :
            # self.sprites.pop().destroy()


class SpaceObject(Sprite):

    def __init__(self,
                 image,
                 position=(0, 0),
                 scale=1,
                 initial_speed=(0, 0),
                 anchor=(0, 0),
                 collision_shape="circle"):
        super().__init__(image, position, scale, anchor, collision_shape)
        self.speed = initial_speed
        self.rotation_speed = 45

    def update(self, dt):
        super().update(dt)

        posx = self.position[0]
        posy = self.position[1]

        posx += dt * self.speed[0]
        posy += dt * self.speed[1]

        if posx > RESOLUTION[0]:
            posx = 0
        elif posx < 0:
            posx = RESOLUTION[0]
        
        if posy > RESOLUTION[1]:
            posy = 0
        elif posy < 0:
            posy = RESOLUTION[1]

        self.position = (posx, posy)

        self.rotation += dt * self.rotation_speed


class Spaceship(SpaceObject):

    def __init__(self, position=(0, 0)):
        super().__init__("assets/spaceship.png", position,
                         anchor=(32, 32))
        self.rotation_speed = 0
        self.velocity = 0
        self.acceleration = 0
        self.lives = 3
        self.immortal = 0

    def on_key_press(self, key, modifiers):
        if symbol_string(key) == "RIGHT":
            self.rotation_speed += 360
        elif symbol_string(key) == "LEFT":
            self.rotation_speed -= 360
        elif symbol_string(key) == "UP":
            self.acceleration = 150
        elif symbol_string(key) == "SPACE":
            self.shoot()

    def on_key_release(self, key, modifiers):
        if symbol_string(key) == "RIGHT":
            self.rotation_speed -= 360
        elif symbol_string(key) == "LEFT":
            self.rotation_speed += 360
        elif symbol_string(key) == "UP":
            self.acceleration = 0

    def update(self, dt):
        # Calculer la vitesse

        if self.acceleration > 0:
            self.velocity += dt * self.acceleration
            #self.velocity = self.acceleration

            angle = radians(-self.rotation)
            speed_x = self.speed[0] + dt * cos(angle) * self.velocity
            speed_y = self.speed[1] + dt * sin(angle) * self.velocity
            
            self.speed = (speed_x, speed_y)
        else:
            self.velocity = 0

        if self.immortal > 0:
            self.immortal -= dt
            self.opacity = 50
        else:
            self.opacity = 255

        super().update(dt)

    def shoot(self):
        angle = radians(-self.rotation)
        speed = (500 * cos(angle), 500 * sin(angle))

        bullet = Bullet(position=self.position, initial_speed=speed)
        self.layer.add(bullet)

    def destroy(self):
        if self.immortal <= 0:
            print(self.lives)
            if self.lives > 0:
                self.lives -= 1
                self.immortal = 3
            else:
                super().destroy()

class Asteroid(SpaceObject):

    def __init__(self, position, initial_speed, size=3):
        self.size = size
        if self.size == 3:
            super().__init__("assets/asteroid128.png",
                            position, 1, initial_speed,
                            (64, 64))
        elif self.size == 2:
            super().__init__("assets/asteroid64.png",
                            position, 1, initial_speed,
                            (32, 32))
        elif self.size == 1:
            super().__init__("assets/asteroid32.png",
                            position, 1, initial_speed,
                            (16, 16))

    def on_collision(self, other):
        if isinstance(other, Spaceship):
            other.destroy()
    
    def destroy(self):
        self.layer.game.score += 1
        if self.size > 1:
            for i in range(2):
                asteroid = Asteroid(self.position,
                                    (randint(-300, 300), randint(-300, 300)),
                                    self.size - 1)
                self.layer.add(asteroid)
        super().destroy()

class Bullet(SpaceObject):
    def __init__(self, position, initial_speed):
        super().__init__("assets/bullet.png",
                         position, 1, initial_speed, (8, 8))
        self.lifetime = 1

    def on_collision(self, other):
        if isinstance(other, Asteroid):
            other.destroy()
            self.destroy()
    
    def update(self, dt):
        super().update(dt)

        self.lifetime -= dt
        if self.lifetime <= 0:
            self.destroy()



