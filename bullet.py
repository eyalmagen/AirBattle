from consts import *
from mobile import Mobile


class Bullet(Mobile):
    # bullet sizes
    bullet_width = 9
    bullet_length = 33

    def __init__(self, manage, player):
        """
        image       :the image that represent bullet
        rect        :Rect - position and size of the bullet.
        drt         :direction of the bullet
        speed       :int - speed of bullet
        strength    :int - how much damage will it cause
        belong_to : the player id that fired it
        aim_to:     id of a quar that this bullet is aimed for
        """
        if player.bullet_amount > 0 and player.life > 0:
            # make it a sprite, and mov eable
            Mobile.__init__(self)

            # reduce number of bullets
            player.bullet_amount -= 1
            # image and rectangle
            self.image = (BULLET_IMAGE)
            self.image = pygame.transform.scale(self.image, (self.bullet_width, self.bullet_length))
            self.image.set_colorkey(black)

            self.rect = self.image.get_rect()
            self.rect.center = player.rect.center
            # direction and speed

            # vector size
            self.speed = player.bullet_speed
            self.angle = player.angle

            # the damage the bullet would do if hit
            self.strength = player.bullet_power

            # the tank which fired
            self.belong_to = player.id

            # add to the group of bullets
            manage.add_sprite(self)
