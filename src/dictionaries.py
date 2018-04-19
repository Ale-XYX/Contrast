import pygame
import glob
import os
import public


def invert(surface):
    'Black changed to white. Others changed to black.'
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            r, g, b, a = surface.get_at((x, y))

            if (r, g, b) == (0, 0, 0):
                r, g, b = (255, 255, 255)

            elif (r, g, b) == (255, 255, 255):
                r, g, b = (0, 0, 0)

            surface.set_at((x, y), (r, g, b, a))
    return surface


animations = {
   0: [
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pidle_0.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pidle_1.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pidle_2.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pidle_3.png')),
    ],
    1: [
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pwalk_0.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pwalk_1.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pwalk_2.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pwalk_3.png')),
    ],
    2: [
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pfall_0.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pfall_1.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pfall_2.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pfall_3.png')),
    ],
    3: [
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pjump_0.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pjump_1.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pjump_2.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pjump_3.png')),
    ],
}

inverted_animations = {}

for set in animations.keys():
    inverted_animations.update({set: []})

    for frame in animations[set]:
        inverted_animations[set].append(invert(frame.copy()))
