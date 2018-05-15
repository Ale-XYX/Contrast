import os
import sys
import glob
import pygame
import public
import functions

# Media
MEDIA = {}
images = glob.glob(os.path.join(os.path.dirname(__file__), 'res', '*.png'))
audio = glob.glob(os.path.join(os.path.dirname(__file__), 'res', '*.wav'))

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


# Sprites
block_ss = Spritesheet(MEDIA['block_ss'])
player_ss = Spritesheet(MEDIA['player_ss'])
obstacles_ss = Spritesheet(MEDIA['obstacles_ss'])

ANIMS = {
    0: player_ss.load_strip([0, 0, 20, 20], 4),

    1: player_ss.load_strip([0, 20, 20, 20], 4),

    2: player_ss.load_strip([0, 40, 20, 20], 4),

    3: player_ss.load_strip([0, 60, 20, 20], 4),

    4: player_ss.load_strip([0, 80, 20, 20], 4),

    5: player_ss.load_strip([0, 100, 20, 20], 4),

    6: obstacles_ss.load_strip([0, 0, 20, 20], 4),

    7: obstacles_ss.load_strip([0, 18, 20, 10], 4),

    8: obstacles_ss.load_strip([0, 28, 20, 10], 4),

    9: Spritesheet(MEDIA['rgbsphere_ss']).load_strip([0, 0, 10, 10], 24),

}

a = block_ss.load_strip([0, 0, 20, 20], 4)
a.extend(block_ss.load_strip([0, 20, 20, 20], 4))
a.extend(block_ss.load_strip([0, 40, 20, 20], 4))
a.extend(block_ss.load_strip([0, 60, 20, 20], 4))

ANIMS.update({10: a})

I_ANIMS = {}
G_ANIMS = {}

for key in ANIMS.keys():
    I_ANIMS.update({key: []})
    G_ANIMS.update({key: []})

    for image in ANIMS[key]:
        I_ANIMS[key].append(functions.ppc(image.copy(), 255, 0))
        G_ANIMS[key].append(functions.ppc(image.copy(), 192, 192))

