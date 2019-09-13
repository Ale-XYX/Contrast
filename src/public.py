import pygame
import platform
from os.path import join, dirname

pygame.init()
BLACK = 0
GREY = 192
WHITE = 255

OS = platform.system()
GRAVITY = 0.1
SHEIGHT = 485
SWIDTH = 800
FPS = 60

FONT_SM = pygame.font.Font(join(dirname(__file__), 'res', 'system.fon'), 30)
FONT_LG = pygame.font.Font(join(dirname(__file__), 'res', 'system.fon'), 50)

all_sprites = pygame.sprite.Group()
blocks = pygame.sprite.Group()

screen = pygame.display.set_mode((SWIDTH, SHEIGHT))
clock = pygame.time.Clock()
dt = clock.tick(FPS) / 1000

level = 1
level_max = -6
spawn = (0, 0)
bg_type = 0
wrapping = True
player = None
music = True

# :^)
