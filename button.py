from consts import *


class Button(pygame.sprite.Sprite):
    def __init__(self, manage, image, pressed_image, center_loc, action):
        pygame.sprite.Sprite.__init__(self)
        self.manage = manage

        self.is_currently_pressed = False
        self.image = image
        self.pressed_image = pressed_image
        self.unpressed_image = image
        self.rect = self.image.get_rect()
        x, y = center_loc
        x, y = int(x), int(y)
        center_loc = x, y
        self.rect.center = center_loc

        self.action = action
        manage.add_sprite(self)

    def handle_button(self, mouse_action):
        mouse_pos = pygame.mouse.get_pos()
        # true if the action is inside the button
        is_inside = self.is_inside_botton(mouse_pos)
        # someone pressed on it, now hes letting go on it, and its done inside the buttom  -  do the buttoms job
        if self.is_currently_pressed and mouse_action == pygame.MOUSEBUTTONUP and is_inside:
            self.action()

        if mouse_action == pygame.MOUSEBUTTONUP:
            self.is_currently_pressed = False
            self.image = self.unpressed_image

        if mouse_action == pygame.MOUSEBUTTONDOWN and is_inside:
            self.is_currently_pressed = True
            self.image = self.pressed_image

        if not is_inside:
            self.image = self.unpressed_image

        if self.is_currently_pressed and is_inside:
            self.image = self.pressed_image

    def is_inside_botton(self, point):
        return self.rect.collidepoint(point)

    def show(self):
        gameDisplay.blit(self.image, self.rect)
