import pygame
from game import constant
from engine import text

class Bar(pygame.sprite.Sprite):
    def __init__(self, pos, groups=[constant.UI]):
        super().__init__(groups)
        self.margin = 16
        self.image = pygame.Surface((constant.SCREEN_SIZE[0], constant.TILE_SIZE + self.margin))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect(topleft=pos)
        self.center_y = pos[1] + (constant.TILE_SIZE + self.margin) / 2
        
        self.time_min = 0
        self.time_sec = 0
        self.time_frame = 0
        self.time_text = "0" + str(self.time_min) + ":" + str(self.time_sec) + "0"
        self.timer_pos = (constant.SCREEN_SIZE[0], self.center_y)
        self.timer = text.Text(self.timer_pos, self.time_text, align="right")
        
        self.bee_count = 0
        self.bee_text = str(self.bee_count) + "   "
        self.bees_counted = []
        self.bee_pos = (constant.SCREEN_SIZE[0] / 2 + self.margin, self.center_y)
        self.bee_display = text.Text(self.bee_pos, "Bees Saved: " + self.bee_text)
        
        self.life_count = 5
        self.life_pos = (self.margin, self.center_y)
        self.life_display = text.Text(self.life_pos, "Lives: " + str(self.life_count), align="left")
    def update_lives(self):
        for player in constant.PLAYER:
            if player.health != self.life_count:
                self.life_count = player.health
                self.life_display.kill()
                self.life_display = text.Text(self.life_pos, "Lives: " + str(self.life_count), align="left")
    def update_bees(self):
        for swarm in constant.INVISIBLE:
            if swarm not in self.bees_counted:
                self.bee_count += 25
                self.bees_counted.append(swarm)
        self.bee_text = str(self.bee_count)
        if 4 - len(str(self.bee_count)) > 0:
            less_than_thousand = 4 - len(str(self.bee_count))
            self.bee_text += less_than_thousand * " "
        self.bee_display.kill()
        self.bee_display = text.Text(self.bee_pos, "Bees Saved: " + self.bee_text)
    def update_timer(self):
        if self.time_frame != 0 and self.time_frame % constant.FPS == 0:
            if self.time_sec < 59:
                self.time_sec += 1
                self.time_frame = 0
            else:
                self.time_min += 1
                self.time_sec = 0
                self.time_frame = 0
            min_text = str(self.time_min)
            sec_text = str(self.time_sec)
            if self.time_min < 10:
                min_text = "0" + min_text
            if self.time_sec < 10:
                sec_text = "0" + sec_text
            self.time_text = min_text + ":" + sec_text
            self.timer.kill()
            self.timer = text.Text(self.timer_pos, self.time_text, align="right")
        self.time_frame += 1
    def update(self):
        if len(constant.PLAYER.sprites()) > 0:
            self.update_timer()
            self.update_lives()
            self.update_bees()
        else:
            self.life_count = 0
            self.life_display.kill()
            self.life_display = text.Text(self.life_pos, "Lives: " + str(self.life_count), align="left")

class Pause_Menu(pygame.sprite.Sprite):
    def __init__(self, board, groups=[constant.VISIBLE, constant.UI]):
        super().__init__(groups)
        self.board = board
        self.image = pygame.Surface(constant.SCREEN_SIZE)
        self.image.fill((0, 0, 0))
        self.image.set_alpha(200)
        self.rect = self.image.get_rect(topleft=(0, 0))
        
        self.esc_held = True
        self.message_group = pygame.sprite.Group()
        self.message = text.Text((constant.SCREEN_SIZE[0] / 2, constant.SCREEN_SIZE[1] / 2),
            "Paused // // Esc to continue // R to restart // M to go to the menu",
            groups=[constant.VISIBLE])
        
        constant.SFX_CHANNEL.play(constant.PAUSE_SOUND)
        
        constant.BUZZ_CHANNEL.pause()
        constant.MUSIC_CHANNEL.pause()
    def update(self):
        if self.esc_held == True and not pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.esc_held = False
        elif self.esc_held == False and pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.board.paused = False
            constant.BUZZ_CHANNEL.unpause()
            constant.MUSIC_CHANNEL.unpause()
            self.message.kill()
            self.kill()