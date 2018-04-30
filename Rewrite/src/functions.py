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

    title = sprites.Title(level_data[0]) if show_title else None
    platform = sprites.Platform()

    for i, row in enumerate(level_data[3]):
        for _i, col in enumerate(row):
            if col in 'ABC':
                color = 255 if col == 'A' else 0 if col == 'B' else 192
                block = sprites.Block((_i * 20, i * 20), color)

            elif col in 'DFH':
                color = 255 if col == 'D' else 0 if col == 'F' else 192
                pit = sprites.Pit((_i * 20, i * 20), color, 'U')

            elif col in 'EGI':
                color = 255 if col == 'E' else 0 if col == 'G' else 192
                pit = sprites.Pit((_i * 20, i * 20), color, 'D')

            elif col in 'KLM':
                color = 255 if col == 'L' else 0 if col == 'K' else 192
                exit = sprites.Exit((_i * 20, i * 20), color)

            elif col in 'NOP':
                color = 255 if col == 'O' else 0 if col == 'N' else 192
                breakable = sprites.Breakable((_i * 20, i * 20), color)

            elif col in 'QRS':
                color = 255 if col == 'R' else 0 if col == 'Q' else 192
                breakable = sprites.Jumpad((_i * 20, i * 20), color)

            elif col == 'J':
                public.spawn = (_i * 20, i * 20)
                public.player = sprites.Ox(public.spawn)

            elif col == '.':
                sphere = sprites.RGBSphere((_i * 20, i * 20), 192)


def clamp(x, low, high):
    return low if x < low else high if x > high else x


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
