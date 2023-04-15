import pygame
from game import constant
import random
import math

class Pollen(pygame.sprite.Sprite):
    def __init__(self, pos, swarm, groups=[constant.POLLEN]):
        super().__init__(groups)
        self.sprites = constant.PARTICLE_SHEET
        self.image = self.sprites[0]
        self.rect = self.image.get_rect(center=pos)
        self.speed = random.choice(range(1, 11))
        self.angle = random.choice(range(-181, 0))
        self.move_x = self.speed * math.cos(math.radians(self.angle))
        self.move_y = self.speed * math.sin(math.radians(self.angle))
        self.lifetime_spread = random.choice(range(5, 11))
        self.lifetime_attract_bees = self.lifetime_spread + random.choice(range(20, 51))
        self.lifetime = self.lifetime_spread + self.lifetime_attract_bees + random.choice(range(5, 21))
        self.life_lived = 0
        self.swarm = swarm
    def update(self):
        if self.life_lived < self.lifetime_spread:
            self.rect.x += self.move_x
            self.rect.y += self.move_y
            self.move_y += 1.25
        elif self.life_lived == self.lifetime_attract_bees:
           self.swarm.members.append(Bee((self.rect.x, self.rect.y)))
        elif self.life_lived >= self.lifetime:
            self.kill()
        else:
            self.image = self.sprites[1]
        self.life_lived += 1

class Bee(pygame.sprite.Sprite):
    def __init__(self, pos, groups=[constant.BEES]):
        super().__init__(groups)
        self.pos = pos
        self.image = constant.PARTICLE_SHEET[2]
        self.rect = self.image.get_rect(center=pos)
        self.radius = random.choice(range(2, 11))
        self.dir = random.choice([-1, 1])
        self.angle = random.choice(range(361))
    def update(self):
        self.rect.x = self.pos[0] + math.cos(self.angle) * self.radius
        self.rect.y = self.pos[1] + math.sin(self.angle) * self.radius
        self.angle += 0.5 * self.dir