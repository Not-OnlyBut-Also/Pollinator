import pygame
from game import constant
from engine import text

class Instructions:
    def __init__(self, main):
        constant.SFX_CHANNEL.play(constant.SELECT_SOUND)
        self.screen = main.screen
        self.text = text.Text((constant.SCREEN_SIZE[0] / 2, constant.SCREEN_SIZE[1] / 2),
            "Instructions: // //Jump on flowers to spread //pollen and attract bees. // //Don't hit flowers. //You're allergic. // //And don't get stung. //Beware their buzzing.",
            groups=[constant.VISIBLE])
        self.text.shift("up", len(self.text.lines) * self.text.font_height / 2)
    def update(self):
        constant.VISIBLE.draw(self.screen)
    def kill(self):
        for sprite in constant.VISIBLE:
            sprite.kill()