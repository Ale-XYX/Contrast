import os
import sys
import glob
import pygame
import public
import functions

MEDIA = {}
images = glob.glob(os.path.join(os.path.dirname(__file__), 'res', '*.png'))
audio = glob.glob(os.path.join(os.path.dirname(__file__), 'res', '*.ogg'))

for file in images:
    obj = pygame.image.load(file).convert_alpha()
    MEDIA[os.path.split(file)[-1][:-4]] = obj

for file in audio:
    obj = pygame.mixer.Sound(file)
    MEDIA[os.path.split(file)[-1][:-4]] = obj


class Spritesheet():
    def __init__(self, surface):
        self.sheet = surface

    def image_at(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image.fill((0, 0, 0, 0))
        image.blit(self.sheet, (0, 0), rect)

        return image

    def images_at(self, rects):
        return [self.image_at(rect) for rect in rects]

    def load_strip(self, rect, image_count):
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]

        return self.images_at(tups)


block_ss = Spritesheet(MEDIA['block_ss'])
player_ss = Spritesheet(MEDIA['player_ss'])
obstacles_ss = Spritesheet(MEDIA['obstacles_ss'])
rgbsphere_ss = Spritesheet(MEDIA['rgbsphere_ss'])

IMAGES = {
    'Idle': player_ss.load_strip([0, 0, 20, 20], 4),

    'Walk': player_ss.load_strip([0, 20, 20, 20], 4),

    'Jump': player_ss.load_strip([0, 40, 20, 20], 4),

    'Fall': player_ss.load_strip([0, 60, 20, 20], 4),

    'Die': player_ss.load_strip([0, 80, 20, 20], 4),

    'Win': player_ss.load_strip([0, 100, 20, 20], 4),

    'Exit': obstacles_ss.load_strip([0, 0, 20, 20], 4),

    'Pit': [
            obstacles_ss.load_strip([0, 20, 20, 10], 4),
            obstacles_ss.load_strip([0, 30, 20, 10], 4),
            obstacles_ss.load_strip([0, 40, 20, 10], 4),
            obstacles_ss.load_strip([0, 50, 20, 10], 4),
        ],

    'Breakable': obstacles_ss.load_strip([0, 60, 20, 10], 4),

    'Jumpad': obstacles_ss.load_strip([0, 70, 20, 10], 4),

    'Flipad': obstacles_ss.load_strip([0, 80, 20, 10], 4),

    'RGBSphere': rgbsphere_ss.load_strip([0, 0, 10, 10], 24),

    'Block': sum([block_ss.load_strip([0, i * 20, 20, 20], 4) for i in range(4)], [])
}

index = -1
I_IMAGES = {}
G_IMAGES = {}

for key in IMAGES.keys():
    I_IMAGES.update({key: []})
    G_IMAGES.update({key: []})

    for image in IMAGES[key]:
        if key == 'Pit':
            I_IMAGES['Pit'].append([])
            G_IMAGES['Pit'].append([])
            index += 1

            for element in image:
                I_IMAGES['Pit'][index].append(
                    functions.ppc(element.copy(), 255, 0))

                G_IMAGES['Pit'][index].append(
                    functions.ppc(element.copy(), 192, 192))

        else:
            I_IMAGES[key].append(functions.ppc(image.copy(), 255, 0))
            G_IMAGES[key].append(functions.ppc(image.copy(), 192, 192))

