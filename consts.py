# from os import path
import pygame
import random
import os

"""
try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()
    print(dir(pygame_sdl2))
except ImportError:
    pass
# img_dir = path.join(path.dirname(__file__), "img")
"""
"""
    @ define some colors
"""

white = (255, 255, 255)
black = (0, 0, 0)
grey = (100, 100, 100)
red = (200, 0, 0)
green = (0, 220, 0)
blue = (0, 0, 240)
yellow = (255, 255, 0)
color1 = (120, 190, 80)
color2 = (190, 120, 24)
color3 = (70, 50, 80)
color4 = (200, 0, 240)

"""
    @ game borders and pygame init
"""

pygame.init()
# pygame.mouse.set_visible(True)
infoObject = pygame.display.Info()

SCREEN_X = infoObject.current_w
SCREEN_Y = infoObject.current_h
# data is the left features
DATA_WIDTH = int(SCREEN_X / 6)
# the game size
B_SIZE_X = SCREEN_X - DATA_WIDTH
B_SIZE_Y = SCREEN_Y

BUTTON_GAP = int(SCREEN_Y / 10)
BUTTON_START_FROM_TOP = int(SCREEN_Y / 10)

SCREEN_CENTER = (SCREEN_X / 2 + DATA_WIDTH / 2, SCREEN_Y / 2)
SCREEN_HEADLINE = (SCREEN_X / 2 + DATA_WIDTH / 2, SCREEN_Y / 12)
BORDER_WIDTH = 0
HALF_SIZE_X = int(B_SIZE_X / 2)
HALF_BORDER = int(BORDER_WIDTH / 2)
BUTTON_MEDIUM_X = 320
BUTTON_MEDIUM_Y = 125
TOKEN_SIZE = 35

FEATURE_X = 120
FEATURE_Y = 65
# if true - when arrive to one wall comes back from the other one
ABLE_MIRROR_WALLS = True
# tank size
TANK_SIZE_X = 42
TANK_SIZE_Y = 42
HALF_TANK = int(TANK_SIZE_X / 2)

# debug
##gameDisplay = pygame.display.set_mode((int(), int()))
gameDisplay = pygame.display.set_mode((SCREEN_X, SCREEN_Y), pygame.FULLSCREEN)
pygame.display.set_caption("Slither")
font = pygame.font.SysFont("arialrounded", 17)
pygame.display.update()  # only update certain area
# clock to slow down the frames per seconds
clock = pygame.time.Clock()

"""
    @ images and animation handling
"""


def load_and_rescale(name, size_x=-1, size_y=-1):
    """
    :param name: name of the picture
    :param size_x:
    :param size_y:
    :return: image type of rescaled image
    """
    if os.path.exists(os.path.join("images", "{}.jpg".format(name))):
        img = pygame.image.load(os.path.join("images", "{}.jpg".format(name))).convert()
    elif os.path.exists(os.path.join("images", "{}.bmp".format(name))):
        img = pygame.image.load(os.path.join("images", "{}.bmp".format(name))).convert()
    else:
        img = pygame.image.load(os.path.join("images", "{}.png".format(name))).convert()

    img.set_colorkey(white)
    if size_x > 0:
        return pygame.transform.scale(img, (size_x, size_y))
    return img


def load_and_rescale_animation(name, size_x=-1, size_y=-1):
    """
    :param name: had to start with name0...name1...name2..
    :param frames: how many frames there is
    :return: a list of the images
    """
    anima = []
    i = 0
    while os.path.exists(os.path.join("images", "{0}{1}.jpg".format(name, i))) or os.path.exists(
            os.path.join("images", "{0}{1}.png".format(name, i))):
        img = load_and_rescale(name + str(i))
        i += 1
        img.set_colorkey(black)
        if size_x > 0:
            img = pygame.transform.scale(img, (size_x, size_y))
        anima.append(img)
    return anima


BULLET_IMAGE = load_and_rescale("laserGreen")
EXPLODE_IMAGE = load_and_rescale("laserGreenShot")
MISSILE_IMAGE = load_and_rescale("laserRed")
EXPLODE_MISSILE_IMAGE = load_and_rescale("laserRedShot")
SHIELD_IMAGE = load_and_rescale("tank_shield")
SHIELD_TRANSPARANCY = 120
SCREEN_IMAGE = load_and_rescale("space")

RULES_IMAGE = load_and_rescale("ruless", DATA_WIDTH * 5, DATA_WIDTH * 3)
# tokens
ADD_LIFE_TOKEN = load_and_rescale("add_life_token", TOKEN_SIZE, TOKEN_SIZE)
SHIELD_TOKEN = load_and_rescale("shield_token", TOKEN_SIZE, TOKEN_SIZE)
MISSILE_TOKEN = load_and_rescale("missile_token", TOKEN_SIZE, TOKEN_SIZE)
BULLETS_TOKEN = load_and_rescale("bullets_token", TOKEN_SIZE, TOKEN_SIZE)

