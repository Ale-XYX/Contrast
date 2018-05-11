#!/usr/bin/env python3
import sys
import subprocess

sys.path.insert(0, 'src')
import game

try:
    import pygame

except ModuleNotFoundError:
    command = ['sudo'] if game.public.OS in ['Darwin', 'Linux'] else []
    command.extend(['py', '-m', 'pip', 'install', 'pygame'])
    subprocess.call(command)

    import pygame

if __name__ == '__main__':
    pygame.init()
    game.title()
    pygame.quit()
