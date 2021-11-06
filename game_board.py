from border import Border
from collect import Collect
from consts import *
from feature import Feature
from tank import Tank


class Game_board():
    """
    handle the game board - fill it, print things to the screen
    initialize walls and players
    all the methods are static
    """

    def __init__(self, manage, game_mode, levelargs):
        self.manage = manage
        # initialize players and walls
        if game_mode == JOURNEY:
            Game_board.init_players(self, levelargs)
        if game_mode == SIMPLE:
            Game_board.init_players(self, levelargs)

        Game_board.init_walls(self)

    @staticmethod
    def message_to_screen(msg, color):
        """
        print a message to the board middle
        """
        screen_text = font.render(msg, True, color)
        gameDisplay.blit(screen_text, (B_SIZE_X / 2, B_SIZE_Y / 2))

    def init_players(self, levelargs):
        """
        initialize the players and their positions
        base on the game mode - race/journyey...

        levelargs format:
        level1_tankprms = {1: {"missiles": 5, "bullets": 100, "life": 220}, 2: {"missiles": 5, "bullets": 100, "life": 220},
                           3: {"missiles": 5, "bullets": 100, "life": 220}, 4: {"missiles": 5, "bullets": 100, "life": 220}}
        levelargs = {
            1: {"teamA": 1,
                "teamB": 3,
                "locations": {1: gen_in_board(), 2: gen_in_board(), 3: gen_in_board(), 4: gen_in_board()},
                "screen_image": SCREEN_IMAGE,
                "tanks_prms": level1_tankprms}
                .
                .
            }
        """
        # the user

        player1 = Tank(self.manage, levelargs["locations"][0], TANK_SPEED, TANK_LIFE, BULLET_SPEED,
                       BULLET_STRENGTH, 0, PLR, ship_anim, TEAM_A, levelargs["tanks_prms"][0]["bullets"],
                       levelargs["tanks_prms"][0]["missiles"])
        Feature(self.manage, player1)
        # with me tanks -1 is minus the player
        for i in range(1, levelargs["teamA"]):
            Tank(self.manage, levelargs["locations"][i], TANK_SPEED, TANK_LIFE, BULLET_SPEED, BULLET_STRENGTH, i,
                 CMP, ship_anim, TEAM_A, levelargs["tanks_prms"][i]["bullets"],
                 levelargs["tanks_prms"][i]["missiles"])
        # enemy team
        for i in range(levelargs["teamA"], levelargs["teamA"] + levelargs["teamB"]):
            Tank(self.manage, levelargs["locations"][i], TANK_SPEED, TANK_LIFE, BULLET_SPEED, BULLET_STRENGTH, i,
                 CMP, ship_anim, TEAM_B, levelargs["tanks_prms"][i]["bullets"],
                 levelargs["tanks_prms"][i]["missiles"])


    def init_walls(self):
        """
        the last True is for mirror attribute

        """
        # used to kill bullets when they hit the end_of_board
        Border(self.manage, DATA_WIDTH, 0, BORDER_WIDTH, B_SIZE_Y, True)  # stand left
        Border(self.manage, SCREEN_X - BORDER_WIDTH, 0, BORDER_WIDTH, B_SIZE_Y, True)  # stand - right
        Border(self.manage, DATA_WIDTH, 0, B_SIZE_X, BORDER_WIDTH, True)  # lay - top
        Border(self.manage, DATA_WIDTH, B_SIZE_Y - BORDER_WIDTH, B_SIZE_X, BORDER_WIDTH, True)  # lay - bottom

    def generate_tokens(self):
        r = random.randrange(0, PROB_OF_GEN)
        if r == 1:
            Collect(self.manage)

    def tick_the_clock(self):
        for tank in self.manage.tanks_group:
            # load more the bullet
            tank.time_load_bullet = min(tank.time_load_bullet + 3, tank.time_of_loading)
            tank.time_of_shield = max(tank.time_of_shield - 1, 0)
            tank.time_of_hit = max(tank.time_of_hit - 1, 0)
            """
            tank.time_rotate = min(tank.time_rotate + rotate_tank_speed, 0) if not tank.rotate_with_clock else max(
                tank.time_rotate - rotate_tank_speed, -90)

            """

    @staticmethod
    def fill_board():
        """
        fill the board with the right screen
        """
        gameDisplay.fill(blue)

    def show_tanks_id_and_stop_all(self):
        for tank in self.manage.tanks_group:
            screen_text = font.render(str(tank.id), True, black)
            gameDisplay.blit(screen_text, tank.rect.center)
            if tank.id != 1:
                for t in tank.todo:
                    tank.todo[t] = False
                    tank.speed = 0

    def show(self):

        """
        print the tank on screen
        and his life and how load is bullet is
        """

        # runways
        for runway in self.manage.runways_group:
            gameDisplay.blit(runway.image, runway.rect)

        for missile in self.manage.missile_group:
            missile.change_location()
            rot_image = pygame.transform.rotate(missile.image, missile.angle - 90)
            rot_rect = rot_image.get_rect()
            rot_rect.center = missile.rect.center
            missile.update()
            gameDisplay.blit(rot_image, rot_rect)
        # bullets
        for bull in self.manage.bullets_group:
            bull.change_location()
            rot_image = pygame.transform.rotate(bull.image, bull.angle)
            rot_rect = rot_image.get_rect()
            rot_rect.center = bull.rect.center
            gameDisplay.blit(rot_image, rot_rect)

        # tank
        for tank in self.manage.tanks_group:
            tank.angle = tank.angle % 360
            tank.update_image()
            if ABLE_MIRROR_WALLS:
                if tank.rect.bottom < 0:
                    tank.rect.centery += (SCREEN_Y + TANK_SIZE_Y) - 1
                elif tank.rect.top > SCREEN_Y:
                    tank.rect.centery -= (SCREEN_Y + TANK_SIZE_Y) + 1
                elif tank.rect.left > SCREEN_X:
                    tank.rect.centerx -= (SCREEN_X + TANK_SIZE_X - DATA_WIDTH) + 1
                elif tank.rect.right < DATA_WIDTH:
                    tank.rect.centerx += (SCREEN_X + TANK_SIZE_X - DATA_WIDTH) - 1

            # print(tank.rect.centery)
            rot_image = pygame.transform.rotate(tank.image, tank.angle)
            rot_rect = rot_image.get_rect()
            rot_rect.center = tank.rect.center
            gameDisplay.blit(rot_image, rot_rect)
            # the attrubutes
            shoot_color = green if tank.time_load_bullet < tank.time_of_loading else yellow
            temp_load = pygame.Rect(tank.rect.left, tank.rect.bottom + 3 * tank.gap_to_attr,
                                    tank.time_load_bullet / tank.time_of_loading * tank.rect.width, tank.attr_width)
            temp_life = pygame.Rect(tank.rect.left, tank.rect.bottom + 2 * tank.gap_to_attr,
                                    tank.life / TANK_LIFE * tank.rect.width, tank.attr_width)
            # blit the life and load.
            pygame.draw.rect(gameDisplay, shoot_color, temp_load)
            pygame.draw.rect(gameDisplay, red, temp_life)
            pygame.draw.rect(gameDisplay, black, temp_load, 1)
            pygame.draw.rect(gameDisplay, black, temp_life, 1)

            # if tank is human
            if tank.id == 0:
                pygame.draw.circle(gameDisplay, red, tank.rect.center, 50, 4)
            if tank.team == TEAM_B:
                pygame.draw.circle(gameDisplay, white, tank.rect.center, 70, 3)
            # still have shield
            if tank.time_of_shield > 0:
                x, y = tank.rect.topleft
                x -= tank.shieldx / 3
                y -= tank.tanky / 2
                gameDisplay.blit(tank.image_of_shield, (x, y))
            if tank.time_of_hit > 0 and tank.time_of_shield == 0:
                gameDisplay.blit(tank.image_of_collision, tank.rect)

        for collect in self.manage.collects_group:
            gameDisplay.blit(collect.image, collect.rect)

        for wall in self.manage.borders_group:
            pygame.draw.rect(gameDisplay, grey, wall)

        # explosions
        for expl in self.manage.explosions_group:
            gameDisplay.blit(expl.image, expl.rect)
            expl.update()

        for feature in self.manage.features_group:
            gameDisplay.blit(feature.image, feature.rect)
            feature.show()


