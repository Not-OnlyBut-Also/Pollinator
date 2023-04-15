import pygame
from game import constant
from engine import text

class Music_Select:
    def __init__(self, main):
        constant.BUZZ_CHANNEL.set_volume(0)
        self.game = main
        self.screen = main.screen
        self.center = (constant.SCREEN_SIZE[0] / 2, constant.SCREEN_SIZE[1] / 2)
        self.header = text.Text(self.center, "Music Select:", groups=[constant.VISIBLE])
        self.header.shift("up", self.header.font_height + 32)
        self.type_a_button = text.Text(self.center, "Type A", align="right", groups=[constant.VISIBLE])
        self.type_a_button.shift("left", 0)
        self.type_b_button = text.Text(self.center, "Type B", align="left", groups=[constant.VISIBLE])
        self.type_b_button.shift("right", 32)
        self.music_types = {
            "Type A" : {
                "button" : self.type_a_button,
                "music" : constant.FLIGHT_OF_THE_BUMBLEBEE,
                "align" : "right",
                "shift" : "left",
                "amount" : 0
            },
            "Type B" : {
                "button" : self.type_b_button,
                "music" : constant.CSIKOS_POST,
                "align" : "left",
                "shift" : "right",
                "amount" : 32
            }
        }
        self.selected = "Type A"
        self.pressed = False
        self.changed = True
    def choose_music_type(self):
        if self.pressed == False and pygame.key.get_pressed()[pygame.K_LEFT] or self.pressed == False and pygame.key.get_pressed()[pygame.K_RIGHT]:
                constant.SFX_CHANNEL.play(constant.BLIP_SOUND)
                self.pressed = True
                self.changed = True
                self.music_types[self.selected]["button"].kill()
                self.music_types[self.selected]["button"] = text.Text(self.center, self.selected, align=self.music_types[self.selected]["align"], color=0, groups=[constant.VISIBLE])
                self.music_types[self.selected]["button"].shift(self.music_types[self.selected]["shift"], self.music_types[self.selected]["amount"])
                if self.selected == "Type A":
                    self.selected = "Type B"
                else:
                    self.selected = "Type A"
        elif self.pressed == True and not pygame.key.get_pressed()[pygame.K_LEFT] and not pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.pressed = False
        self.music_types[self.selected]["button"].kill()
        self.music_types[self.selected]["button"] = text.Text(self.center, self.selected, align=self.music_types[self.selected]["align"], color=1, groups=[constant.VISIBLE])
        self.music_types[self.selected]["button"].shift(self.music_types[self.selected]["shift"], self.music_types[self.selected]["amount"])
        if self.changed == True:
            self.changed = False
            constant.MUSIC_CHANNEL.play(self.music_types[self.selected]["music"], loops=-1)
    def update(self):
        self.choose_music_type()
        constant.VISIBLE.draw(self.screen)
    def kill(self):
        for sprite in constant.VISIBLE:
            sprite.kill()