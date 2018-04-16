import pygame
import public


class Splitter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(public.all_sprites)

        self.image = pygame.Surface((800, 4))
        self.rect = self.image.get_rect()
        self.rect.y = ((public.SHEIGHT - 2) / 2)
        self.type = 'Splitter'

        self.image.fill(public.GREY)

    def draw(self):
        public.screen.blit(self.image, self.rect)
   