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


def generate_level(tbool):
    for sprite in public.all_sprites:
        sprite.kill()

    public.breakables = []

    if tbool:
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

            elif c == 'D':
                exit = sprites.Pit((_i * 20, (i * 20) + 10), 0, public.WHITE)

            elif c == 'E':
                exit = sprites.Pit((_i * 20, (i * 20)), 1, public.WHITE)

            elif c == 'F':
                exit = sprites.Pit((_i * 20, (i * 20) + 10), 0, public.BLACK)

            elif c == 'G':
                exit = sprites.Pit((_i * 20, (i * 20)), 1, public.BLACK)

            elif c == 'H':
                exit = sprites.Pit((_i * 20, (i * 20) + 10), 0, public.GREY)

            elif c == 'I':
                exit = sprites.Pit((_i * 20, (i * 20)), 1, public.GREY)

            elif c == 'J':
                public.spawn = (_i * 20, i * 20)

            elif c == 'K':
                exit = sprites.Exit((_i * 20, i * 20), public.BLACK)

            elif c == 'L':
                exit = sprites.Exit((_i * 20, i * 20), public.WHITE)

            elif c == 'M':
                exit = sprites.Exit((_i * 20, i * 20), public.GREY)

            elif c == 'N':
                exit = sprites.BreakableBlock(((_i * 20) + 10, (i * 20) + 5), public.BLACK)

            elif c == 'O':
                exit = sprites.BreakableBlock(((_i * 20) + 10, (i * 20) + 5), public.WHITE)

            elif c == 'P':
                exit = sprites.BreakableBlock(((_i * 20) + 10, (i * 20) + 5), public.GREY)

            elif c == 'Q':
                exit = sprites.JumpPad(((_i * 20), (i * 20) + 10), public.BLACK)

            elif c == 'R':
                exit = sprites.JumpPad(((_i * 20), (i * 20) + 10), public.WHITE)

            elif c == 'S':
                exit = sprites.JumpPad(((_i * 20), (i * 20) + 10), public.GREY)

            elif c == '.':
                sphere = sprites.Sphere(((_i * 20) + 5, (i * 20) + 5), (13, 54, 6))

    
    public.player = sprites.Player(public.spawn, public.all_sprites)
    splitter = sprites.Splitter()


def clamp(x, low, high):
    if x < low:
        return low
    elif x > high:
        return high
    return x
