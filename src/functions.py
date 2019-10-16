import os
import pygame
import random
import public
import sprites
import dictionaries


def generate_clouds():
    '''
    - Draws 15 clouds when the game() function begins
    - The amount of small/large clouds, and the positions, are completely random.
    '''

    for i in range(15):
        size_seed = random.randint(0, 1)
        pos_seed = (random.randint(0, public.SWIDTH), 
            random.randint(0, public.SHEIGHT))
        sprites.Cloud(pos_seed, size_seed)


def generate_level(show_title):
    '''
    Main level generation engine.

    - Reads level respective tmx
    - Generates blocks from data
    - Sets up other level data and starts block decor.
    '''

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

    for sprite in public.all_sprites: # Clear prev. level
        if sprite.type != 'Cloud':
            sprite.kill()

    if public.level == 20 and public.music: # End level music switch
        dictionaries.MEDIA['greetings'].stop()
        dictionaries.MEDIA['deathly'].play(-1)

    level_data = dictionaries.MEDIA['map_' + str(public.level)] # Read new .tmx file

    # Fill out level data, background type, wrapping status, top/bottom blockrows.
    public.bg_type = level_data.properties['Background']
    public.init_bg_type = level_data.properties['Background']
    public.wrapping = level_data.properties['Wrapping']
    [sprites.Block((x * 20, 480), public.GREY, True) for x in range(40)]
    [sprites.Block((x * 20, -20), public.GREY, True) for x in range(40)]

    if show_title: # Title show
        scramble_name = False

        if level_data.properties['Title'] == '?':
            scramble_name = True # Scramble title name as added effect for easter egg level

        title = sprites.Title(level_data.properties['Title'], scramble_name)

    # Main level creation
    # All levels are 40x24, and all objects must be part of the tmx file's spritesheet.
    for x in range(40):
        for y in range(24):
            tile = level_data.get_tile_properties(x, y, 0) # Find tile for specific position/layer.

            # Check if tile exists
            # If true, then take tile type and spawn sprite in exact location as tile, along with tiles color and flipped status
            if tile is not None:
                obj = objects[tile['type']](
                    (x * 20, y * 20), tile['Color'], tile['Flipped'])

                if tile['type'] == 'Player':
                    public.player = obj
                    public.flip_status = tile['Flipped']

            if x == 0 or x == 39: # If X at certain position, and if wrapping is true, then spawn gradient tiles
                if public.wrapping:
                    obj = objects['Wrapping']((x * 20, y * 20))

    if public.level == 0:
        generate_easter_egg()

    # Start block decor post-generation, as all blocks need to be generated for proper decor results.
    # If sprite is block or half-blocks [breakable, pit], then start respective decor creation code.
    for sprite in public.blocks:
        if sprite.type == 'Block':
            sprite.image = block_return(sprite)

        elif sprite.type in ['Breakable', 'Pit']:
            sprite.image = half_return(sprite)

    if public.wrapping: # IDK why this is here but it breaks the game if I remove it so
        obj = objects['Wrapping']((0, 480))
        obj = objects['Wrapping']((780, 480))


def level_regen():
    ''' I was going to improve legel regeneration but then I decided to drop the project'''
    positions = dict()

    for sprite in public.regenables:
        positions[sprite.type] = sprite.init_pos
        sprite.kill()

    for key in positions.keys():
        if key == 'Player':
            public.player = sprites.Ox(positions[key], 0, public.flip_status)
            print(public.flip_status)

    if public.init_bg_type != public.bg_type:
        public.bg_type = public.init_bg_type


def generate_easter_egg():
    dictionaries.MEDIA['greetings'].stop()

    if random.randint(0, 1):
        public.player = sprites.Ox((20 * 3, 20 * 15), public.GREY, False)

    else:
        public.player = sprites.Ox((20 * 36, 20 * 15), public.GREY, True) 

    for sprite in public.all_sprites:
        if sprite.type == 'Block':
            if sprite.color == public.GREY:
                sprite.kill()

        elif sprite.type == 'Player':
            sprite.velocities = dict(right=[0.03, 0], left=[-0.03, 1])

        elif sprite.type == 'Cloud':
            sprite.skip_pos = (sprite.pos.x, sprite.pos.y)


def clamp(x, low, high):
    '''
    Acceleration clamping function, prevents runaway speeding caused by *something*, not sure it just works.

    I forgot who made this function for me, but I thank them :)
    '''
    if x < low:
        return low

    elif x > high:
        return high

    else:
        return x


