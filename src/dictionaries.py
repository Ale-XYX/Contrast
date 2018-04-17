import pygame
import glob
import os
import public

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
            os.path.join(os.path.dirname(__file__), 'res', 'pfall_0.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pfall_1.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pfall_2.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pfall_3.png')),
    ]
}
