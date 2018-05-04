#!/usr/bin/env python3

import sys
import platform
import subprocess

sys.path.insert(0, 'src')
import game

try:
    import pygame

except ModuleNotFoundError:
    if game.public.OS == 'Windows':
        subprocess.call(['py', '-m', 'pip', 'install', 'pygame'])

    elif game.public.OS == 'Darwin':
        subprocess.call(['sudo', 'py', '-m', 'pip', 'install', 'pygame'])

    elif game.public.OS == 'Linux':
        subprocess.call(['sudo', 'py', '-m', 'pip', 'install', '--user', 'pygame'])

    import pygame

if __name__ == '__main__':
    pygame.init()
    game.title()
    pygame.quit()
