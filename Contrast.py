#!/usr/bin/env python3

import sys
import time
import subprocess

try:
    import pygame
    import pytmx

except ModuleNotFoundError:
    print('! PyTMX/Pygame not installed !')
    time.sleep(3)
    sys.exit()

sys.path.insert(0, 'src')
import game

if __name__ == '__main__':
    game.public.level = 12

    pygame.init()
    game.title()
    pygame.quit()
