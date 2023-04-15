import pygame
from game import constant
from engine import text

class Credits:
    def __init__(self, main):
        self.screen = main.screen
        self.text = text.Text((constant.SCREEN_SIZE[0] / 2, constant.SCREEN_SIZE[1] / 2),
            "Game created by: Riley Hysell // //Music by: Fez Goat Music // //Thanks for playing // // // //Enter to Return to Menu",
            groups = [constant.VISIBLE])
    def update(self):
        constant.VISIBLE.draw(self.screen)
        constant.BEES.draw(self.screen)
        constant.BEES.update()
    def kill(self):
        for sprite in constant.VISIBLE:
            sprite.kill()