FEATURE_IMAGE = load_and_rescale("features", DATA_WIDTH, SCREEN_Y)
MISSILE_LEFT = load_and_rescale("missiles_left", FEATURE_X, FEATURE_Y)
BULLETS_LEFT = load_and_rescale("bullets_left", FEATURE_X, FEATURE_Y)
# LIFE_LEFT = load_and_rescale("missiles_left", FEATURE_X, FEATURE_Y)

START_SCREEN = load_and_rescale("start_screen", SCREEN_X, SCREEN_Y)
GAME_NAME = load_and_rescale("name", BUTTON_MEDIUM_X * 3, BUTTON_MEDIUM_Y * 3)
# buttons
BEGIN_B = load_and_rescale("begin_b", BUTTON_MEDIUM_X, BUTTON_MEDIUM_Y)
BEGIN_BP = load_and_rescale("begin_bp", BUTTON_MEDIUM_X, BUTTON_MEDIUM_Y)
RULES_B = load_and_rescale("rules_b", BUTTON_MEDIUM_X, BUTTON_MEDIUM_Y)
RULES_BP = load_and_rescale("rules_bp", BUTTON_MEDIUM_X, BUTTON_MEDIUM_Y)
SETTING_B = load_and_rescale("settings_b", BUTTON_MEDIUM_X, BUTTON_MEDIUM_Y)
SETTING_BP = load_and_rescale("settings_bp", BUTTON_MEDIUM_X, BUTTON_MEDIUM_Y)
BACK_B = load_and_rescale("back_b", BUTTON_MEDIUM_X, BUTTON_MEDIUM_Y)
BACK_BP = load_and_rescale("back_bp", BUTTON_MEDIUM_X, BUTTON_MEDIUM_Y)
QUICK_GAME_B = load_and_rescale("quick_start_b", BUTTON_MEDIUM_X, BUTTON_MEDIUM_Y)
QUICK_GAME_BP = load_and_rescale("quick_start_bp", BUTTON_MEDIUM_X, BUTTON_MEDIUM_Y)
MULTY_PLAYER_B = load_and_rescale("multy_player_b", BUTTON_MEDIUM_X, BUTTON_MEDIUM_Y)
MULTY_PLAYER_BP = load_and_rescale("multy_player_bp", BUTTON_MEDIUM_X, BUTTON_MEDIUM_Y)
JOURNEY_B = load_and_rescale("journey_b", BUTTON_MEDIUM_X, BUTTON_MEDIUM_Y)
JOURNEY_BP = load_and_rescale("journey_bp", BUTTON_MEDIUM_X, BUTTON_MEDIUM_Y)
CONTINUE_B = load_and_rescale("continue_b", BUTTON_MEDIUM_X, BUTTON_MEDIUM_Y)
CONTINUE_BP = load_and_rescale("continue_bp", BUTTON_MEDIUM_X, BUTTON_MEDIUM_Y)
# texts
TEXT_X, TEXT_Y = int(SCREEN_X / 1.5), int(SCREEN_Y / 1.5)
TEXT_BACKGROUND = load_and_rescale("text_background", SCREEN_X, SCREEN_Y)
LEVEL1_TXT = load_and_rescale("level1_txt", TEXT_X, TEXT_Y)
LEVEL2_TXT = load_and_rescale("level2_txt", TEXT_X, TEXT_Y)
LEVEL3_TXT = load_and_rescale("level3_txt", TEXT_X, TEXT_Y)
level_to_promo = {1: LEVEL1_TXT, 2: LEVEL2_TXT, 3: LEVEL3_TXT}

ship_anim = load_and_rescale_animation("ship")
explode_anim = load_and_rescale_animation("expl", 120, 120)
missile_anim = load_and_rescale_animation("", 100, 38)

"""
    @ game parameters - speed and amounts 
"""
# speed of game
FRAMES_PER_SECOND = 34

# default tank speed
TANK_SPEED = 8
TANK_MAX_SPEED = 8
TANK_MIN_SPEED = 8

# default tank life
TANK_LIFE = 300

# bullets to start with
START_BULLETS = 700

# missiles to start with
START_MISSILES = 30

# bullet size
BULLET_SIZE = 6

# bullet speed
BULLET_SPEED = 20

# bullet strength
BULLET_STRENGTH = 20

# player or computer
PLR = True
CMP = False

DO_START_SCREEN = 0
GAME_LOOP = 1
INSTRUCTIONS = 2
CHOSE_GAME_MODE = 3
SETTINGS = 4
JOURNEY = 5


SHORT_WALK = 50
LONG_WALK = 300

# generate tokes
PROB_OF_GEN = 20
MOST_OF_EACH = 2
SHIELD_TIME = 600

