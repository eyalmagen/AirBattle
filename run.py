from bullet import Bullet
from button import Button
from consts import *
from game_board import Game_board
from manager import Manager
from missile import Missile


class Run():
    def __init__(self):
        self.manage = Manager()
        self.next_step = {0: self.do_start_screen, 1: self.game_loop, 2: self.instructions, 3: self.chose_game_play}
        self.option = 0
        
        
        # multy player or journey
        self.mode = 0
        self.mode_dic = {0: "regular", 1: "journey", 2: "multy"}
        self.level = 1
        self.start_screen_rect = START_SCREEN.get_rect()
        self.buttons_gap = BUTTON_MEDIUM_Y + 30
        self.start_from_top = BUTTON_MEDIUM_Y * 3
        self.game_name_rect = GAME_NAME.get_rect()
        self.game_name_rect.center = int(SCREEN_X / 2), self.start_from_top - self.buttons_gap - 20
        while True:
            self.next_step[self.option]()

    def show_and_handle_buttons(self):
        for button in self.manage.buttons_group:
            button.show()
        pygame.display.update()
        for event in pygame.event.get():

            # press exit
            if event.type == pygame.QUIT or event.type == pygame.K_TAB:
                pygame.quit()
                exit()
            for button in self.manage.buttons_group:
                button.handle_button(event.type)

    def chose_game_play(self):
        """
        display choosing between journey, multiplayer and quick start
        :return:
        """
        self.manage.delete_all_sprites()
        mid_screen_x = SCREEN_X / 2  # - BUTTON_MEDIUM_X / 2
        # go back
        Button(self.manage, BACK_BP, BACK_B, (int(BUTTON_MEDIUM_X / 2), self.start_from_top + 2 * self.buttons_gap),
               self.do_start_screen)
        # quick start simple game
        Button(self.manage, QUICK_GAME_BP, QUICK_GAME_B, (mid_screen_x, self.start_from_top), self.game_loop)
        # start multy player
        Button(self.manage, MULTY_PLAYER_BP, MULTY_PLAYER_B, (mid_screen_x, self.start_from_top + self.buttons_gap),
               self.game_loop)
        # start journey
        Button(self.manage, JOURNEY_BP, JOURNEY_B, (mid_screen_x, self.start_from_top + 2 * self.buttons_gap),
               self.text_promo)
        rules_rect = RULES_IMAGE.get_rect()
        rules_rect.center = self.start_screen_rect.center

        while True:
            gameDisplay.blit(START_SCREEN, self.start_screen_rect)
            gameDisplay.blit(GAME_NAME, self.game_name_rect)
            self.show_and_handle_buttons()

    def text_promo(self):
        self.mode = 1
        self.manage.delete_all_sprites()
        txt_rect = level_to_promo[self.level].get_rect()
        txt_rect.center = SCREEN_CENTER
        # go back
        Button(self.manage, CONTINUE_BP, CONTINUE_B, (BUTTON_MEDIUM_X, SCREEN_Y - BUTTON_MEDIUM_Y),
               self.game_loop)
        while True:
            gameDisplay.blit(TEXT_BACKGROUND, self.start_screen_rect)
            gameDisplay.blit(level_to_promo[self.level], txt_rect)
            self.show_and_handle_buttons()

    def instructions(self):
        self.manage.delete_all_sprites()
        Button(self.manage, BACK_B, BACK_BP, (BUTTON_MEDIUM_X, SCREEN_Y - BUTTON_MEDIUM_Y), self.do_start_screen)
        rules_rect = RULES_IMAGE.get_rect()
        rules_rect.center = self.start_screen_rect.center

        while True:
            gameDisplay.blit(START_SCREEN, self.start_screen_rect)
            gameDisplay.blit(RULES_IMAGE, rules_rect)
            self.show_and_handle_buttons()

    def settings_screen(self):
        self.manage.delete_all_sprites()
        # go back
        Button(self.manage, BACK_BP, BACK_B, (int(BUTTON_MEDIUM_X / 2), self.start_from_top + 2 * self.buttons_gap),
               self.do_start_screen)
        while True:
            gameDisplay.blit(START_SCREEN, self.start_screen_rect)
            gameDisplay.blit(GAME_NAME, self.game_name_rect)
            self.show_and_handle_buttons()

    def do_start_screen(self):
        self.manage.delete_all_sprites()
        mid_screen_x = SCREEN_X / 2  # - BUTTON_MEDIUM_X / 2
        Button(self.manage, BEGIN_BP, BEGIN_B, (mid_screen_x, self.start_from_top), self.chose_game_play)
        Button(self.manage, RULES_BP, RULES_B, (mid_screen_x, self.start_from_top + self.buttons_gap),
               self.instructions)
        Button(self.manage, SETTING_BP, SETTING_B, (mid_screen_x, self.start_from_top + 2 * self.buttons_gap),
               self.settings_screen)

        while True:
            gameDisplay.blit(START_SCREEN, self.start_screen_rect)
            gameDisplay.blit(GAME_NAME, self.game_name_rect)
            self.show_and_handle_buttons()

    def kill_all_groupB(self):
        for tank in self.manage.tanks_group:
            if tank.team == TEAM_B:
                tank.kill()

    def check_win(self):
        """
        this function check if someone has won or lose - that means its the end of the game
        """
        liveA, liveB = 0, 0
        for tank in self.manage.tanks_group:
            if tank.team == TEAM_A:
                liveA += 1
            else:
                liveB += 1
        if not liveA:
            self.level = 0
            return LOST
        if not liveB:
            if self.mode_dic[self.mode] == self.mode:
                self.level += 1
            return WON
        return KEEP_PLAY

    def game_loop(self):
        """
        the main loop that the game run on
        """
        self.manage.delete_all_sprites()

        game_board = Game_board(self.manage, self.mode, levelargs[self.level])

        backgroung = SCREEN_IMAGE
        backgroung = pygame.transform.scale(backgroung, (B_SIZE_X, B_SIZE_X))
        background_rect = backgroung.get_rect()
        background_rect.topleft = (DATA_WIDTH, 0)

        human_tanks = self.manage.get_human()
        human_player = human_tanks[0]

        # when to exit the game
        game_exit = False
        # wheher its a game over situation
        game_over = False
        # if a fire was made
        fire = False
        # if a missile was launched
        missile_fire = False

        while not game_exit:

            # case its a game over situation
            while game_over == True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            game_over = False
                        if event.type == pygame.QUIT or event.type == pygame.K_RSHIFT:
                            pygame.quit()
                            quit()

            for event in pygame.event.get():
                # press exit
                if event.type == pygame.QUIT:
                    game_exit = True

                # press key
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        human_player.todo[CW] = True
                    if event.key == pygame.K_RIGHT:
                        human_player.todo[ACW] = True
                    if event.key == pygame.K_UP:
                        human_player.todo[FASTER] = True
                    if event.key == pygame.K_DOWN:
                        human_player.todo[SLOWER] = True
                    if event.key == pygame.K_SPACE:
                        fire = True
                    if event.key == pygame.K_m:
                        missile_fire = True
                    if event.key == pygame.K_RSHIFT:
                        game_exit = True
                    if event.key == pygame.K_p:
                        game_over = True
                    if event.key == pygame.K_w:
                        self.kill_all_groupB()
                    # restart
                    if event.key == pygame.K_r:
                        self.game_loop()

                # stop pressing the key
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        human_player.todo[CW] = False
                    elif event.key == pygame.K_RIGHT:
                        human_player.todo[ACW] = False
                    elif event.key == pygame.K_UP:
                        human_player.todo[FASTER] = False
                    elif event.key == pygame.K_DOWN:
                        human_player.todo[SLOWER] = False
                    elif event.key == pygame.K_SPACE:
                        fire = False

            # fill_board()
            gameDisplay.blit(backgroung, background_rect)

            # show object
            game_board.generate_tokens()

            # Game_board.fill_board()
            game_board.show()
            # collides handle
            self.manage.tanks_collide_bullets()
            self.manage.bullets_collide_walls()
            self.manage.missiles_collide_walls()
            self.manage.tanks_collide_tokens()
            self.manage.tank_collide_walls()
            self.manage.tanks_collide_runways()
            self.manage.tanks_collide_missiles()

            # check if someone win or lose
            if len(self.manage.explosions_group.sprites()) == 0:
                win_lose_keepplay = self.check_win()
                if win_lose_keepplay:
                    if win_lose_keepplay == WON:
                        self.manage.win_message = True
                        if self.mode == JOURNEY:
                            self.level += 1
                            self.text_promo()
                        elif self.mode == SIMPLE:
                            self.chose_game_play()
                    else:
                        self.level = 1
                        self.chose_game_play()

            # case a shoot was made
            if fire and human_player.time_load_bullet == human_player.time_of_loading:
                human_player.time_load_bullet = 0
                Bullet(self.manage, human_player)

            # case a missile was used
            if missile_fire:
                Missile(self.manage, human_player)
                missile_fire = False

            # move the tank to the right direction
            human_player.think_then_move()

            # after modify the screen, time to update it
            pygame.display.update()
            # tick some things that work on time
            game_board.tick_the_clock()
            clock.tick(FRAMES_PER_SECOND)

        pygame.display.update()
        pygame.quit()
        quit()


def main():
    Run()


if __name__ == "__main__":
    main()
