import random

from consts import *


class Collect(pygame.sprite.Sprite):
    """
    tokens are things you can collect, they give you things like shield or life
    """

    def __init__(self, manage):
        # add to the right list
        pygame.sprite.Sprite.__init__(self)
        manage.collects_group.add(self)
        # generate type
        self.manage = manage
        #print(manage.tokens_group)
        # a number represent the token
        self.type = random.randrange(0, len(manage.tokens_group) - 1)
        self.image = manage.tokens_group[self.type]
        # token location
        locx, locy = random.randrange(DATA_WIDTH + TOKEN_SIZE, SCREEN_X - TOKEN_SIZE),  random.randrange(TOKEN_SIZE, SCREEN_Y - TOKEN_SIZE)
        self.rect = pygame.Rect((locx, locy), (TOKEN_SIZE, TOKEN_SIZE))
        # makes the white color transparent
        self.image.set_colorkey(white)
        manage.tokens_counter[self.type] += 1
        # here you can add prob of cancellation
        if manage.tokens_counter[self.type] > MOST_OF_EACH:
            manage.collects_group.remove(self)
            manage.tokens_counter[self.type] -= 1
