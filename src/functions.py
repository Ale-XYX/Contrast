import pygame
import random
import levels
import public
import sprites
import dictionaries


def generate_clouds():
    for i in range(15):
        generated_int = random.randint(0, 1)
        cloud = sprites.Cloud(
            (random.randint(0, public.SWIDTH),
                random.randint(0, public.SHEIGHT)), generated_int)


def update_clouds():
    public.clouds.update()

    if len(public.clouds.sprites()) < 20:
        generated_int = random.randint(0, 1)

        if public.background[0] == 255:
            cloud = sprites.Cloud(
                (-10, random.randint(0, public.SHEIGHT)), generated_int)

        elif public.background[0] == 0:
            cloud = sprites.Cloud(
                (public.SWIDTH + 10, random.randint(0, public.SHEIGHT)), generated_int)


def generate_level():
    public.all_sprites.empty()
    public.title = sprites.Title(levels.LEVELS[public.level][0])
    public.background = levels.LEVELS[public.level][1]
    public.padding = levels.LEVELS[public.level][2]

    for i, l in enumerate(levels.LEVELS[public.level][3]):
        for _i, c in enumerate(l):
            if c == 'A':
                block = sprites.Block(
                    (_i * 20, i * 20), public.WHITE)
            elif c == 'B':
                block = sprites.Block(
                    (_i * 20, i * 20), public.BLACK)

            elif c == 'C':
                block = sprites.Block(
                    (_i * 20, i * 20), public.GREY)

            elif c == 'G':
                public.spawn = (_i * 20, i * 20)


def clamp(x, low, high):
    if x < low:
        return low
    elif x > high:
        return high
    return x