LEVELS = {
    -1: ['Testing', 0, True, [
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '            AAAA                        ',
        '               4                        ',
        '                                        ',
        '   >       1                              '
    ]],

    0: ['Congrats, You found Egg!', 0, True, [
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '             AAAAA                      ',
        '            A     A                     ',
        '           A       A                    ',
        '       AAAA         A                   ',
        '       A            A  AA               ',
        '       A            AAA A               ',
        '        A     A         AAA             ',
        '         A    A           A             ',
        '          AA              A             ',
        '            AA            A             ',
        '           A             A              ',
        '           AA          AA               ',
        '            A         A                 ',
        '            A        A                  ',
        '            A       A                   ',
        '   >         A AA AA              E     ',
        '             AA AA                      '
    ]],

    1: ['To Begin...', 0, True, [
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '            A              B            ',
        '            A              B        D   ',
        '   >        A              B            '
    ]],

    2: ['Further Practice', 0, True, [
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        ' D                CCC                   ',
        'AAA      BB                AAA          ',
        '                           A            ',
        '                        BBBA            ',
        '                  BB    B  A            ',
        '            AA    B     B  A            ',
        '   >  AA    A     B     B  A            '
    ]],

    3: ['Risky Manuver', 0, False, [
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                  CCCCA                 ',
        '                     LA                 ',
        '                      A                 ',
        '          HH      I   AGGG              ',
        '          BBBBB   CCCCCAAAAA            ',
        '                  C               HH    ',
        '  D               C           BBBBBB    ',
        'AAAAA             C >                   ',
        '                  CAAAAAA               ',
        'IIIIIIIIIIIIIIIIIICIIIIIIIIIIIIIIIIIIIII'
    ]],

    4: ['Pillars', 0, False, [
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '             C                          ',
        '             CHHHHGGGGGGC               ',
        '             CBBBBAAAAAACBB             ',
        '             A   BA     C       I       ',
        '     F       A   BA     CAA     C   <   ',
        '     C       A   BA     C   H   C  AAA  ',
        '     C     CCCCCCCA     C   BBBBC       ',
        'IIIIICIIIIIIICIIIIIIIIIICIIIIIIICIIIIIII'
    ]],

    5: ['An Unintended Solution', 255, True, [
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '            HI                          ',
        '        BBBBBC                          ',
        '             C     I                    ',
        '   A       IIC     C            BBB     ',
        '        CCCCCC     C     I      B       ',
        '             CHHHHHC     C    HHB       ',
        'BBBBB        CBBBBBCAAAAACBBBBBBB   AAAA',
        '    B        C  D  C  >  C              ',
        '   BB        CCCCCCCCCCCCC              ',
        'IIIIIIIIIIIIIIICIIIIIIICIIIIIIIIIIIIIIII'
    ]],

    6: ['Altitude', 255, False, [
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '   E        M         N    GG           ',
        '            A         B    AAAAAAA      ',
        '                                        ',
        '                                        ',
        '                              O         ',
        '                  H          CCC        ',
        '                  BBBB                  ',
        '                     B                  ',
        '        I      I     B                  ',
        ' >    N CIIIIIIC   M BCIIIIIIIIIIIIIIIII'
    ]],

    7: ['In Range', 0, False, [
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '         I     B                        ',
        '         C     B                        ',
        '         C  N  B                        ',
        '         CBBBBBB     GGGGGGG       AAA  ',
        '         C           AAAAAAA       A    ',
        '         C           I     I       A    ',
        '         C  M  I     C     C       A   M',
        '         CAAAAAC  HHHCH   HC       AAAAA',
        '    D          CBBBBBCBBBBBCH      A    ',
        '               C     A     CBBBB   A  < ',
        '               C     A     C       ACCCC',
        'IIIIIIIIIIIIIIIC  M  A     CIIIIIIIIIIII'
    ]],

    8: ['Panic!', 0, True, [
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        ',
        '                                        '
    ]]
}

# A: White Block
# B: Black Block
# C: Grey Block

# D: Exit White
# E: Exit Black
# F: Exit Grey

# G: White Pit Up
# H: Black Pit Up
# I: Grey Pit Up
# J: White Pit Down
# K: Black Pit Down
# L: Grey Pit Down

# M: White Jumpad Up
# N: Black Jumpad Up
# O: Grey JumPad Up
# P: White Jumpad Down
# Q: Black Jumpad Down
# R: Grey Jumpad Down

# S: White Breakable Up
# T: Black Breakable Up
# U: Grey Breakable Up
# V: White Breakable Down
# W: Black Breakable Down
# X: Grey Breakable Down

# Y: Spawn

# 1: Flipad Up White
# 2: Flipad Up Black
# 3: Flipad Up Grey
# 4: Flipad Down White
# 5: Flipad Down Black
# 6: Flipad Down Grey
# .: RGBSphere
