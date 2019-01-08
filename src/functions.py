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
        'Flipad': sprites.Flipad,
        'Breakable': sprites.Breakable,
        'RGBSphere': sprites.RGBSphere,
    }

    for sprite in public.all_sprites:
        if sprite.type != 'Cloud':
            sprite.kill()

    level_data = dictionaries.MEDIA['map_' + str(public.level)]

    public.bg_type = level_data.properties['Background']
    public.wrapping = level_data.properties['Wrapping']
    platform = sprites.Platform()

    if show_title:
        title = sprites.Title(level_data.properties['Title'])

    for x in range(40):
        for y in range(24):
            tile = level_data.get_tile_properties(x, y, 0)

            if tile is not None:
                obj = objects[tile['type']](
                    (x * 20, y * 20), tile['Color'], tile['Flipped'])

                if tile['type'] == 'Player':
                    public.player = obj

    for sprite in public.blocks:
        if sprite.type == 'Block':
            sprite.image = block_return(sprite, sprite.color)

        elif sprite.type == 'Pit':
            pit_return(sprite, sprite.color)

        elif sprite.type == 'Breakable':
            sprite.image = breakable_return(sprite, sprite.color)

            if sprite.flipped:
                sprite.image = pygame.transform.flip(sprite.image, 0, 1)


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
    arr = ['Exit', 'Jumpad', 'Flipad', 'RGBSphere']

    if block.type not in arr[0:list_index]:
        return True

    return False


def anim_check(obj):
    prep_anim = 'Idle'

    if obj.accelerating:
        prep_anim = 'Walk'

    if not obj.on_ground:
        if obj.flipped_vertical:
            if obj.vel.y > 0:
                prep_anim = 'Jump'

            elif obj.vel.y < 0:
                prep_anim = 'Fall'

        elif not obj.flipped_vertical:
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
    if color == 0:
        return dictionaries.IMAGES[index]

    elif color == 255:
        return dictionaries.I_IMAGES[index]

    return dictionaries.G_IMAGES[index]


def block_return(obj, color):
    corners = {
        'LEFTUP': 1,
        'RIGHTUP': 1,
        'RIGHTDOWN': 1,
        'LEFTDOWN': 1,
    }
    x = obj.rect.center[0]
    y = obj.rect.center[1]

    LEFT = -11
    UP = -11

    RIGHT = 11
    DOWN = 11

    # LEFTUP
    pos = (x + LEFT, y + UP)

    for sprite in public.all_sprites:
        if sprite.type not in ['Cloud', 'Exit'] and \
                sprite.rect.collidepoint(pos):

            corners['LEFTUP'] = 0
            break

    if pos[0] < 0:
        corners['LEFTUP'] = 0
        corners['LEFTDOWN'] = 0

    if pos[1] > public.SHEIGHT:
        corners['LEFTUP'] = 0
        corners['RIGHTUP'] = 0

    # UP
    pos = (x, y + UP)

    for sprite in public.all_sprites:
        if sprite.type not in ['Cloud', 'Exit'] and \
                sprite.rect.collidepoint(pos):

            corners['LEFTUP'] = 0
            corners['RIGHTUP'] = 0
            break

    if pos[1] > public.SHEIGHT:
        corners['LEFTUP'] = 0
        corners['RIGHTUP'] = 0

    # RIGHTUP
    pos = (x + RIGHT, y + UP)

    for sprite in public.all_sprites:
        if sprite.type not in ['Cloud', 'Exit'] and \
                sprite.rect.collidepoint(pos):

            corners['RIGHTUP'] = 0
            break

    if pos[0] > public.SWIDTH:
        corners['RIGHTUP'] = 0
        corners['RIGHTDOWN'] = 0

    if pos[1] > public.SHEIGHT:
        corners['LEFTUP'] = 0
        corners['RIGHTUP'] = 0

    # RIGHT
    pos = (x + RIGHT, y)

    for sprite in public.all_sprites:
        if sprite.type not in ['Cloud', 'Exit'] and \
                sprite.rect.collidepoint(pos):

            corners['RIGHTUP'] = 0
            corners['RIGHTDOWN'] = 0

            break

    if pos[0] > public.SWIDTH:
        corners['RIGHTUP'] = 0
        corners['RIGHTDOWN'] = 0

    # RIGHTDOWN
    pos = (x + RIGHT, y + DOWN)

    for sprite in public.all_sprites:
        if sprite.type not in ['Cloud', 'Exit'] and \
                sprite.rect.collidepoint(pos):

            corners['RIGHTDOWN'] = 0
            break

    if pos[0] > public.SWIDTH:
        corners['RIGHTUP'] = 0
        corners['RIGHTDOWN'] = 0

    if pos[1] < 0:
        corners['LEFTDOWN'] = 0
        corners['RIGHTDOWN'] = 0

    # DOWN
    pos = (x, y + DOWN)

    for sprite in public.all_sprites:
        if sprite.type not in ['Cloud', 'Exit'] and \
                sprite.rect.collidepoint(pos):

            corners['LEFTDOWN'] = 0
            corners['RIGHTDOWN'] = 0
            break

    if pos[1] < 0:
        corners['LEFTDOWN'] = 0
        corners['RIGHTDOWN'] = 0

    # LEFTDOWN
    pos = (x + LEFT, y + DOWN)

    for sprite in public.all_sprites:
        if sprite.type not in ['Cloud', 'Exit'] and \
                sprite.rect.collidepoint(pos):

            corners['LEFTDOWN'] = 0
            break

    if pos[0] < 0:
        corners['LEFTUP'] = 0
        corners['LEFTDOWN'] = 0

    if pos[1] < 0:
        corners['LEFTDOWN'] = 0
        corners['RIGHTDOWN'] = 0

    # LEFT
    pos = (x + LEFT, y)

    for sprite in public.all_sprites:
        if sprite.type not in ['Cloud', 'Exit'] and \
                sprite.rect.collidepoint(pos):

            corners['LEFTUP'] = 0
            corners['LEFTDOWN'] = 0
            break

    if pos[0] < 0:
        corners['LEFTUP'] = 0
        corners['LEFTDOWN'] = 0

    binary = int(''.join(map(str, corners.values())), 2)

    return image_return(color, 'Block')[binary]


