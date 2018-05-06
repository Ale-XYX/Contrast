import platform
import pygame
import platform
from os.path import join, dirname

pygame.init()
BLACK = (0, 0, 0)
GREY = (192, 192, 192)
WHITE = (255, 255, 255)

OS = platform.system()
GRAVITY = 0.1
SHEIGHT = 483
SWIDTH = 800
FPS = 60

fargs = ['vgawin.fon', 30, 50] if OS == 'Windows' else ['vgattf.ttf', 15, 20]
FONT_SM = pygame.font.Font(join(dirname(__file__), 'res', fargs[0]), fargs[1])
FONT_LG = pygame.font.Font(join(dirname(__file__), 'res', fargs[0]), fargs[2])

all_sprites = pygame.sprite.Group()
blocks = pygame.sprite.Group()

screen = pygame.display.set_mode((SWIDTH, SHEIGHT))
clock = pygame.time.Clock()

level = 5
spawn = (0, 0)
bg_type = 0
wrapping = True
player = None
