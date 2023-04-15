import pygame
from game import constant
from engine import spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups=[constant.VISIBLE, constant.PLAYER]):
        super().__init__(groups)
        self.sprites = constant.PLAYER_SHEET
        self.animations = {
            "idle" : {
                "frames" : [0, 1],
                "speed" : 5
            },
            "run" : {
                "frames" : [2, 5],
                "speed" : 10
            },
            "jump" : {
                "frames" : [6, 6],
                "speed" : 1
            }
        }
        self.state = "idle"
        self.frame = self.animations[self.state]["frames"][0]
        self.cycle = 0
        self.image = self.sprites[self.frame]
        self.rect = self.image.get_rect(topleft=pos)
        
        self.health = 5
        self.inv_frames = 0
        self.speed = 7
        self.dir = 1
        self.dy = self.rect.y
        self.vel_y = 0
        self.max_vel_y = 30
        self.jump_vel = -30
        self.jumped = False
        self.jump_ended = True
        self.burst = False
        self.combo = 0
        self.combos = []
        self.in_swarm_timer = 0
    def run(self):
        if pygame.key.get_pressed()[pygame.K_RIGHT] and not pygame.key.get_pressed()[pygame.K_LEFT]:
            self.dir = 1
            self.rect.x += self.speed * self.dir
            if self.state != "jump":
                self.set_state("run")
        elif pygame.key.get_pressed()[pygame.K_LEFT] and not pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.dir = -1
            self.rect.x += self.speed * self.dir
            if self.state != "jump":
                self.set_state("run")
        elif self.state != "jump":
            self.set_state("idle")
        self.wrap()
    def wrap(self):
        if self.rect.right < 0:
            self.rect.right = constant.SCREEN_SIZE[0] + constant.TILE_SIZE - 1
        elif self.rect.left > constant.SCREEN_SIZE[0]:
            self.rect.left = 0 - constant.TILE_SIZE + 1
    def jump(self):
        if self.vel_y > constant.GRAVITY:
            self.jumped = True
            self.jumped_ended = False
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.jumped == False:
            constant.SFX_CHANNEL.play(constant.JUMP_SOUND)
            self.vel_y += self.jump_vel
            self.jumped = True
            self.jump_ended = False
            self.set_state("jump")
        if not pygame.key.get_pressed()[pygame.K_SPACE] and self.jumped == True and self.jump_ended == False and self.vel_y < 0 and self.burst == False:
            self.vel_y = 0
        elif self.jumped == True and not pygame.key.get_pressed()[pygame.K_SPACE] and self.jump_ended == True:
            self.jumped = False
        if self.vel_y > 0 and self.state != "jump":
            self.set_state("jump")
        if self.vel_y < self.max_vel_y:
            self.vel_y += constant.GRAVITY
        self.burst_flowers()
    def burst_flowers(self):
        moved_rect = pygame.Rect(self.rect.x, self.dy + self.vel_y, constant.TILE_SIZE, constant.TILE_SIZE)
        for enemy in constant.ENEMIES:
            if enemy.rect.colliderect(moved_rect):
                if self.vel_y > 0 and self.rect.bottom <= enemy.rect.top:
                    self.combo += 1
                    self.vel_y = -20
                    self.jumped = True
                    self.jump_ended = False
                    self.set_state("jump")
                    self.burst = True
                    if self.combo % 6 == 0:
                        self.combo = 1
                    if self.combo == 1:
                        constant.SFX_CHANNEL.play(constant.POLLINATE_SOUND)
                    else:
                        constant.SFX_CHANNEL.play(constant.COMBO_SOUND[self.combo - 1])
                    enemy.pollinate()
                elif self.rect.top >= enemy.rect.bottom:
                    enemy.vel_y = -25
                else:
                    enemy.pollinate()
                    if self.burst == False:
                        self.hurt()
        self.get_stung()
    def get_stung(self):
        if pygame.sprite.spritecollideany(self, constant.INVISIBLE) != None:
            if pygame.sprite.spritecollideany(self, constant.INVISIBLE).shrinking == True:
                self.in_swarm_timer += 1
                if constant.BUZZ_CHANNEL.get_volume() < 0.5:
                    constant.BUZZ_CHANNEL.set_volume(constant.BUZZ_CHANNEL.get_volume() + 0.025)
        elif self.in_swarm_timer > 0:
            self.in_swarm_timer -= 0.5
            constant.BUZZ_CHANNEL.set_volume(constant.BUZZ_CHANNEL.get_volume() - 0.01)
        if self.in_swarm_timer >= 20:
            self.in_swarm_timer = 0
            self.hurt()
        self.fall()
    def fall(self):
        if pygame.key.get_pressed()[pygame.K_DOWN] and self.jumped == False and self.rect.topleft[1] < constant.BOTTOM:
            self.rect.y += 1
            self.set_state("jump")
        self.collide()
    def collide(self):
        self.dy += self.vel_y
        moved_rect = pygame.Rect(self.rect.x, self.dy, constant.TILE_SIZE, constant.TILE_SIZE)
        for sprite in constant.COLLIDABLE:
            if sprite.rect.colliderect(moved_rect):
                if self.vel_y > 0 and self.rect.bottom <= sprite.rect.top:
                    self.rect.bottom = sprite.rect.top
                    self.dy = self.rect.y
                    self.vel_y = 0
                    self.jump_ended = True
                    self.burst = False
                    if self.state == "jump":
                        self.set_state("idle")
                    
                    if self.combo > 1:
                        self.combos.append(self.combo)
                    self.combo = 0
        self.rect.y = self.dy
        self.invincible()
    def invincible(self):
        if self.inv_frames > 0:
            if self.inv_frames % 5 == 0:
                if self.sprites == constant.PLAYER_SHEET:
                    self.sprites = constant.HURT_SHEET
                else:
                    self.sprites = constant.PLAYER_SHEET
            self.inv_frames -= 1
        elif self.sprites != constant.PLAYER_SHEET:
            self.sprites = constant.PLAYER_SHEET
    def update(self):
        spritesheet.animate(self)
        self.run()
        self.jump()
        if self.health == 0:
            constant.BUZZ_CHANNEL.set_volume(0)
            self.kill()
    def set_state(self, state):
        if self.state != state:
            self.state = state
            self.frame = self.animations[self.state]["frames"][0]
            self.cycle = 0
    def hurt(self):
        if self.inv_frames == 0:
            constant.SFX_CHANNEL.play(constant.HIT_SOUND)
            self.health -= 1
            self.inv_frames = 60