def breakable_return(obj, color):
    sides = {'LEFT': 1, 'RIGHT': 1}

    LEFT = -11
    RIGHT = 11
    x = obj.rect.center[0]
    y = obj.rect.center[1]

    # LEFT

    pos = (x + LEFT, y)

    for sprite in public.all_sprites:
        if sprite.type not in ['Cloud', 'Exit'] and \
                sprite.rect.collidepoint(pos):

            sides['LEFT'] = 0
            break

    if pos[0] < 0:
        sides['LEFT'] = 0

    # RIGHT

    pos = (x + RIGHT, y)

    for sprite in public.all_sprites:
        if sprite.type not in ['Cloud', 'Exit'] and \
                sprite.rect.collidepoint(pos):

            sides['RIGHT'] = 0
            break

    if pos[0] > public.SWIDTH:
        sides['RIGHT'] = 0

    binary = int(''.join(map(str, sides.values())), 2)

    return image_return(color, 'Breakable')[binary]


def pit_return(obj, color):
    sides = {'LEFT': 1, 'RIGHT': 1}

    LEFT = -11
    RIGHT = 11
    x = obj.rect.center[0]
    y = obj.rect.center[1]

    # LEFT

    pos = (x + LEFT, y)

    for sprite in public.all_sprites:
        if sprite.type not in ['Cloud', 'Exit'] and \
                sprite.rect.collidepoint(pos):

            sides['LEFT'] = 0

    if pos[0] < 0:
        sides['LEFT'] = 0

    # RIGHT

    pos = (x + RIGHT, y)

    for sprite in public.all_sprites:
        if sprite.type not in ['Cloud', 'Exit'] and \
                sprite.rect.collidepoint(pos):

            sides['RIGHT'] = 0
            break

    if pos[0] > public.SWIDTH:
        sides['RIGHT'] = 0

    binary = int(''.join(map(str, sides.values())), 2)

    obj.image = image_return(color, 'Pit')[binary]

    if obj.flipped:
        if type(obj.image) is list:
            obj.image = \
                [pygame.transform.flip(image, 0, 1) for image in obj.image]

        elif not type(obj.image) is list:
            obj.image = pygame.transform.flip(obj.image, 0, 1)


def color_return(options, value):
    prep_color = list(options)

    if prep_color[0] == value:
        return 255

    elif prep_color[1] == value:
        return 0

    return 192


def flip_check(obj):
    if not obj.flipped:
        obj.rect.y += 10

    elif obj.flipped:
        if type(obj.image) is list:
            obj.image = \
                [pygame.transform.flip(image, 0, 1) for image in obj.image]

        elif not type(obj.image) is list:
            obj.image = pygame.transform.flip(obj.image, 0, 1)
