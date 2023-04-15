import pygame
from game import constant, particles
from engine import text
import random

class Menu:
    def __init__(self, main):
        self.screen = main.screen
        title_x, title_y = constant.SCREEN_SIZE[0] / 2, constant.SCREEN_SIZE[1] / 2
        self.title = Title((title_x, title_y))
        self.message = text.Text((title_x, title_y + 64),
            "Press Enter to Start // //L for Leaderboard // //C for Credits",
            groups=[constant.VISIBLE])
        self.message_alpha = 0
        self.frame_count = 0
        self.bee_count = random.choice(range(10, 31))
        if len(constant.BEES.sprites()) > 0:
            self.bee_count = 0
        for bee in range(self.bee_count):
            x = random.choice(range(64, constant.SCREEN_SIZE[0] - 64))
            y = random.choice(range(64, constant.SCREEN_SIZE[1] - 64))
            particles.Bee((x, y))
        constant.MUSIC_CHANNEL.stop()
        constant.BUZZ_CHANNEL.unpause()
        constant.BUZZ_CHANNEL.set_volume(0.1)
    def flash_message(self):
        if self.frame_count % (constant.FPS / 2) == 0:
            if self.message_alpha == 255:
                self.message_alpha = 140
            else:
                self.message_alpha = 255
            self.message.set_alpha(self.message_alpha)
        self.frame_count += 1
    def update(self):
        constant.VISIBLE.draw(self.screen)
        constant.BEES.draw(self.screen)
        constant.BEES.update()
        self.flash_message()
    def kill(self):
        self.message.set_alpha(255)
        for sprite in constant.VISIBLE:
            sprite.kill()

class Title(pygame.sprite.Sprite):
    def __init__(self, pos, groups=[constant.VISIBLE]):
        super().__init__(groups)
        self.image = constant.TITLE_IMG
        self.rect = self.image.get_rect(center=pos)