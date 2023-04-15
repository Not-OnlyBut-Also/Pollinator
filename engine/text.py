import pygame
from game import constant
import string

class Text:
    def __init__(self, pos, text, align="center", color=0, groups=[constant.TEXT]):
        self.text = text
        self.font = constant.FONT_SHEET
        self.font_width = self.font[0].get_width()
        self.font_height = self.font[0].get_height()
        self.letters = []
        self.key = list(string.ascii_uppercase) + [str(num) for num in range(10)] + [":", ".", "_", "~"]
        self.lines = self.text.split(" //")
        self.line_widths = []
        self.letters = []
        
        for num in range(len(self.lines)):
            self.line_widths.append(len(self.lines[num]) * self.font_width)
            if align == "left":
                x = pos[0]
            elif align == "right":
                x = pos[0] - self.line_widths[num]
                self.right = x
            else:
                x = pos[0] - (self.line_widths[num] / 2) + self.font_width
            y = pos[1] + self.font_height * num
            for letter in self.lines[num]:
                cap_letter = letter.capitalize()
                if cap_letter in self.key:
                    self.letters.append(Letter((x, y), self.font[self.key.index(cap_letter) + (len(self.key) + 2) * color], align, groups))
                    x += self.font_width
                elif cap_letter == " ":
                    x += self.font_width
    def set_alpha(self, alpha):
        for letter in self.letters:
            letter.image.set_alpha(alpha)
    def shift(self, direction, amount):
        hori_directions = { "up" : 0, "down" : 0, "left" : -1, "right" : 1 }
        vert_directions = { "up" : -1, "down" : 1, "left" : 0, "right" : 0 }
        x = amount * hori_directions[direction]
        y = amount * vert_directions[direction]
        for letter in self.letters:
            letter.rect.x += x
            letter.rect.y += y
    def kill(self):
        for letter in self.letters:
            letter.kill()

class Letter(pygame.sprite.Sprite):
    def __init__(self, pos, letter_img, align, groups):
        super().__init__(groups)
        self.image = letter_img
        self.rect = self.image.get_rect(center=pos)
        if align == "left":
            self.rect.left = pos[0]
        elif align == "right":
            self.rect.right = pos[0]