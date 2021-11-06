import pygame


class Border(pygame.sprite.Sprite):
    def __init__(self, manage, x1, y1, x2, y2, type=False):
        """
        x1,x2,y1,y2 - borders
        type - False if its the end of the board
        else it just bring you up from the other side
        """
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x1, y1, x2, y2)
        manage.add_sprite(self)

        # border or between quarters
        self.type = type
