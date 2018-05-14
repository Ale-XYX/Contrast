import pygame
import random
import public
import sprites
import dictionaries


def generate_clouds():
    for i in range(15):
        generated_int = random.randint(0, 1)
        cloud = sprites.Cloud(
            (random.randint(0, public.SWIDTH),
                random.randint(0, public.SHEIGHT)), generated_int)


def generate_level(show_title):
    for sprite in public.all_sprites:
        if sprite.type != 'Cloud':
            sprite.kill()

    level_data = dictionaries.LEVELS[public.level]
    public.bg_type = level_data[1]
    public.wrapping = level_data[2]

    platform = sprites.Platform()

    if show_title:
        title = sprites.Title(level_data[0])

    for i, row in enumerate(level_data[3]):
        for _i, col in enumerate(row):
            if col in 'ABC':
                color = color_return('ABC', col)
                block = sprites.Block((_i * 20, i * 20), color)

            elif col in 'DFH':
                color = color_return('DFH', col)
                pit = sprites.Pit((_i * 20, i * 20), color, 'U')

            elif col in 'EGI':
                color = color_return('EGI', col)
                pit = sprites.Pit((_i * 20, i * 20), color, 'D')

            elif col in 'KLM':
                color = color_return('KLM', col)
                exit = sprites.Exit((_i * 20, i * 20), color)

            elif col in 'NOP':
                color = color_return('NOP', col)
                breakable = sprites.Breakable((_i * 20, i * 20), color)

            elif col in 'QRS':
                color = color_return('QRS', col)
                breakable = sprites.Jumpad((_i * 20, i * 20), color)

            elif col == 'J':
                public.spawn = (_i * 20, i * 20)
                public.player = sprites.Ox(public.spawn)

            elif col == '.':
                sphere = sprites.RGBSphere((_i * 20, i * 20), 192)


def clamp(x, low, high):
    if x < low:
        return low

    elif x > high:
        return high

    else:
        return x


def center(surface):
    return ((
        public.SWIDTH / 2) - surface.get_width() // 2, (
        public.SHEIGHT / 2) - surface.get_height() // 2)


def ppc(surface, color_black, color_white):
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            r, g, b, a = surface.get_at((x, y))

            if (r, g, b) == (0, 0, 0):
                r, g, b = [color_black] * 3

            elif (r, g, b) == (255, 255, 255):
                r, g, b = [color_white] * 3

            surface.set_at((x, y), (r, g, b, a))

    return surface


def block_check(block, list_index):
    arr = ['Exit', 'Jumpad', 'RGBSphere']

    if block.type not in arr[0:list_index]:
        return True

    return False


def anim_check(obj):
    to_return = 0

    if obj.accelerating:
        to_return = 1

    if not obj.on_ground:
        if obj.vel.y < 0:
            to_return = 2

        elif obj.vel.y > 0:
            to_return = 3

    if obj.vel.y > 1 or obj.super_jump:
        to_return = 3

    if obj.died:
        to_return = 4

    if obj.won:
        to_return = 5

    return to_return


def image_return(color, index):
    if color == 0:
        return dictionaries.ANIMS[index]

    elif color == 255:
        return dictionaries.I_ANIMS[index]

    return dictionaries.G_ANIMS[index]


def block_return(obj, color):
    # Corners are ordered as LEFTUP, RIGHTUP, RIGHTDOWN, LEFTDOWN
    corners = [0, 0, 0, 0]
    x = obj.rect.center[0]
    y = obj.rect.center[1]

    # LEFTUP
    pos = (x - 20, y - 20)

    for sprite in public.all_sprites:
        if sprite.type != 'Cloud' and sprite.rect.collidepoint(pos):
            corners[0] = 1
            break

    # UP
    pos = (x, y - 20)

    for sprite in public.all_sprites:
        if sprite.type != 'Cloud' and sprite.rect.collidepoint(pos):
            corners[0], corners[1] = 1, 1
            break

    # RIGHTUP
    pos = (x + 20, y - 20)

    for sprite in public.all_sprites:
        if sprite.type != 'Cloud' and sprite.rect.collidepoint(pos):
            corners[1] = 1
            break

    # RIGHT
    pos = (x + 20, y)

    for sprite in public.all_sprites:
        if sprite.type != 'Cloud' and sprite.rect.collidepoint(pos):
            corners[1], corners[2] = 1, 1
            break

    # DOWNRIGHT
    pos = (x + 20, y + 20)

    for sprite in public.all_sprites:
        if sprite.type == 'Block' and sprite.rect.collidepoint(pos):
            corners[2] = 1
            break

    # DOWN
    pos = (x, y + 20)

    for sprite in public.all_sprites:
        if sprite.type != 'Cloud' and sprite.rect.collidepoint(pos):
            corners[2], corners[3] = 1, 1
            break

    # DOWNLEFT
    pos = (x - 20, y + 20)

    for sprite in public.all_sprites:
        if sprite.type != 'Cloud' and sprite.rect.collidepoint(pos):
            corners[3] = 1
            break

    # LEFT
    pos = (x - 20, y)

    for sprite in public.all_sprites:
        if sprite.type != 'Cloud' and sprite.rect.collidepoint(pos):
            corners[3], corners[0] = 1, 1
            break

    binary = int(''.join(map(str, corners)), 2)
    
    if color == 0:
        return dictionaries.ANIMS[10][binary]

    elif color == 255:
        return dictionaries.I_ANIMS[10][binary]

    else:
        return dictionaries.G_ANIMS[10][binary]

def color_return(options, value):
    to_return = list(options)

    if to_return[0] == value:
        return 255

    elif to_return[1] == value:
        return 0

    return 192
