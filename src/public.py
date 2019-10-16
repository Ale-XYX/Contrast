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
regenables = pygame.sprite.Group()

# MAJOR GAME VARIABLES
# Mess with these, just keep in mind that it may completely break the game.
screen = pygame.display.set_mode((SWIDTH, SHEIGHT))
clock = pygame.time.Clock()
dt = clock.tick(FPS) / 1000

level = 1
level_max = 0
spawn = (0, 0)
bg_type = 0
init_bg_type = 0
wrapping = True
player = None
flip_status = False
music = True
end_title = False

# :^)
