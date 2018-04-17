import pygame
import levels
import public
import sprites
import dictionaries


def generate_level():
    public.all_sprites.empty()

    for i, l in enumerate(levels.LEVELS[public.level]['Top']):
        for _i, c in enumerate(l):
            if c == 'P':
                player = sprites.Player(
                    ((_i * 20), (i * 20)), public.all_sprites)

    for i, l in enumerate(levels.LEVELS[public.level]['Bottom']):
        for _i, c in enumerate(l):
            if c == 'P':
                player = sprites.Player(
                    ((_i * 20), (i * 20) + 264), public.all_sprites)


def clamp(x, low, high):
    if   x < low:
        return low
    elif x > high:
        return high
    return x
