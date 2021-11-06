from consts import *


class Feature(pygame.sprite.Sprite):
    """
    use to show the player info
    """
    gap = 40

    def __init__(self, manage, player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        # features screen
        self.image = FEATURE_IMAGE
        # the bullets and missiles
        self.bullets_rect = BULLETS_LEFT.get_rect()
        self.missiles_rect = MISSILE_LEFT.get_rect()
        self.bullets_rect.center = DATA_WIDTH // 2, SCREEN_Y - self.gap * 6
        self.missiles_rect.center = DATA_WIDTH // 2, SCREEN_Y - self.gap * 4
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.player = player
        manage.add_sprite(self)

    def show(self):
        bull = font.render(str(self.player.get_bullet_amount()), True, black)
        miss = font.render(str(self.player.get_missiles_amount()), True, black)
        gameDisplay.blit(BULLETS_LEFT, self.bullets_rect)
        gameDisplay.blit(MISSILE_LEFT, self.missiles_rect)
        gameDisplay.blit(bull, (
            self.bullets_rect.right - FEATURE_X // 2 - bull.get_width() // 2,
            self.bullets_rect.centery))
        gameDisplay.blit(miss, (
            self.missiles_rect.right - FEATURE_X // 2 - miss.get_width() // 2,
            self.missiles_rect.centery))
