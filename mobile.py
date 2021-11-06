from consts import *
import math


class Mobile(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # direction movement - very important
        self.todo = {FASTER: False, SLOWER: False, CW: False, ACW: False}
        self.do_action = {FASTER: self.go_faster, SLOWER: self.go_slower, CW: self.go_cw, ACW: self.go_acw}

        self.speed = 0
        self.angle = 0

        self.accelerate = 1
        self.angular_velocity = 5


    def go_faster(self):
        self.speed = min(self.speed + self.accelerate, TANK_MAX_SPEED)

    def go_slower(self):
        if self.speed >= TANK_MIN_SPEED:
            self.speed = max(self.speed - self.accelerate, TANK_MIN_SPEED)
        else:
            self.speed = max(self.speed - self.accelerate, 0)

    def go_cw(self):
        self.angle = (self.angle + self.angular_velocity) % 360

    def go_acw(self):
        self.angle = (self.angle - self.angular_velocity) % 360

    def change_location(self):
        """
        move an object
        """

        # this loop update speed and angle
        for action in self.todo:
            if self.todo[action]:
                self.do_action[action]()

        # update location
        self.rect = self.rect.move(-math.sin(math.radians(self.angle)) * self.speed,
                                   -math.cos(math.radians(self.angle)) * self.speed)

    def virtual_move(self, drt, togo):
        """
        get an object and return when it will be after togo moves
        important note - does not return the centre
        the reason it is important is that it used for heuristic purpose later 
        """
        newspeed, newangle = self.speed, self.angle
        if drt[FASTER]:
            newspeed = min(self.speed + self.accelerate, TANK_MAX_SPEED)
        elif drt[SLOWER]:
            newspeed = max(self.speed - self.accelerate, TANK_MIN_SPEED)
        if drt[CW]:
            newangle = (self.angle + self.angular_velocity) % 360
        elif drt[ACW]:
            newangle = (self.angle - self.angular_velocity) % 360

        return self.rect.move(math.sin(newangle) * newspeed * togo, math.cos(newangle) * newspeed * togo)

    def get_speed(self):
        return self.speed