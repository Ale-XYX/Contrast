import os
import pygame
import random
import public
import dictionaries

# Player: 


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)

        self.image = dictionaries.animations[0]
        self.rect = self.image[0].get_rect(center=pos)

        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2(0, 0)

        self.type = 'Player'
        self.on_ground = False
        self.max_speed = 2
        self.min_speed = 0

        self.anim_type = 0
        self.anim_index = 0
        self.anim_ticks = 0
        self.anim_cap = [75, 10, 25, 25, 100]

        self.direction = 'Right'

    def update(self):
        self.pos.x += self.vel.x
        self.rect.x = self.pos.x

        collided = pygame.sprite.spritecollide(self, public.blocks, False)
        for block in collided:
            if block.color[0] != public.background[0] or block.color[0] == public.GREY[0]:
                if self.vel.x > 0:
                    self.rect.right = block.rect.left
                    self.anim_type = 0

                elif self.vel.x < 0:
                    self.rect.left = block.rect.right
                    self.anim_type = 0

                self.pos.x = self.rect.x

                if block.type == 'Switch':
                    if not block.is_on:
                        block.is_on

        self.pos.y += self.vel.y
        self.rect.y = self.pos.y

        collided = pygame.sprite.spritecollide(self, public.blocks, False)
        for block in collided:
            if block.color[0] != public.background[0] or block.color[0] == public.GREY[0]:
                if self.vel.y > 0:
                    self.rect.bottom = block.rect.top
                    self.vel.y = 0
                    self.on_ground = True

                elif self.vel.y < 0:
                    self.rect.top = block.rect.bottom
                    self.vel.y = 0
                    self.on_ground = True

                if block.type == 'Switch':
                    if not block.is_on:
                        block.is_on = True
                        if public.background[0] == 0:
                            public.background = (255, 255, 255)
                        elif public.background[0] == 255:
                            public.background = (0, 0, 0)

            self.pos.y = self.rect.y

        if self.rect.right >= public.SWIDTH:
            self.rect.left = 1
            self.pos.x = self.rect.left

        elif self.rect.left <= 0:
            self.rect.right = public.SWIDTH - 1
            self.pos.x = self.rect.left

        self.vel.y += public.GRAVITY

        self.anim_ticks += 1

        if self.anim_ticks == self.anim_cap[self.anim_type]:
            self.anim_index = (self.anim_index + 1) % 4
            self.anim_ticks = 0
        else:
            if self.anim_ticks > self.anim_cap[self.anim_type]:
                self.anim_ticks = 0

        if not self.on_ground:
            if self.vel.y > 0:
                self.anim_type = 2
            elif self.vel.y < 0:
                self.anim_type = 3

        self.image = dictionaries.animations[self.anim_type]

    def draw(self):
        if public.background[0] == 255:
            inv = pygame.PixelArray(self.image[self.anim_index]).extract((0, 0, 0), 0.07).surface.convert_alpha()
        else:
            inv = self.image[self.anim_index]

        if self.direction == 'Left':
            inv = pygame.transform.flip(inv, True, False)

        public.screen.blit(inv, self.rect)


class Block(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__(public.all_sprites, public.blocks)

        self.image = pygame.Surface((20, 20))
        self.rect = self.image.get_rect(topleft=pos)

        self.type = 'Block'
        self.order = 0
        self.color = color

        self.image.fill(self.color)

    def draw(self):
        public.screen.blit(self.image, self.rect)


class Splitter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(public.all_sprites, public.blocks)

        self.image = pygame.Surface((800, 3))
        self.rect = self.image.get_rect()
        self.rect.y = 480

        self.type = 'Block'
        self.color = public.GREY

        self.image.fill(self.color)

    def draw(self):
        public.screen.blit(self.image, self.rect)
