import pygame
import os

pygame.init()

# Constants
BLACK = (0, 0, 0)
GREY = (192, 192, 192)
WHITE = (255, 255, 255)
SWIDTH = 800
SHEIGHT = 483
FPS = 60
FONTS = {'Plain': pygame.font.Font(os.path.join(os.path.dirname(__file__), 'res', 'vgasys.ttf'), 15), 'BigBoi': pygame.font.Font(os.path.join(os.path.dirname(__file__), 'res', 'vgasys.ttf'), 20)}

# Classes
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
blocks = pygame.sprite.Group()
clouds = pygame.sprite.Group()
text = pygame.sprite.Group()

screen = pygame.display.set_mode((SWIDTH, SHEIGHT))
clock = pygame.time.Clock()

background = (0, 0, 0)
level = 14
spawn = (0, 0)
padding = True
title = 'Congrats!, You found my unnessisary placeholder!'

player = None
breakables = []
won = False