import pygame
import glob
import os
import public


def invert(surface):
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            r, g, b, a = surface.get_at((x, y))

            if (r, g, b) == (0, 0, 0):
                r, g, b = (255, 255, 255)

            elif (r, g, b) == (255, 255, 255):
                r, g, b = (0, 0, 0)

            surface.set_at((x, y), (r, g, b, a))
    return surface


def greyify(surface):
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            r, g, b, a = surface.get_at((x, y))

            if (r, g, b) == (0, 0, 0):
                r, g, b = (public.GREY)

            elif (r, g, b) == (255, 255, 255):
                r, g, b = (public.GREY)

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
    4: [
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pdied_0.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pdied_1.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pdied_2.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pdied_3.png')),
    ],
    5: [
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pwon_0.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pwon_1.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pwon_2.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pwon_3.png')),
    ],
    6: [
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'exit_0.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'exit_1.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'exit_2.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'exit_3.png')),
    ],
    7: [
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pit_0.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pit_1.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pit_2.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pit_3.png')),
    ],
    8: [
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'jumpad_0.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'jumpad_1.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'jumpad_2.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'jumpad_3.png')),
    ],
    9: [
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'shiny_00.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'shiny_01.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'shiny_02.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'shiny_03.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'shiny_04.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'shiny_05.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'shiny_06.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'shiny_07.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'shiny_08.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'shiny_09.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'shiny_10.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'shiny_11.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'shiny_12.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'shiny_13.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'shiny_14.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'shiny_15.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'shiny_16.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'shiny_17.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'shiny_18.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'shiny_19.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'shiny_20.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'shiny_21.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'shiny_22.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'shiny_23.png')),
    ]

}

inverted_animations = {}
grey_animations = {}

for set in animations.keys():
    inverted_animations.update({set: []})
    grey_animations.update({set: []})

    for frame in animations[set]:
        inverted_animations[set].append(invert(frame.copy()))
        grey_animations[set].append(greyify(frame.copy()))
