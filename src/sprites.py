import os
import pygame
import random
import public
import pyganim
import dictionaries


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)

        self.image = dictionaries.animations['Idle']
        self.rect = self.image[0] .get_rect(topleft=pos)

        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2(0, 0)

        self.type = 'Player'
        self.on_ground = True
        self.max_speed = 2
        self.min_speed = 0
        self.anim_index = 0
        self.anim_ticks = 0
        self.anim_cap = 75

    def update(self):
        self.pos.x += self.vel.x
        self.rect.x = self.pos.x

        collided = pygame.sprite.spritecollide(self, public.blocks, False)
        for block in collided:
            if self.vel.x > 0:
                self.rect.right = block.rect.left

            elif self.vel.x < 0:
                self.rect.left = block.rect.right

            self.pos.x = self.rect.x

        self.pos.y += self.vel.y
        self.rect.y = self.pos.y

        collided = pygame.sprite.spritecollide(self, public.blocks, False)
        for block in collided:
            if self.vel.y > 0:
                self.rect.bottom = block.rect.top
                self.vel.y = 0
                self.on_ground = True

            elif self.vel.y < 0:
                self.rect.top = block.rect.bottom
                self.vel.y = 0

            self.pos.y = self.rect.y

        if self.rect.bottom >= public.SHEIGHT:
            self.vel.y = 0
            self.rect.bottom = public.SHEIGHT
            self.pos.y = self.rect.y
            self.on_ground = True

        else:
            self.vel.y += public.GRAVITY

        self.anim_ticks += 1

        if self.anim_ticks == self.anim_cap:
            self.anim_index = (self.anim_index + 1) % 4
            self.anim_ticks = 0

        print(self.anim_ticks)

    def draw(self):
        public.screen.blit(self.image[self.anim_index], self.rect)


class Splitter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(public.all_sprites, public.blocks)

        self.image = pygame.Surface((800, 4))
        self.rect = self.image.get_rect()
        self.rect.y = (((public.SHEIGHT - 2) / 2) - 1)

        self.type = 'Splitter'

        self.image.fill(public.GREY)

    def draw(self):
        public.screen.blit(self.image, self.rect)
   