# consts for movement change clockwise and anticlockwise
FASTER = 0
SLOWER = 1
#
CW = 2
ACW = 3
#
TEAM_A = 0
TEAM_B = 1

# game modes:
SIMPLE = 0
JOURNEY = 1
MULTY = 2
RACE = 3
CAMPS = 4
# buttons locations
BOTTUN_LOC_1 = (HALF_SIZE_X, BUTTON_START_FROM_TOP)
BOTTUN_LOC_2 = (HALF_SIZE_X, BUTTON_START_FROM_TOP + BUTTON_GAP)
BOTTUN_LOC_3 = (HALF_SIZE_X, BUTTON_START_FROM_TOP + 2 * BUTTON_GAP)
BOTTUN_LOC_4 = (HALF_SIZE_X, BUTTON_START_FROM_TOP + 3 * BUTTON_GAP)

# situatios
LOST = 1
WON = 2
KEEP_PLAY = 0

# moves for computer
move_options = [FASTER, SLOWER, CW, ACW]
MOVES = [dict(zip(move_options, [True, False, False, False])),
         dict(zip(move_options, [False, True, False, False])),
         dict(zip(move_options, [False, False, True, False])),
         dict(zip(move_options, [False, False, False, True])),
         dict(zip(move_options, [True, False, True, False])),
         dict(zip(move_options, [False, True, False, True])),
         dict(zip(move_options, [True, False, False, True])),
         dict(zip(move_options, [False, True, True, False])),
         dict(zip(move_options, [False, False, False, False]))]

SPIN_MOVES = [dict(zip(move_options, [False, False, True, False])),
              dict(zip(move_options, [False, False, False, True])),
              dict(zip(move_options, [False, False, False, False]))]


# levels
def gen_in_board():
    return random.randrange(DATA_WIDTH, SCREEN_X), random.randrange(DATA_WIDTH, SCREEN_X)


# teams sides - there can be tanks in my team
sizeA1, sizeB1 = 2, 2
sizeAll1 = sizeA1 + sizeB1
sizeA2, sizeB2 = 3, 3
sizeAll2 = sizeA2 + sizeB2
sizeA3, sizeB3 = 3, 3
sizeAll3 = sizeA3 + sizeB3

level1_tankprms = {0: {"missiles": START_MISSILES, "bullets": START_BULLETS, "life": TANK_LIFE},
                   1: {"missiles": START_MISSILES, "bullets": START_BULLETS, "life": TANK_LIFE},
                   2: {"missiles": START_MISSILES, "bullets": START_BULLETS, "life": TANK_LIFE},
                   3: {"missiles": START_MISSILES, "bullets": START_BULLETS, "life": TANK_LIFE}}

level2_tankprms = {0: {"missiles": START_MISSILES, "bullets": START_BULLETS, "life": TANK_LIFE},
                   1: {"missiles": START_MISSILES, "bullets": START_BULLETS, "life": TANK_LIFE},
                   2: {"missiles": START_MISSILES, "bullets": START_BULLETS, "life": TANK_LIFE},
                   3: {"missiles": START_MISSILES, "bullets": START_BULLETS, "life": TANK_LIFE},
                   4: {"missiles": START_MISSILES, "bullets": START_BULLETS, "life": TANK_LIFE},
                   5: {"missiles": START_MISSILES, "bullets": START_BULLETS, "life": TANK_LIFE}}

level3_tankprms = {0: {"missiles": START_MISSILES, "bullets": START_BULLETS, "life": TANK_LIFE},
                   1: {"missiles": START_MISSILES, "bullets": START_BULLETS, "life": TANK_LIFE},
                   2: {"missiles": START_MISSILES, "bullets": START_BULLETS, "life": TANK_LIFE},
                   3: {"missiles": START_MISSILES, "bullets": START_BULLETS, "life": TANK_LIFE},
                   4: {"missiles": START_MISSILES, "bullets": START_BULLETS, "life": TANK_LIFE},
                   5: {"missiles": START_MISSILES, "bullets": START_BULLETS, "life": TANK_LIFE}}

levelargs = {
    1: {"teamA": sizeA1, "teamB": sizeB1,
        "locations": dict(zip(list(i for i in range(sizeAll1)), list(gen_in_board() for i in range(sizeAll1)))),
        "screen_image": SCREEN_IMAGE,
        "tanks_prms": level1_tankprms},

    2: {"teamA": sizeA2, "teamB": sizeB2,
        "locations": dict(zip(list(i for i in range(sizeAll2)), list(gen_in_board() for i in range(sizeAll2)))),
        "screen_image": SCREEN_IMAGE,
        "tanks_prms": level2_tankprms},

    3: {"teamA": sizeA3, "teamB": sizeB3,
        "locations": dict(zip(list(i for i in range(sizeAll3)), list(gen_in_board() for i in range(sizeAll3)))),
        "screen_image": SCREEN_IMAGE, "tanks_prms": level3_tankprms}
}