# Levels
LEVELS = {
    0: ['Test_Level', 0, False, [
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXAXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXAAAXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXAXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XJXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        ]],

    24: ['EggBag!', 0, False, [
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXBBBXBXBXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXBBXBXBXBXBXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXBBBXXBXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXBXXXXBXXXX",
            "XXXXXXXXXXXXXAAAAAXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXAXXXXXAXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXAXXXXXXXAXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXAAAAXXXXXXXXXAXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXAXXXXXXXXXXXXAXXAAXXXXXXXXXXXXXXX",
            "XXXXXXXAXXXXXXXXXXXXAAAXAXXXXXXXXXXXXXXX",
            "XXXXXXXXAXXXXXAXXXXXXXXXAAAXXXXXXXXXXXXX",
            "XXXXXXXXXAXXXXAXXXXXXXXXXXAXXXXXXXXXXXXX",
            "XXXXXXXXXXAAXXXXXXXXXXXXXXAXXXXXXXXXXXXX",
            "XXXXXXXXXXXXAAXXXXXXXXXXXXAXXXXXXXXXXXXX",
            "XXXXXXXXXXXAXXXXXXXXXXXXXAXXXXXXXXXXXXXX",
            "XXXXXXXXXXXAAXXXXXXXXXXAAXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXAXXXXXXXXXAXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXAXXXXXXXXAXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXAXXXXXXXAXXXXXXXXXXXXXXXXXXX",
            "XXXJXXXXXXXXXAXAAXAAXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXAAXAAXXXXXXXXXXXXXXXXXXXXXX",
        ]],

    1: ['To Begin...', 0, False, [
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXAXXXXXXXXXXXXXXBXXXXXXXXXXXX",
            "XXXXXXXXXXXXAXXXXXXXXXXXXXXBXXXXXXXXKXXX",
            "XXXJXXXXXXXXAXXXXXXXXXXXXXXBXXXXXXXXXXXX",
        ]],

    2: ['Further Practice', 0, False, [
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XKXXXXXXXXXXXXXXXXCCCXXXXXXXXXXXXXXXXXXX",
            "AAAXXXXXXBBXXXXXXXXXXXXXXXXAAAXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXAXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXBBBAXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXBBXXXXBXXAXXXXXXXXXXXX",
            "XXXXXXXXXXXXAAXXXXBXXXXXBXXAXXXXXXXXXXXX",
            "XXXJXXAAXXXXAXXXXXBXXXXXBXXAXXXXXXXXXXXX",
        ]],

    3: ['Risky Manuver', 0, False, [
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXCCCCAXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXIAXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXAXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXFFXXXXXXHXXXADDDXXXXXXXXXXXXXX",
            "XXXXXXXXXXBBBBBXXXCCCCCAAAAAXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXCXXXXXXXXXXXXXXXFFXXXX",
            "XXKXXXXXXXXXXXXXXXCXXXXXXXXXXXBBBBBBXXXX",
            "AAAAAXXXXXXXXXXXXXCXJXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXCAAAAAAXXXXXXXXXXXXXXX",
            "HHHHHHHHHHHHHHHHHHCHHHHHHHHHHHHHHHHHHHHH",
        ]],

    4: ['Pillars', 0, False, [
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXCXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXCFFFFDDDDDDCXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXCBBBBAAAAAACBBXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXAXXXBAXXXXXCXXXXXXXHXXXXXXX",
            "XXXXXMXXXXXXXAXXXBAXXXXXCAAXXXXXCXXXJXXX",
            "XXXXXCXXXXXXXAXXXBAXXXXXCXXXFXXXCXXAAAXX",
            "XXXXXCXXXXXCCCCCCCAXXXXXCXXXBBBBCXXXXXXX",
            "HHHHHCHHHHHHHCHHHHHHHHHHCHHHHHHHCHHHHHHH",
        ]],

    5: ['An Unintended Solution', 255, True, [
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXFHXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXBBBBBCXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXCXXXXXHXXXXXXXXXXXXXXXXXXXX",
            "XXXAXXXXXXXHHCXXXXXCXXXXXXXXXXXXBBBXXXXX",
            "XXXXXXXXCCCCCCXXXXXCXXXXXHXXXXXXBXXXXXXX",
            "XXXXXXXXXXXXXCFFFFFCXXXXXCXXXXFFBXXXXXXX",
            "BBBBBXXXXXXXXCBBBBBCAAAAACBBBBBBBXXXAAAA",
            "XXXXBXXXXXXXXCXXKXXCXXJXXCXXXXXXXXXXXXXX",
            "XXXBBXXXXXXXXCCCCCCCCCCCCCXXXXXXXXXXXXXX",
            "HHHHHHHHHHHHHHHCHHHHHHHCHHHHHHHHHHHHHHHH",
        ]],

    6: ['Altitude', 0, False, [
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXLXXXXXXXXQXXXXXXXXXRXXXXDDXXXXXXXXXXX",
            "XXXXXXXXXXXXAXXXXXXXXXBXXXXAAAAAAAXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXSXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXFXXXXXXXXXXCCCXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXBBBBXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXBXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXHXXXXXXHXXXXXBXXXXXXXXXXXXXXXXXX",
            "XJXXXXRXCHHHHHHCXXXQXBCHHHHHHHHHHHHHHHHH",
            ]],

    7: ['In Range', 0, False, ['J']]
}

# A: White Block
# B: Black Block
# C: Grey Block
# D: White pit up
# E: White pit down
# F: Black pit up
# G: Black pit down
# H: Grey pit up
# I: Grey pit down
# J: Entrance
# K: Exit White
# L: Exit Black
# M: Exit Grey
# N: BreakableBlock White
# O: BreakableBlock Black
# P: BreakableBlock Grey
# Q: JumPad White
# R: JumPad Black
# S: JumPad Grey
# .: RGBSphere
