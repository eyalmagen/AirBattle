from consts import *
from mobile import Mobile
import random


class Missile(Mobile):
    # bullet sizes
    missile_width = 50
    missile_length = 19

    def __init__(self, manage, player):
        """
        image       :the image that represent bullet
        rect        :Rect - position and size of the bullet.
        drt         :direction of the bullet
        speed       :int - speed of bullet
        strength    :int - how much damage will it cause
        belong_to : the player id that fired it

        """
        if player.missile_amount > 0 and player.life > 0:
            # make it a sprite, and mov eable
            Mobile.__init__(self)
            self.manage = manage
            self.mis_speed = 10
            self.angular_velocity = 3
            # reduce number of bullets
            player.missile_amount -= 1
            # image and rectangle
            self.animation = missile_anim
            for ani in self.animation:
                ani.set_colorkey(white)
            self.image = missile_anim[0]

            # self.image = pygame.transform.scale(self.image, (self.missile_width, self.missile_length))
            self.frame = 0
            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 30

            self.rect = self.image.get_rect()
            self.rect.center = player.rect.center
            # direction and speed

            # vector size
            self.speed = self.mis_speed
            self.angle = player.angle

            # the damage the bullet would do if hit
            self.strength = player.bullet_power

            # the tank which fired
            self.belong_to = player.id

            # add to the group of bullets
            manage.add_sprite(self)

    def update(self):
        now = pygame.time.get_ticks()
        self.todo = self.manage.tank_most_in_object_way(self)

        # its been at least that losg
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame = (self.frame + 1) % len(self.animation)
            self.image = self.animation[self.frame]
