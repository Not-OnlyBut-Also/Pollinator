import pygame
from game import constant
from engine import text, spritesheet
import json

class Score:
    def __init__(self, main):
        constant.MUSIC_CHANNEL.play(constant.SCORE_MUSIC, loops=-1)
        self.screen = main.screen
        self.min = main.scores["min"]
        self.sec = main.scores["sec"]
        self.time_score = (self.min * 60 + self.sec) * 2
        self.bees = main.scores["bees"]
        self.combos = sum([combo * 25 for combo in main.scores["combos"]])
        self.final_score = self.time_score + self.bees + self.combos
        self.title = text.Text((constant.SCREEN_SIZE[0] / 2, 64), "Your Score:", groups=[constant.VISIBLE])
        self.time_label = "Time: "
        self.time_label += " " * (len(str(self.final_score)) - len(str(self.time_score)))
        self.bee_label = "Bees: "
        self.bee_label += " " * (len(str(self.final_score)) - len(str(self.bees)))
        self.combo_label = "Combos: "
        self.combo_label += " " * (len(str(self.final_score)) - len(str(self.combos)))
        self.score = text.Text((constant.SCREEN_SIZE[0] / 2, 64 * 2),
            f"{self.time_label}{self.time_score} // //{self.bee_label}{self.bees} // //{self.combo_label}{self.combos} // // // //Total: {self.final_score}",
            align="right",
            groups=[constant.VISIBLE])
        self.score.shift("right", max(self.score.line_widths) / 2)
        self.line = text.Text((constant.SCREEN_SIZE[0] / 2, 64 * 2 + 20 * 6), "____________________", groups=[constant.VISIBLE])
        self.leaderboard = Leaderboard(main, score=self.final_score,
            pos=(constant.SCREEN_SIZE[0] / 2, self.score.letters[-1].rect.bottom + 64 * 2))
    def update(self):
        constant.VISIBLE.draw(self.screen)
        self.leaderboard.update()
    def kill(self):
        for sprite in constant.VISIBLE:
            sprite.kill()
        self.leaderboard.kill()

class Leaderboard:
    def __init__(self, main, score=None, pos=(constant.SCREEN_SIZE[0] / 2, constant.SCREEN_SIZE[1] / 2)):
        self.pos = pos
        self.score = score
        self.screen = main.screen
        self.save_file = open(constant.SAVE_PATH + "scores.json", "r")
        self.saved_scores = json.load(self.save_file)
        unchanged_scores = self.saved_scores.copy()
        self.slots = list(self.saved_scores.keys())
        self.current_slot = None
        self.current_text = ""
        self.current_display = None
        self.current_color = 1
        self.letter_index = 0
        self.pressed = False
        self.message_index = 0
        self.text = "Leaderboard"
        for slot in self.slots:
            if self.score != None and self.current_slot == None and self.score >= self.saved_scores[slot][1]:
                self.current_slot = slot
                self.message_index = 1
                for slot_to_change in self.slots[int(slot):]:
                    self.saved_scores[slot_to_change] = unchanged_scores[str(int(slot_to_change) - 1)]
                self.saved_scores[slot] = ["~~~", self.score]
                self.score = 0
            dots = "." * (25 - len(str(self.saved_scores[slot][1])))
            if self.current_slot != slot:
                self.text += " // //" + self.saved_scores[slot][0] + dots + str(self.saved_scores[slot][1])
            else:
                self.text += " // //   " + dots + str(self.saved_scores[slot][1])
                self.current_text = "~~~"
        self.save_file.close()
        self.save()
        self.display = text.Text((self.pos[0], self.pos[1]), self.text, groups=[constant.VISIBLE])
        if self.score == None:
            self.display.shift("up", len(self.display.lines) * self.display.font_height / 2)
        self.messages = ["Enter to Return to Menu", "Arrow Keys to Choose Letter //Enter to Select"]
        self.message_pos = (self.pos[0], self.display.letters[-1].rect.bottom + 64)
        self.message = text.Text(self.message_pos, self.messages[self.message_index],
            groups=[constant.VISIBLE])
    def update_letters(self):
        key = [letter for letter in self.display.key if letter not in [":", ".", "_"]]
        if self.current_color == 1 and pygame.key.get_pressed()[pygame.K_UP] and self.pressed == False:
            constant.SFX_CHANNEL.play(constant.BLIP_SOUND)
            self.pressed = True
            try:
                new_letter = key[key.index(self.current_text[self.letter_index]) + 1]
            except IndexError:
                new_letter = key[0]
            self.current_text = self.current_text[:self.letter_index] + new_letter + self.current_text[self.letter_index + 1:]
        elif self.current_color == 1 and pygame.key.get_pressed()[pygame.K_DOWN] and self.pressed == False:
            constant.SFX_CHANNEL.play(constant.BLIP_SOUND)
            self.pressed = True
            try:
                key[key.index(self.current_text[self.letter_index]) - 1]
            except IndexError:
                new_letter = key[-1]
            self.current_text = self.current_text[:self.letter_index] + key[key.index(self.current_text[self.letter_index]) - 1] + self.current_text[self.letter_index + 1:]
        elif pygame.key.get_pressed()[pygame.K_RETURN] and self.pressed == False:
            self.pressed = True
            constant.SFX_CHANNEL.play(constant.SELECT_SOUND)
            if self.letter_index < 2:
                self.letter_index += 1
            elif self.current_color == 1:
                self.current_color = 0
        elif self.pressed == True and not pygame.key.get_pressed()[pygame.K_UP] and not pygame.key.get_pressed()[pygame.K_DOWN] and not pygame.key.get_pressed()[pygame.K_RETURN]:
            self.pressed = False
        if self.current_display != None:
            self.current_display.kill()
        padding = " " * (25 - len(str(self.saved_scores[self.current_slot][1])) + len(str(self.saved_scores[self.current_slot][0])) + 1)
        padded_text = self.current_text + padding
        self.current_display = text.Text((self.pos[0], self.pos[1] + 20 * (2 * int(self.current_slot))),
            padded_text, color=self.current_color, groups=[constant.VISIBLE])
        if self.current_color == 0:
            self.saved_scores[self.current_slot][0] = self.current_text
            self.save()
            self.message_index = 0
            self.message.kill()
            self.message = text.Text(self.message_pos, self.messages[self.message_index],
                groups=[constant.VISIBLE])
            self.current_slot = None
    def update(self):
        if self.score == None:
            constant.VISIBLE.draw(self.screen)
        if self.current_slot != None:
            self.update_letters()
        constant.BEES.draw(self.screen)
        constant.BEES.update()
    def save(self):
        self.save_file = open(constant.SAVE_PATH + "scores.json", "w")
        json.dump(self.saved_scores, self.save_file)
        self.save_file.close()
    def kill(self):
        self.save()
        for sprite in constant.VISIBLE:
            sprite.kill()