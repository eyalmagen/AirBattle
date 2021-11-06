from math import atan2, degrees

from consts import *
from explosion import Explosion


class Manager():
    """
    this class manage groups of all the objects
    """

    def __init__(self):

        self.tanks_group = pygame.sprite.Group()
        self.bullets_group = pygame.sprite.Group()
        self.borders_group = pygame.sprite.Group()
        self.collects_group = pygame.sprite.Group()
        self.explosions_group = pygame.sprite.Group()
        self.runways_group = pygame.sprite.Group()
        self.features_group = pygame.sprite.Group()
        self.buttons_group = pygame.sprite.Group()
        self.missile_group = pygame.sprite.Group()


        exist_token = [ADD_LIFE_TOKEN, SHIELD_TOKEN, MISSILE_TOKEN, BULLETS_TOKEN]
        self.tokens_group = dict(zip(range(len(exist_token)), exist_token))
        self.tokens_counter = dict(zip(range(len(exist_token)), range(len(exist_token))))

        self.type_to_group = {"Bullet": self.bullets_group,
                              "Border": self.borders_group,
                              "Tank": self.tanks_group,
                              "Token": self.collects_group,
                              "Explosion": self.explosions_group,
                              "Runway": self.runways_group,
                              "Feature": self.features_group,
                              "Button": self.buttons_group,
                              "Missile": self.missile_group
                              }

    def add_sprite(self, obj):
        """
        :param obj: a sprite of any kind
        add it to his kind of sprite
        """
        # print(obj)
        self.type_to_group[obj.__class__.__name__].add(obj)

    def delete_all_sprites(self):
        """
        simply empty all the groups
        """
        for type in self.type_to_group:
            self.type_to_group[type].empty()

    def angle_between_sprite(self, sp1, sp2):
        """

        :param sp1: sprite 1
        :param sp2: sprite 2
        :return: the angle between then - 0 - 270 - 180 - 90 (like tank)
        """
        p1x, p1y, p2x, p2y = sp1.rect.centerx, sp1.rect.centery, sp2.rect.centerx, sp2.rect.centery
        dx = p2x - p1x
        dy = p2y - p1y
        rads = atan2(-dy, dx)
        # to match the tank degrees +270
        return int(degrees(rads) + 270) % 360

    def tank_most_in_object_way(self, ob):
        """
        :param ob: object on which we check - return a
        :return: a dictionary which represent the move that ob should do in order be in a tank direction.
        """
        # angle of the object right now
        angle_of_ob = ob.angle
        # to find the tank that is currently most in range, we want the object to orient it
        most_in_range = 360
        best_angle_between_2 = 360

        # distinguish between a missile and a tank as ob
        check_not_myself = None
        # case its a missile
        if ob.__class__.__name__ == "Missile":
            check_not_myself = ob.belong_to
        # case its a tank
        else:
            check_not_myself = ob.id

        # for each tank
        for tank in self.tanks_group:
            if tank.id != check_not_myself:
                # angle between the two sprites - uses arctan
                angle_between_2 = self.angle_between_sprite(ob, tank)
                # the difference in absolute value
                diff = max(angle_between_2, angle_of_ob) - min(angle_between_2, angle_of_ob)
                if (diff >= 180):
                    diff = 360 - diff
                if diff < most_in_range:
                    most_in_range = diff
                    # to use later
                    best_angle_between_2 = angle_between_2

        # case its 0 difference - exactly in the right direction
        if most_in_range == 0:
            return SPIN_MOVES[2]
        # this chunk of code is to determine whether ob should turn left or right
        diff = max(best_angle_between_2, angle_of_ob + ob.angular_velocity) - min(best_angle_between_2,
                                                                                  angle_of_ob + ob.angular_velocity)
        if (diff > 180):
            diff = 360 - diff
        if diff < most_in_range:
            return SPIN_MOVES[0]
        return SPIN_MOVES[1]

    def which_spin_get_me_closer(self, mobile_ob, look_for_ob, togo=1):
        """
        :param mobile_ob: the parameter has to be mobile
        :param look_for_ob: a string the class name, of what the object is looking for
        :param width: the width of the strip
        :return: the center of the closest "type" object
        """
        # going over all the sprites of look_for_ob type
        tmp = 0
        best_move = dict(zip(move_options, [False, False, False, False]))
        min_distance = 3
        for not_moving_obj in self.type_to_group[look_for_ob]:
            if mobile_ob.belong_to != not_moving_obj.id:
                for drt in SPIN_MOVES:
                    move_new_distance = self.get_new_distance(mobile_ob, not_moving_obj, drt)
                    if move_new_distance < min_distance:
                        print(move_new_distance)
                        min_distance = move_new_distance
                        best_move = drt
        return best_move

    def tanks_collide_bullets(self):
        # tanks_collide_bullets = {tank1 : [bull1, bull2], ....}
        tanks_collide_bullets = pygame.sprite.groupcollide(self.tanks_group, self.bullets_group, False, False)
        for tank in tanks_collide_bullets:
            # bullets who hit the specific tank
            for bull in tanks_collide_bullets[tank]:
                if tank.id != bull.belong_to:
                    tank.time_of_hit = tank.full_time_hit_by_bullet
                    self.bullets_group.remove(bull)
                    if tank.time_of_shield == 0:
                        tank.life -= bull.strength
                    # his life is over so he's gone
                    if tank.life <= 0:
                        Explosion(self, tank)
                        self.tanks_group.remove(tank)

    def tanks_collide_missiles(self):
        # tanks_collide_bullets = {tank1 : [bull1, bull2], ....}
        tanks_collide_missiles = pygame.sprite.groupcollide(self.tanks_group, self.missile_group, False, False)
        for tank in tanks_collide_missiles:
            # bullets who hit the specific tank
            for miss in tanks_collide_missiles[tank]:
                if tank.id != miss.belong_to:
                    # tank.time_of_hit = tank.full_time_hit_by_bullet
                    self.missile_group.remove(miss)
                    if tank.time_of_shield == 0:
                        Explosion(self, tank)
                        tank.life -= miss.strength
                    # his life is over so he's gone
                    if tank.life <= 0:
                        Explosion(self, tank)
                        self.tanks_group.remove(tank)

    def bullets_collide_walls(self):
        """
        erase the bullets which hit the walls

        """
        # Explosion(self.manage, )
        pygame.sprite.groupcollide(self.borders_group, self.bullets_group, False, True)
        pygame.sprite.groupcollide(self.features_group, self.bullets_group, False, True)

    def missiles_collide_walls(self):
        """
        erase the bullets which hit the walls

        """
        pygame.sprite.groupcollide(self.borders_group, self.missile_group, False, True)
        pygame.sprite.groupcollide(self.features_group, self.missile_group, False, True)

    def tank_collide_walls(self):
        """
        erase the bullets which hit the walls
        """
        tanks_collide_walls = pygame.sprite.groupcollide(self.borders_group, self.tanks_group, False, False)
        for border in tanks_collide_walls:
            for tank in tanks_collide_walls[border]:
                if not border.type:
                    Explosion(self, tank)
                    tank.kill()

    def tanks_collide_tokens(self):
        """
        takes the tokes.

        """
        tanks_collide_tokens = pygame.sprite.groupcollide(self.tanks_group, self.collects_group, False, True)
        for tank in tanks_collide_tokens:
            for token in tanks_collide_tokens[tank]:
                if token.image == ADD_LIFE_TOKEN:
                    tank.add_life()
                if token.image == SHIELD_TOKEN:
                    tank.shield_up()
                if token.image == MISSILE_TOKEN:
                    tank.missile_amount += 5
                if token.image == BULLETS_TOKEN:
                    tank.bullet_amount += 50
                self.tokens_counter[token.type] -= 1

    def tanks_collide_runways(self):
        tanks_collide_runways = pygame.sprite.groupcollide(self.tanks_group, self.runways_group, False, False)
        for tank in tanks_collide_runways:
            # print(tank.speed, TANK_MIN_SPEED, tank.angle, )
            if tank.speed == TANK_MIN_SPEED and tank.angle % 180 <= 20:
                tank.land()

    def get_human(self):
        """"
        return a list of the human players
        """
        h_tanks = []
        for tank in self.tanks_group:
            # if a real human player
            if tank.type == True:
                h_tanks.append(tank)
        return h_tanks
