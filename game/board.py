import pygame
from game import constant, player, enemy, ui
from engine import text
import random
import math

class Board:
    def __init__(self, main):
        constant.BUZZ_CHANNEL.set_volume(0)
        constant.BUZZ_CHANNEL.unpause()
        for sprite in constant.BEES:
            sprite.kill()
        
        self.game = main
        self.screen = main.screen
        self.frames_lost = 0
        self.paused = False
        self.previously_paused = False
        self.spawn_points = []
        self.spawn_timer = 0
        self.difficulty = 250
        self.difficulties = {
            250 : {
                "enemies" : ["yellow"],
                "weights" : [100],
                "spawn rate" : 60
            },
            500 : {
                "enemies" : ["yellow", "red"],
                "weights" : [60, 40],
                "spawn rate" : 60
            },
            750 : {
                "enemies" : ["yellow", "red", "purple"],
                "weights" : [20, 60, 20],
                "spawn rate" : 50
            },
            1000 : {
                "enemies" : ["yellow", "red", "purple"],
                "weights" : [10, 40, 50],
                "spawn rate" : 50
            },
            1250 : {
                "enemies" : ["red", "purple"],
                "weights" : [25, 75],
                "spawn rate" : 40
            },
            1500 : {
                "enemies" : ["purple"],
                "weights" : [100],
                "spawn rate" : 30
            }
        }
        self.difficulty_levels = list(self.difficulties.keys())
        for row_index, row in enumerate(constant.BOARD_DATA):
            for col_index, col in enumerate(row):
                x = col_index * constant.TILE_SIZE
                y = row_index * constant.TILE_SIZE
                if col in [1, 2]:
                    Path((x, y), ID=col)
                elif col == 6:
                    self.UI = ui.Bar((x, y))
                elif col == 8:
                    self.spawn_points.append((x, y))
                elif col == 9:
                    self.player = player.Player((x, y))
    def ramp_up_difficulty(self):
        if self.UI.bee_count > self.difficulty:
            self.difficulty = self.difficulty_levels[self.difficulty_levels.index(self.difficulty) + 1]
            self.spawn_timer = 0
    def spawn_enemies(self):
        self.spawn_timer += 1
        if self.spawn_timer == self.difficulties[self.difficulty]["spawn rate"]:
            spawn_point = random.choice(self.spawn_points)
            enemy.Enemy(spawn_point, color=random.choices(self.difficulties[self.difficulty]["enemies"], weights=self.difficulties[self.difficulty]["weights"])[0])
            self.spawn_timer = 0
    def play_buzzing(self):
        if self.player.in_swarm_timer == 0:
            constant.BUZZ_CHANNEL.set_volume(0)
        for swarm in constant.INVISIBLE:
            if constant.BUZZ_CHANNEL.get_volume() < 0.1:
                constant.BUZZ_CHANNEL.set_volume(constant.BUZZ_CHANNEL.get_volume() + 0.005)
    def pause_menu(self):
        if self.previously_paused == False and pygame.key.get_pressed()[pygame.K_ESCAPE] and self.frames_lost == 0:
            self.paused = True
            self.previously_paused = True
            ui.Pause_Menu(self)
        elif self.previously_paused == True and not pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.previously_paused = False
    def lose(self):
        if self.player.health == 0:
            if self.frames_lost == 0:
                text.Text((constant.SCREEN_SIZE[0] / 2, constant.SCREEN_SIZE[1] / 2), "Game Over")
                constant.MUSIC_CHANNEL.play(constant.GAME_OVER_SOUND)
            self.frames_lost += 1
            if self.frames_lost % (constant.FPS * 4) == 0:
                self.game.scores = {
                    "min" : self.UI.time_min,
                    "sec" : self.UI.time_sec,
                    "bees" : self.UI.bee_count,
                    "combos" : self.player.combos
                }
                self.game.set_state("score")
    def update(self):
        if self.paused == False:
            self.pause_menu()
            self.play_buzzing()
            constant.POLLEN.draw(self.screen)
            constant.POLLEN.update()
            constant.VISIBLE.draw(self.screen)
            constant.VISIBLE.update()
            constant.INVISIBLE.update()
            constant.BEES.draw(self.screen)
            constant.BEES.update()
            constant.UI.draw(self.screen)
            constant.UI.update()
            constant.TEXT.draw(self.screen)
            self.spawn_enemies()
            self.ramp_up_difficulty()
            self.lose()
        else:
            constant.POLLEN.draw(self.screen)
            constant.BEES.draw(self.screen)
            constant.VISIBLE.draw(self.screen)
            constant.UI.update()
    def kill(self):
        for group in constant.GROUPS:
            for sprite in group:
                sprite.kill()

class Path(pygame.sprite.Sprite):
    def __init__(self, pos, groups=[constant.VISIBLE, constant.COLLIDABLE], ID=1):
        super().__init__(groups)
        self.image = constant.PATH_SHEET[ID - 1]
        self.rect = pygame.Rect(*pos, constant.TILE_SIZE, 8)
        
        if ID == 2:
            x = pos[0]
            y = constant.TILE_SIZE * (pos[1] // constant.TILE_SIZE - 1)
            GrassTop((x, y))

class GrassTop(pygame.sprite.Sprite):
    def __init__(self, pos, groups=[constant.VISIBLE]):
        super().__init__(groups)
        self.image = constant.PATH_SHEET[2]
        self.rect = self.image.get_rect(topleft=pos)