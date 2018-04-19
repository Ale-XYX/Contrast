import pip
import sys

if __name__ == '__main__':
    try:
        import pygame
    except ModuleNotFoundError:
        pip.main('install', 'pygame')

    sys.path.insert(0, './src')
    import game

    pygame.init()
    game.title()
    pygame.quit()
