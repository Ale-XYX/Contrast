import os
import re
import sys
import glob
import pytmx
import pygame
import public
import functions

# Media loading system
# Takes all sounds, images, and maps from /res/ and compiles them into an array for further use.
MEDIA = {}
images = glob.glob(os.path.join(os.path.dirname(__file__), 'res', '*.png'))
audio = glob.glob(os.path.join(os.path.dirname(__file__), 'res', '*.ogg'))
maps = glob.glob(os.path.join(os.path.dirname(__file__), 'res', '*.tmx'))

for file in images:
    obj = pygame.image.load(file).convert_alpha()
    MEDIA[os.path.split(file)[-1][:-4]] = obj # Trunicate filename, add to object.

for file in audio:
    obj = pygame.mixer.Sound(file)
    MEDIA[os.path.split(file)[-1][:-4]] = obj

for file in maps:
    obj = pytmx.TiledMap(file)
    MEDIA[os.path.split(file)[-1][:-4]] = obj

    # Finds the number in a map file, then converts it out of the stupid re.Match format
    level_num = int(re.search('map_(.+?).tmx', file).group(1)) 
    if level_num > public.level_max: # If map num is higher than max level, raise max level.
        public.level_max = level_num

    print(public.level_max)

class Spritesheet():
    def __init__(self, surface):
        '''
        Class for managine the spritesheet files in .res
        From pygame.org
        '''
        self.sheet = surface

    def image_at(self, rectangle):
        '''Find images at rect'''
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image.fill((0, 0, 0, 0))
        image.blit(self.sheet, (0, 0), rect)

        return image

    def images_at(self, rects):
        '''Find images at several rects'''
        return [self.image_at(rect) for rect in rects]

    def load_strip(self, rect, image_count):
        '''Load a strip of sprites, all with the same rect'''
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]

        return self.images_at(tups)


ui_ss = Spritesheet(MEDIA['ui_ss'])
decor_ss = Spritesheet(MEDIA['decor_ss'])
player_ss = Spritesheet(MEDIA['player_ss'])
obstacles_ss = Spritesheet(MEDIA['obstacles_ss'])
rgbsphere_ss = Spritesheet(MEDIA['rgbsphere_ss'])

IMAGES = { # Main animation storage system, most anims are loaded in 20x20x4 strips.
    'Idle': player_ss.load_strip([0, 0, 20, 20], 4),

    'Walk': player_ss.load_strip([0, 20, 20, 20], 4),

    'Jump': player_ss.load_strip([0, 40, 20, 20], 4),

    'Fall': player_ss.load_strip([0, 60, 20, 20], 4),

    'Die': player_ss.load_strip([0, 80, 20, 20], 4),

    'Win': player_ss.load_strip([0, 100, 20, 20], 4),

    'Exit': obstacles_ss.load_strip([0, 0, 20, 20], 4),

    'Pit': [# Pit loads several strips due to the decor system.
            obstacles_ss.load_strip([0, 20, 20, 10], 4),
            obstacles_ss.load_strip([0, 30, 20, 10], 4),
            obstacles_ss.load_strip([0, 40, 20, 10], 4),
            obstacles_ss.load_strip([0, 50, 20, 10], 4),
        ],

    'Breakable': obstacles_ss.load_strip([0, 60, 20, 10], 4),

    'Jumpad': obstacles_ss.load_strip([0, 70, 20, 10], 4),

    'RGBSphere': rgbsphere_ss.load_strip([0, 0, 10, 10], 24),

    'Decor': decor_ss.load_strip([0, 80, 20, 20], 4),

    'Buttons': ui_ss.load_strip([200, 0, 50, 55], 3),

    'Logo': ui_ss.image_at([0, 100, 300, 43]),

    # block_ss is 20x20x(4x4), so it adds up 4 strips constructed from each strip in the spritesheet into an array.
    'Block': sum([decor_ss.load_strip([0, i * 20, 20, 20], 4) for i in range(4)], []),
}

# Image post-processing, creates White, Black, Grey variants of all images and anims using functions.ppc()
index = -1
I_IMAGES = {}
G_IMAGES = {}

for key in IMAGES.keys():
    I_IMAGES.update({key: []})
    G_IMAGES.update({key: []})

    if key != 'Logo':
        for image in IMAGES[key]:
            if key == 'Pit': # Special instructions for pit as it has decor, convert all anim instances.
                I_IMAGES['Pit'].append([])
                G_IMAGES['Pit'].append([])
                index += 1

                for element in image:
                    I_IMAGES['Pit'][index].append(
                        functions.ppc(element.copy(), public.WHITE, public.BLACK))

                    G_IMAGES['Pit'][index].append(
                        functions.ppc(element.copy(), public.GREY, public.GREY))

            else: # Otherwise just convert every instance to their respective color.
                I_IMAGES[key].append(functions.ppc(image.copy(), public.WHITE, public.BLACK))
                G_IMAGES[key].append(functions.ppc(image.copy(), public.GREY, public.GREY))

icon_data = [
    b'BZh91AY&SY\xed#\x01l\x00\x05\xb0\xfc\x04\xf8"""""""" ',
    b'@\x00\x00\x00\xb0\x01XP\x0cJ\x0fH\r=\x1aLP\x01\x88',
    b'\xd3M\x1a\x08R\xa3@\x002l\x80\x86\x12\x0e\x90+',
    b'\xc2Ex\xd4\xa6\x82\x88\x12\xa4+\x14\x89* Q\x05',
    b'\x0bI@\xd3@\xd1@4\xd2\x85R\x04B\xc4\x01E\x03MB',
    b'\xb3\xa1p.$"\xef%(\xa9\x90\xa8\xaa\x94B\xef',
    b'\xca\xc5\xe5\xdc&E\x89\t\x00\xbdb\x19\x13\x08',
    b'\x98\xb6\xdc\xd6bn\xfc\x0c\x97]l\xcb\x9d\xd2^P',
    b'\x81\xb2\xa8\x0f\x82\x82\xa8H\x84\xa4\xa0ii\xa8',
    b'\x80\xa0\n\x04\xa1b\x02\x8aD\xa4\x02\xa2T\xa4',
    b'\x10\xc5DfU\xc1\x10\xc9P1T\x03\x01T\x90\x0cA\xc7Yr',
    b'\rd6\x87\xf8\xbb\x92)\xc2\x84\x87i\x18\x0b`'

    # I have no idea why I turned the icon into a string instead of an image file but whatever
]            

MEDIA['icon'] = b''.join(icon_data)

# :^)
