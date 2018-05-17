#!/usr/bin/env python3

import sys
import subprocess

sys.path.insert(0, 'src')
import game

try:
    import pygame

except ModuleNotFoundError:
    if game.public.OS == 'Windows':
        subprocess.call(['py', '-m', 'pip', 'install', 'pygame'])

    else:
        print('Unsupported OS to install pygame, please install manually.')

    import pygame

if __name__ == '__main__':
    pygame.init()
    game.title()
    pygame.quit()
