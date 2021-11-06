from bullet import Bullet
from consts import *
from mobile import Mobile


class Tank(Mobile):
    """
    tank manage
    """

    # collision with bullet
    full_time_hit_by_bullet = 23
    full_time_die = 23
    collidex = 32
    collidey = 32

    # tank sizes
    tankx = 44
    tanky = 44
    shieldx = 100
    shieldy = 74

    # time of loading a new shoot
    time_of_loading = 20


    # gap between the tank and the life and load
    gap_to_attr = 5
    attr_width = 4
    life_extra = 60

    def __init__(self, manage, startfrom, speed, life, bullet_speed, bullet_power, id, type, anim_name, team, numofbullets, numofmissiles):
        """
        @params
        speed       : int - speed of tank
        life        : int - how much life the tank has
        bullet_speed: if a bullet comes out of it, this will be the bullets speed
        bullet_power: if a bullet comes out of it, this will be the bullets damage 
        id          : id of player 
        type        : PLR for human player and CMP for computer player
        image_name  : name of the image that represent the tank
        
        
        @auto initialize
        image       : the image that represent tank
        rect        : Rect - position and size of the tank.
        vec         : direction of the tank
        togo        : if its a computer player, he
                      has togo more to go before he thinks again
                      where he should move
        """

        # make it a sprite, and moveable
        Mobile.__init__(self)

        # parameters:
        self.manage = manage
        self.speed = TANK_MAX_SPEED
        self.life = life
        self.bullet_speed = bullet_speed
        self.bullet_power = bullet_power
        self.id = id
        self.type = type

        self.full_bullet_amount = 300
        self.full_missile_amount = 400
        # auto initialize:
        self.bullet_amount = self.full_bullet_amount
        self.missile_amount = self.full_missile_amount

        # image and rectangle
        self.animation = anim_name
        self.image = anim_name[int(len(anim_name) / 2)]
        self.image = pygame.transform.scale(self.image, (self.tankx, self.tanky))
        self.image.set_colorkey(black)

        self.rect = self.image.get_rect()
        self.rect.center = startfrom

        self.team = team
        # if its a COM - he has togo more clock ticks before he think again
        self.togo = 0

        # fully load the bullet
        self.time_load_bullet = self.time_of_loading

        # fully time of dying
        self.time_die = self.full_time_die

        # explodes - why its here - because it is used in show
        image_of_collision = EXPLODE_IMAGE
        self.image_of_collision = pygame.transform.scale(image_of_collision, (self.tankx, self.tanky))
        self.image_of_collision.set_colorkey(black)
        self.time_of_hit = 0

        # shield
        image_of_shield = SHIELD_IMAGE
        self.image_of_shield = pygame.transform.scale(image_of_shield, (self.shieldx, self.shieldy))
        self.image_of_shield.set_colorkey(black)
        # define transparency of shield 
        self.image_of_shield.set_alpha(SHIELD_TRANSPARANCY)
        self.time_of_shield = 0

        self.frame = int(len(anim_name) / 2)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 12
        # add tank to the tanks group
        manage.add_sprite(self)

    def update_image(self):
        """
        for animated vision - update image of tank
        :return:
        """
        now = pygame.time.get_ticks()
        # its been at least that losg
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            # todo = {FASTER: False, SLOWER: False, CW: False, ACW: False}
            if self.todo[CW]:
                self.frame = min(self.frame + 1, len(self.animation) - 1)
            if self.todo[ACW]:
                self.frame = max(self.frame - 1, 0)
            if not self.todo[CW] and not self.todo[ACW] and self.frame != int(len(self.animation) / 2):
                self.frame = self.frame - 1 if self.frame > int(len(self.animation) / 2) else self.frame + 1

            self.image = self.animation[self.frame]

    def land(self):
        """
        descrice what happens when a tank is landing

        """
        self.bullet_amount = self.full_bullet_amount
        for act in self.todo:
            self.todo[act] = False

    def _location_heur(self, tmp_rect):  # need a massive work
        """
        it has all the data
        return heuristic about how good is the position
        """
        x, y = tmp_rect.centerx, tmp_rect.centery
        h = 0
        for bullet in self.manage.bullets_group:
            if bullet.belong_to != self.id:
                h += abs(bullet.rect.centerx - self.rect.centerx) + abs(bullet.rect.centery - self.rect.centery)
        return h

    def _location_heur1(self, tmp_rect):  # need a massive work
        """
        tmp_rect: the rectangel representing the location of where
                  the tank could be
        it has all the data
        return heuristic about how good is the position
        """
        x, y = tmp_rect.centerx, tmp_rect.centery
        h = 0
        for bullet in self.manage.bullets_group:
            # if its a bullet to watch out from
            if bullet.aim_to == self.quar.id:
                # same row - row collision
                if (bullet.rect.top <= self.rect.bottom and bullet.rect.bottom >= self.rect.top) and (
                            bullet.drt[RIGHT] or bullet.drt[LEFT]):
                    h += abs(bullet.rect.centerx - x) * abs(y - bullet.rect.centery)
                # same col - col collision
                if (bullet.rect.left <= self.rect.right and bullet.rect.right >= self.rect.left) and (
                            bullet.drt[UP] or bullet.drt[DOWN]):
                    h += abs(bullet.rect.centerx - x) * abs(y - bullet.rect.centery)
        return h

    def is_possible_dirt(self, tmp_rect):
        """
        get a rect of imaginary position and return True if this position is in the quarter
        """
        return not (
            tmp_rect.right >= self.quar.right_b or tmp_rect.left <= self.quar.left_b or tmp_rect.bottom >= self.quar.lower_b or tmp_rect.top <= self.quar.upper_b)

    def add_life(self):
        self.life = min(self.life + self.life_extra, TANK_LIFE)

    def shield_up(self):
        self.time_of_shield = SHIELD_TIME

    def think_then_move(self):
        """
        think where should move, then actually
        call change_location for the tank
        """
        for tank in self.manage.tanks_group:
            # case its human
            if tank.type == PLR:
                tank.change_location()
            # its a computer player
            else:
                # randomly shoot and spin - can be much better
                r = random.randrange(0, 100)
                if 4 < r < 18 and tank.time_load_bullet == tank.time_of_loading:
                    tank.time_load_bullet = 0
                    Bullet(self.manage, tank)
                if tank.togo <= 0:
                    tank.togo = random.randrange(SHORT_WALK, LONG_WALK)
                    best_h = -1  # min value
                    best_move = []
                    # print("start")
                    DIRECTIONS = MOVES
                    random.shuffle(DIRECTIONS)
                    for drt in DIRECTIONS:
                        #   situation of the board
                        situation = tank.virtual_move(drt, tank.togo)
                        heuristic = tank._location_heur(situation)
                        if heuristic > best_h:
                            best_h = heuristic
                            best_move = drt
                    tank.todo = best_move
                else:
                    tank.change_location()
                    tank.togo -= 1

    @staticmethod
    def out_of_border():
        """
        return nothing, yet if a tank hit a border, don't
        let him go any further
        """
        for tank in Manager.tanks_group:
            if tank.rect.right >= tank.quar.right_b:
                tank.drt[RIGHT] = False
            if tank.rect.left <= tank.quar.left_b:
                tank.drt[LEFT] = False
            if tank.rect.bottom >= tank.quar.lower_b:
                tank.drt[DOWN] = False
            if tank.rect.top <= tank.quar.upper_b:
                tank.drt[UP] = False

    def get_bullet_amount(self):
        return self.bullet_amount

    def get_missiles_amount(self):
        return self.missile_amount
