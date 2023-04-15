import pygame
from game import constant

def interpret(full_sheet, width=constant.TILE_SIZE, height=constant.TILE_SIZE):
    sprite_width, sprite_height = full_sheet.get_width()//width, full_sheet.get_height()//height
    sprites = []
    for y in range(sprite_height):
        for x in range(sprite_width):
            sprites.append(full_sheet.subsurface((x * width, y * height, width, height)))
    return sprites

def animate(sprite):
    if sprite.cycle % (constant.FPS // sprite.animations[sprite.state]["speed"]) == 0:
        if sprite.frame > sprite.animations[sprite.state]["frames"][1]:
            sprite.frame = sprite.animations[sprite.state]["frames"][0]
        sprite.image = sprite.sprites[sprite.frame]
        if sprite.dir == -1:
            sprite.image = pygame.transform.flip(sprite.image, True, False)
        sprite.frame += 1
    sprite.cycle += 1