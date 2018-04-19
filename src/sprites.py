import os
import pygame
import pygame.gfxdraw
import random
import public
import dictionaries
clouds = [
    pygame.image.load(
        os.path.join(os.path.dirname(__file__), 'res', 'cloud0.png')),
    pygame.image.load(
        os.path.join(os.path.dirname(__file__), 'res', 'cloud1.png'))
]

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
        self.anim_cap = [75, 10, 25, 25]
        self.collided = None
        self.jump = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'res', 'jump.wav'))

        self.direction = 'Right'

    def update(self):
        self.pos.x += self.vel.x
        self.rect.x = self.pos.x

        self.collided = pygame.sprite.spritecollide(self, public.blocks, False)
        for block in self.collided:
            if block.color[0] != public.background[0] or block.color[0] == public.GREY[0]:
                if block.type != 'Entrance':
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

        self.collided = pygame.sprite.spritecollide(self, public.blocks, False)
        for block in self.collided:
            if block.color[0] != public.background[0] or block.color[0] == public.GREY[0]:
                if block.type != 'Entrance':
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
            if public.padding:
                self.rect.left = 1
            elif not public.padding:
                self.rect.right = public.SWIDTH 
                self.vel.x = 0
                self.anim_type = 0

            self.pos.x = self.rect.left

        elif self.rect.left <= 0:
            if public.padding:
                self.rect.right = public.SWIDTH - 1
            elif not public.padding:
                self.rect.left = 1
                self.vel.x = 0
                self.anim_type = 0

            self.pos.x = self.rect.left

        self.vel.y += public.GRAVITY

        if self.vel.y > 1:
            self.on_ground = False

        self.anim_ticks += 1

        if self.anim_ticks == self.anim_cap[self.anim_type]:
            self.anim_index = (self.anim_index + 1) % 4
            self.anim_ticks = 0
        else:
            if self.anim_ticks > self.anim_cap[self.anim_type]:
                self.anim_ticks = 0

        if not self.on_ground:
            if self.vel.y < 0:
                self.anim_type = 3
            elif self.vel.y > 0:
                self.anim_type = 2

        if public.background[0] == 255:
            self.image = dictionaries.inverted_animations[self.anim_type]
        else:
            self.image = dictionaries.animations[self.anim_type]

    def draw(self):
        inv = self.image[self.anim_index]

        if self.direction == 'Left':
            inv = pygame.transform.flip(inv, True, False)

        public.screen.blit(inv, self.rect)


class Block(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__(public.all_sprites, public.blocks)

        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)

        self.type = 'Block'
        self.order = 0
        self.color = color

        self.image.fill((self.color[0], self.color[1], self.color[2], 255))

    def update(self):
        if self.color[0] == public.background[0]:
            self.image.fill((self.color[0], self.color[1], self.color[2], 0))
        elif self.color[0] != public.background[0]:
            self.image.fill((self.color[0], self.color[1], self.color[2], 255))

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


class Title(pygame.sprite.Sprite):
    def __init__(self, title):
        super().__init__(public.all_sprites)

        self.image = pygame.Surface(public.FONTS['Plain'].render(title, False, (255, 255, 255)).get_size(), pygame.SRCALPHA).convert_alpha()
        self.text = public.FONTS['Plain'].render(title, False, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10

        self.alpha = 0
        self.dt = public.clock.tick(60) / 1000
        self.time = 1
        self.title = title
        self.type = 'Title'

    def update(self):
        if self.alpha == 255:
            self.kill()
        if self.time > 0:
            self.time -= self.dt
        elif self.time <= 0:
            if self.alpha != 255:
                self.alpha += 5

        if public.background[0] != 0:
            self.text = public.FONTS['Plain'].render(self.title, False, (0, 0, 0))
        elif public.background[0] == 0:
            self.text = public.FONTS['Plain'].render(self.title, False, (255, 255, 255))

        self.image.fill((public.background[0], public.background[1], public.background[2], self.alpha))

    def draw(self):
        public.screen.blit(self.text, self.rect)
        public.screen.blit(self.image, self.rect)


vels = {0: 0.2, 1: 0.5, 2: 0.9}


class Cloud(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__(public.clouds)

        self.image = pygame.transform.flip(clouds[type], True, False)
        self.rect = self.image.get_rect(center=pos)

        self.vel = vels[type]
        self.cap = vels[type]
        self.type = type
        self.pos = pygame.math.Vector2(pos)

    def update(self):
        self.pos.x-= self.vel
        self.rect.center = self.pos

        if self.pos.x < -20 or self.pos.x > 810:
            self.kill()

        if public.background[0] == 255 and self.vel != -self.cap:
            self.vel -= 0.1

        elif public.background[0] == 0 and self.vel != self.cap:
            self.vel += 0.1

    def draw(self):
        if public.background[0] == 255 and self.vel != -self.cap:
            self.image = clouds[self.type]

        elif public.background[0] == 0 and self.vel != self.cap:
            self.image = pygame.transform.flip(clouds[self.type], True, False)

        public.screen.blit(self.image, self.rect)


class Exit(pygame.sprite.Sprite):
    def __init__(self, pos, type, color):
        super().__init__(public.all_sprites, public.blocks)

        self.image = pygame.Surface((20, 20))
        self.rect = self.image.get_rect(topleft=pos)

        self.type = type
        self.color = color
        if self.type == 'Entrance':
            self.color = public.GREY

        self.image.fill(self.color)

    def draw(self):
        public.screen.blit(self.image, self.rect)


class Button(pygame.sprite.Sprite):
    def __init__(self, surf, psurf, rect, prect, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = rect
        self.normal = [surf, rect]
        self.pressed = [psurf, prect]
        self.type = 5

    def update(self):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            self.image, self.rect = self.pressed

        else:
            self.image, self.rect = self.normal

    def draw(self):
        public.screen.blit(self.image, self.rect)