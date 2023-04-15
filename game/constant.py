import os

TITLE = "POLLINATOR"
SCREEN_SIZE = (768, 768)
BG = "#000000"
FPS = 30
TILE_SIZE = 32
TOP = TILE_SIZE * 6
BOTTOM = SCREEN_SIZE[1] - TILE_SIZE * 2
GRAVITY = 3

BOARD_DATA = [
[6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0],
[1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0],
[1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0],
[1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
]

SAVE_PATH = "saves/"
IMG_PATH = "sprites/"
SOUND_PATH = "sounds/"
SOUND_EXT = ".ogg"
def init():
    import pygame
    global GROUPS, VISIBLE, INVISIBLE, UI, TEXT, COLLIDABLE, PLAYER, ENEMIES, POLLEN, BEES
    VISIBLE = pygame.sprite.Group()
    INVISIBLE = pygame.sprite.Group()
    UI = pygame.sprite.Group()
    TEXT = pygame.sprite.Group()
    COLLIDABLE = pygame.sprite.Group()
    PLAYER = pygame.sprite.Group()
    ENEMIES = pygame.sprite.Group()
    POLLEN = pygame.sprite.Group()
    BEES = pygame.sprite.Group()
    
    GROUPS = [VISIBLE, INVISIBLE, UI, TEXT, COLLIDABLE, PLAYER, ENEMIES, POLLEN, BEES]
    
    from engine import spritesheet
    global TITLE_IMG, PLAYER_SHEET, HURT_SHEET, PATH_SHEET, FLOWER_SHEET, PARTICLE_SHEET, FONT_SHEET
    TITLE_IMG = pygame.image.load(IMG_PATH + "title.png").convert_alpha()
    PLAYER_SHEET = spritesheet.interpret(pygame.image.load(IMG_PATH + "player.png").convert_alpha())
    HURT_SHEET = spritesheet.interpret(pygame.image.load(IMG_PATH + "hurt.png").convert_alpha())
    PATH_SHEET = spritesheet.interpret(pygame.image.load(IMG_PATH + "path.png").convert_alpha())
    FLOWER_SHEET = spritesheet.interpret(pygame.image.load(IMG_PATH + "flower.png").convert_alpha())
    PARTICLE_SHEET = spritesheet.interpret(pygame.image.load(IMG_PATH + "particles.png").convert_alpha(), width=4, height=4)
    FONT_SHEET = spritesheet.interpret(pygame.image.load(IMG_PATH + "font.png").convert_alpha(), width=20, height=20) + spritesheet.interpret(pygame.image.load(IMG_PATH + "font_orange.png").convert_alpha(), width=20, height=20)
    
    global JUMP_SOUND, HIT_SOUND, POLLINATE_SOUND, COMBO_SOUND, BUZZ_SOUND, GAME_OVER_SOUND, PAUSE_SOUND, BLIP_SOUND, SELECT_SOUND, FLIGHT_OF_THE_BUMBLEBEE, CSIKOS_POST, SCORE_MUSIC
    JUMP_SOUND = pygame.mixer.Sound(SOUND_PATH + "jump" + SOUND_EXT)
    HIT_SOUND = pygame.mixer.Sound(SOUND_PATH + "hit" + SOUND_EXT)
    POLLINATE_SOUND = pygame.mixer.Sound(SOUND_PATH + "pollinate" + SOUND_EXT)
    COMBO_SOUND = [pygame.mixer.Sound(SOUND_PATH + f"combo{num + 1}" + SOUND_EXT) for num in range(5)]
    BUZZ_SOUND = pygame.mixer.Sound(SOUND_PATH + "buzz" + SOUND_EXT)
    GAME_OVER_SOUND = pygame.mixer.Sound(SOUND_PATH + "pollinate" + SOUND_EXT)
    PAUSE_SOUND = pygame.mixer.Sound(SOUND_PATH + "pause" + SOUND_EXT)
    BLIP_SOUND = pygame.mixer.Sound(SOUND_PATH + "blip" + SOUND_EXT)
    SELECT_SOUND = pygame.mixer.Sound(SOUND_PATH + "select" + SOUND_EXT)
    FLIGHT_OF_THE_BUMBLEBEE = pygame.mixer.Sound(SOUND_PATH + "flight_of_the_bumblebee" + SOUND_EXT)
    CSIKOS_POST = pygame.mixer.Sound(SOUND_PATH + "csikos_post" + SOUND_EXT)
    SCORE_MUSIC = pygame.mixer.Sound(SOUND_PATH + "score_song" + SOUND_EXT)
    
    
    global SFX_CHANNEL, BUZZ_CHANNEL, MUSIC_CHANNEL
    SFX_CHANNEL = pygame.mixer.Channel(0)
    SFX_CHANNEL.set_volume(0.5)
    
    BUZZ_CHANNEL = pygame.mixer.Channel(1)
    BUZZ_CHANNEL.play(BUZZ_SOUND, loops=-1)
    BUZZ_CHANNEL.set_volume(0)
    
    MUSIC_CHANNEL = pygame.mixer.Channel(2)
    MUSIC_CHANNEL.set_volume(0.25)