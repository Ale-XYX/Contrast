import os
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
    objects = {
        'Player': sprites.Ox,
        'Block': sprites.Block,
        'Exit': sprites.Exit,
        'Pit': sprites.Pit,
        'Jumpad': sprites.Jumpad,
        'Breakable': sprites.Breakable,
        'RGBSphere': sprites.RGBSphere,
        'Wrapping': sprites.Wrapping,
        'KillBlock': sprites.KillBlock
    }

    for sprite in public.all_sprites:
        if sprite.type != 'Cloud':
            sprite.kill()

    if public.level == 20 and public.music:
        dictionaries.MEDIA['greetings'].stop()
        dictionaries.MEDIA['deathly'].play(-1)

    level_data = dictionaries.MEDIA['map_' + str(public.level)]

    public.bg_type = level_data.properties['Background']
    public.wrapping = level_data.properties['Wrapping']
    [sprites.Block((x * 20, 480), public.GREY, True) for x in range(40)]
    [sprites.Block((x * 20, -20), public.GREY, True) for x in range(40)]

    if show_title:
        title = sprites.Title(level_data.properties['Title'], False)

    for x in range(40):
        for y in range(24):
            tile = level_data.get_tile_properties(x, y, 0)

            if tile is not None:
                obj = objects[tile['type']](
                    (x * 20, y * 20), tile['Color'], tile['Flipped'])

                if tile['type'] == 'Player':
                    public.player = obj

            if x == 0 or x == 39:
                if public.wrapping:
                    obj = objects['Wrapping']((x * 20, y * 20))

    for sprite in public.blocks:
        if sprite.type == 'Block':
            sprite.image = block_return(sprite)

        elif sprite.type in ['Breakable', 'Pit']:
            sprite.image = half_return(sprite)

    if public.wrapping:
        obj = objects['Wrapping']((0, 480))
        obj = objects['Wrapping']((780, 480))


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
    arr = ['Exit', 'Jumpad', 'Flipad', 'RGBSphere', 'KillBlock']

    if block.type == 'Breakable':
        if block.dead or block.recovering:
            return False

        elif not block.dead or not block.recovering:
            return True

    if block.type not in arr[0:list_index]:
        return True

    return False


def anim_check(obj):
    prep_anim = 'Idle'

    if obj.accelerating:
        prep_anim = 'Walk'

    if not obj.on_ground:
        if obj.vel.y < 0:
            prep_anim = 'Jump'

        elif obj.vel.y > 0:
            prep_anim = 'Fall'

    if obj.vel.y > 1 or obj.super_jump:
        prep_anim = 'Fall'

    if obj.died:
        prep_anim = 'Die'

    if obj.won:
        prep_anim = 'Win'

    return prep_anim


def image_return(color, index):
    if color == public.BLACK:
        return dictionaries.IMAGES[index]

    elif color == public.WHITE:
        return dictionaries.I_IMAGES[index]

    return dictionaries.G_IMAGES[index]


def block_return(obj):
    corners = {
        'LeftUp': [
            [(-11, -11), (0, -11), (-11, 0)], 
            ['pos_[1] < 0',
            'pos_[0] < 0'],
            1
            ],

        'RightUp': [
            [(11, -11), (0, -11), (11, 0)],
            ['pos_[1] < 0', 
            'pos_[0] > public.SWIDTH'],
            1,
            ],

        'RightDown': [
            [(11, 11), (0, 11), (11, 0)],
            ['pos_[1] > public.SHEIGHT',
            'pos_[0] > public.SWIDTH'],
            1
            ],

        'LeftDown': [
            [(-11, 11), (0, 11), (-11, 0)],
            ['pos_[1] > public.SHEIGHT',
            'pos_[0] < 0'],
            1
            ],
    }

    x = obj.rect.center[0]
    y = obj.rect.center[1]
    creqs = [obj.color, public.GREY]


    for i, corner in enumerate(corners):
        for pos in corners[corner][0]:
            pos_ = tuple(map(sum, zip((x,y), pos)))

            for block in public.blocks:
                if block.rect.collidepoint(pos_):
                    if obj.color != public.GREY:
                        if block.type not in ['Exit', 'KillBlock'] and block.color in creqs:
                            corners[corner][2] = 0

                    elif obj.color == public.GREY:
                        if block.type not in ['Exit', 'KillBlock']:
                            corners[corner][2] = 0

        # Eval is evil my ass

        for exp in corners[corner][1]:
            if eval(exp):
                corners[corner][2] = 0

    binary = int(''.join([str(corners[corner][2]) for corner in corners]), 2)

    return image_return(obj.color, 'Block')[binary]


def half_return(obj):
    sides = {
        'Left': [
            (-11, 0),
            'pos[0] < 0',
            1
            ],

        'Right': [
            (11, 0),
            'pos[0] > public.SWIDTH',
            1
            ]
    }

    x = obj.rect.center[0]
    y = obj.rect.center[1]
    creqs = [obj.color, public.GREY]

    for i, side in enumerate(sides):
        pos = tuple(map(sum, zip((x,y), sides[side][0])))

        for block in public.blocks:
            if block.rect.collidepoint(pos):
                if obj.color != 192:
                    if block.type != 'Exit' and block.color in creqs:
                        sides[side][2] = 0

                elif obj.color == 192:
                    if block.type != 'Exit':
                        sides[side][2] = 0

        if eval(sides[side][1]):
            sides[side][2] = 0


    binary = int(''.join([str(sides[side][2]) for side in sides]), 2)

    image = image_return(obj.color, obj.type)[binary]

    if obj.flipped:
        if type(obj.image) is list:
            image = \
                [pygame.transform.flip(image, 0, 1) for image in image]

        elif not type(obj.image) is list:
            image = pygame.transform.flip(image, 0, 1)

    return image


def color_return(options, value):
    prep_color = list(options)

    if prep_color[0] == value:
        return public.WHITE

    elif prep_color[1] == value:
        return public.BLACK

    return public.GREY


def flip_check(obj):
    if not obj.flipped:
        obj.rect.y += 10

    elif obj.flipped:
        if type(obj.image) is list:
            obj.image = \
                [pygame.transform.flip(image, 0, 1) for image in obj.image]

        elif not type(obj.image) is list:
            obj.image = pygame.transform.flip(obj.image, 0, 1)

# :^)
