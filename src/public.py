import pygame
pygame.init()

# Constants
BLACK = (0, 0, 0)
GREY = (192, 192, 192)
WHITE = (255, 255, 255)
SWIDTH = 800
SHEIGHT = 524
GRAVITY = 0.1
FPS = 60
FONTS = {}

# Classes
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
blocks = pygame.sprite.Group()

screen = pygame.display.set_mode((SWIDTH, SHEIGHT))
clock = pygame.time.Clock()

level = 1