def center(surface):
    '''Gives a centerred position based on sprite size, its about what you expect.'''
    return ((
        public.SWIDTH / 2) - surface.get_width() // 2, (
        public.SHEIGHT / 2) - surface.get_height() // 2)


def ppc(surface, color_black, color_white):
    '''
    Per pixel conversion
    - Takes an image
    - Flips black pixels and white pixels to the specified color
    - Used to lower the amount of sprites needed, all calculation done pre-load

    Thank you Illume from the pygame discord for creating this function, was having trouble with this before.
    '''

    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            r, g, b, a = surface.get_at((x, y))

            if (r, g, b) == (0, 0, 0): # If pixel is black, change to new color specified
                r, g, b = [color_black] * 3

            elif (r, g, b) == (255, 255, 255): # If pixel is white, change to new color specified.
                r, g, b = [color_white] * 3

            surface.set_at((x, y), (r, g, b, a))

    return surface


def block_check(block, list_index):
    '''
    Checks block type and returns yes-collision or no-collision
    '''
    arr = ['Exit', 'Jumpad', 'Flipad', 'KillBlock', 'RGBSphere']

    # Specific breakable conditions
    # Dont return collission if the block has fully fallen or is respawning.
    if block.type == 'Breakable': 
        if block.dead or block.recovering:
            return False

        elif not block.dead or not block.recovering:
            return True

    # If its not in the array [Therefore a collidable] return yes-collision
    if block.type not in arr[0:list_index]:
        return True

    return False # Return no-collission otherwise.


def anim_check(obj):
    '''
    Series of IF's for which player anim to be specifically using
    All variables are descriptive so no need to comment this code
    '''

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
    '''Returns Black/White/Grey images based on color.'''
    if color == public.BLACK:
        return dictionaries.IMAGES[index]

    elif color == public.WHITE:
        return dictionaries.I_IMAGES[index]

    return dictionaries.G_IMAGES[index]


def block_return(obj):
    '''
    The main block decor engine, takes a blocks position and does calculations to return a specific
    decorred image. Very poorly designed, but I couldn't find a better way to do this.

    half_return() is the same too, but with some stuff lobbed off since its for pits/breakables.
    '''

    corners = { # Hardcoded storage for the checks block corners do, since there are too many to fit into IF's
        'LeftUp': [
            [(-11, -11), (0, -11), (-11, 0)], # Position values block looks
            ['pos_[1] < 0', # Edge Calculations, if either are true then block is flagged as no-corner
            'pos_[0] < 0'], # ^
            1 # Status of block corner
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
    creqs = [obj.color, public.GREY] # Color requirements, must be same color or grey to preserve seperate worlds.


    for i, corner in enumerate(corners):
        for pos in corners[corner][0]:
            pos_ = tuple(map(sum, zip((x,y), pos))) # Very nested code for basically adding the change tuple to the current pos of block

            for block in public.blocks:
                if block.rect.collidepoint(pos_):
                    if obj.color != public.GREY:
                        if block.type not in ['Exit', 'KillBlock'] and (block.color in creqs or public.level == 0):
                            corners[corner][2] = 0 # If its not an exit/a killblock, and its the same color, mark it as no-corner

                    elif obj.color == public.GREY:
                        if block.type not in ['Exit', 'KillBlock']:
                            corners[corner][2] = 0

        # Eval is evil my ass

        for exp in corners[corner][1]:
            if eval(exp):
                corners[corner][2] = 0 # If edge case true, mark as no-corner

    binary = int(''.join([str(corners[corner][2]) for corner in corners]), 2) # Consolidate all Corner and no-corners into a binary number
    
    return image_return(obj.color, 'Block')[binary] # Use decrypted binary number to index spritesheet array. Why in the fuck did I design it like this.


def half_return(obj):
    ''' Returns half decor, see block_return()'''
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


def flip_check(obj):
    '''
    Slightly deprecated for other objects. 
    If the object is flipped, push up, and also modify the animations
    '''
    if not obj.flipped:
        obj.rect.y += 10

    elif obj.flipped:
        if type(obj.image) is list:
            obj.image = \
                [pygame.transform.flip(image, 0, 1) for image in obj.image]

        elif not type(obj.image) is list:
            obj.image = pygame.transform.flip(obj.image, 0, 1)

# :^)
