import pygame
import glob
import os
import public
import pyganim

animations = {
   'Idle': [
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pidle_0.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pidle_1.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pidle_2.png')),
        pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'res', 'pidle_3.png')),
    ],
}
