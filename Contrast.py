#!/usr/bin/env python3

import sys
import subprocess

try:
    import pygame
    import pytmx

except ModuleNotFoundError:
    if game.public.OS == 'Windows':
        subprocess.call(['py', '-m', 'pip', 'install', 'pygame'])
        subprocess.call(['py', '-m', 'pip', 'install', 'pytmx'])

    else:
        print('Unsupported OS to install pygame/pytmx, please install manually.')

    import pygame
    import pytmx

sys.path.insert(0, 'src')
import game

if __name__ == '__main__':
    # print(game.functions.generate_blank())
    # game.public.level = 0

    pygame.init()
    game.title()
    pygame.quit()
