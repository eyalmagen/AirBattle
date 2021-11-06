from consts import *


class Explosion(pygame.sprite.Sprite):
    """
    dead tank
    """
    def __init__(self, manage, player):
        pygame.sprite.Sprite.__init__(self)
        self.size = player.tankx
        self.image = explode_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 30
        manage.add_sprite(self)

    def update(self):
        now = pygame.time.get_ticks()
        # its been at least that losg
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explode_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explode_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
