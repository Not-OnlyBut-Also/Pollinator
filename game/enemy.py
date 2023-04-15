import pygame
from game import constant, particles
from engine import spritesheet
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, color="yellow", groups=[constant.VISIBLE, constant.ENEMIES]):
        super().__init__(groups)
        self.sprites = constant.FLOWER_SHEET
        self.color = {
            "yellow" : {
                "speed" : 2,
                "frame" : 8
            },
            "red" : {
                "speed" : 3,
                "frame" : 4
            },
            "purple" : {
                "speed" : 5,
                "frame" : 0
            }
        }
        self.animations = {
            "run" : {
                "frames" : [0 + self.color[color]["frame"], 3 + self.color[color]["frame"]],
                "speed" : 6
            }
        }
        self.state = "run"
        self.frame = self.animations[self.state]["frames"][0]
        self.cycle = 0
        self.image = self.sprites[self.frame]
        self.rect = self.image.get_rect(topleft=pos)
        
        if pygame.sprite.spritecollideany(self, constant.ENEMIES) != self or pygame.sprite.spritecollideany(self, constant.PLAYER) != None:
            self.kill()
        
        self.speed = self.color[color]["speed"]
        self.dir = random.choice([-1, 1])
        self.bumped = []
        self.dy = self.rect.y
        self.vel_y = 0
        self.max_vel_y = 30
        self.jump_vel = -30
    def walk(self):
        self.rect.x += self.speed * self.dir
        self.bump()
    def bump(self):
        self.bumped = []
        for enemy in constant.ENEMIES:
            if enemy.rect.colliderect(self.rect) and enemy != self and self not in enemy.bumped:
                self.bumped.append(enemy)
                if self.rect.top > enemy.rect.top:
                    self.vel_y = self.jump_vel
                    self.jump_ended = False
                self.dir = -self.dir
                self.rect.x += self.speed * self.dir
                if self.dir == enemy.dir:
                    enemy.dir = -enemy.dir
        self.wrap()
    def wrap(self):
        wrapped = False
        if self.rect.right <= 0:
            self.rect.right = constant.SCREEN_SIZE[0] + constant.TILE_SIZE - 1
            wrapped = True
        elif self.rect.left >= constant.SCREEN_SIZE[0]:
            self.rect.left = 0 - constant.TILE_SIZE + 1
            wrapped = True
        if wrapped == True and self.rect.topleft[1] >= constant.BOTTOM:
            self.rect.topleft = (self.rect.x, constant.TOP)
            self.dy = self.rect.y
        self.collide()
    def collide(self):
        if self.vel_y < self.max_vel_y:
            self.vel_y += constant.GRAVITY
        self.dy += self.vel_y
        moved_rect = pygame.Rect(self.rect.x, self.dy, constant.TILE_SIZE, constant.TILE_SIZE)
        for sprite in constant.COLLIDABLE:
            if sprite.rect.colliderect(moved_rect):
                if self.vel_y > 0 and self.rect.bottom <= sprite.rect.top:
                    self.rect.bottom = sprite.rect.top
                    self.dy = self.rect.y
                    self.vel_y = 0
        self.rect.y = self.dy
    def update(self):
        spritesheet.animate(self)
        self.walk()
    def pollinate(self):
        Swarm(self.rect.center)
        self.kill()

class Swarm(pygame.sprite.Sprite):
    def __init__(self, pos, groups=[constant.INVISIBLE]):
        super().__init__(groups)
        self.size = 80
        self.image = pygame.Surface((self.size, self.size))
        self.rect = self.image.get_rect(center=pos)
        for i in range(25):
            particles.Pollen(self.rect.center, self)
        self.members = []
        self.shrinking = False
        self.life_lived = 0
    def update(self):
        if len(self.members) == 25:
            self.shrinking = True
        if self.shrinking == True:
            if self.life_lived % 120 == 0:
                self.size -= 10
                self.image = pygame.Surface((self.size, self.size))
                self.rect = self.image.get_rect(center=self.rect.center)
                for member in self.members:
                    if not member.rect.colliderect(self.rect):
                        self.members.remove(member)
                        member.kill()
            if self.size == 0:
                for member in self.members:
                    member.kill()
                self.kill()
            self.life_lived += 1
        