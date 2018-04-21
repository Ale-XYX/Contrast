import os
import pygame
import random
import public
import levels
import dictionaries
import functions

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
        self.anim_cap = [75, 10, 25, 25, 13, 20]
        self.collided = None
        self.jump = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'res', 'jump.wav'))
        self.exit = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'res', 'leave.wav'))
        self.die = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'res', 'died.wav'))
        self.jumpad = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'res', 'jumpad.wav'))
        self.crumble = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'res', 'crumble.wav'))
        self.pas = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'res', 'pass.wav'))
        self.won = False
        self.died = False
        self.super_jump = False
        self.gravity = 0.1

        self.direction = 'Right'

    def update(self):
        self.pos.x += self.vel.x
        self.rect.x = self.pos.x

        self.collided = pygame.sprite.spritecollide(self, public.blocks, False)
        for block in self.collided:
            if block.color[0] != public.background[0] or block.color[0] == public.GREY[0] and not self.won and not public.won:
                if block.type != 'Exit' and block.type != 'JumpPad' and block.type != 'Sphere':
                    if self.vel.x > 0:
                        self.rect.right = block.rect.left

                        if not self.died:
                            self.anim_type = 0

                    elif self.vel.x < 0:
                        self.rect.left = block.rect.right

                        if not self.died:
                            self.anim_type = 0

                    self.pos.x = self.rect.x

                    if block.type == 'Pit' and not self.died:
                        self.died = True
                        self.anim_index = 0
                        self.anim_ticks = 0
                        self.die.play()

                    elif block.type == 'Breakable':
                        block.broken = True
                        self.crumble.play()

                elif block.type == 'JumpPad' and self.on_ground:
                    self.vel.y = -4.5
                    self.on_ground = False
                    self.super_jump = True
                    self.jumpad.play()

                elif block.type == 'Exit' and not self.won:
                        public.level += 1
                        self.exit.play()
                        functions.generate_level(True)
                        self.won = True


        for block in self.collided:
            if block.type == 'Sphere' and not public.won:
                block.rect.y -= 20
                public.won = True
                self.pas.play()
                break


        self.pos.y += self.vel.y
        self.rect.y = self.pos.y

        self.collided = pygame.sprite.spritecollide(self, public.blocks, False)
        for block in self.collided:
            if block.color[0] != public.background[0] or block.color[0] == public.GREY[0] and not self.won and not public.won:
                if block.type != 'Exit' and block.type != 'JumpPad' and block.type != 'Sphere':
                    if self.vel.y > 0:
                        self.rect.bottom = block.rect.top
                        self.vel.y = 0
                        self.on_ground = True
                        self.super_jump = False

                    elif self.vel.y < 0:
                        self.rect.top = block.rect.bottom
                        self.vel.y = 0
                        self.on_ground = True
                        self.super_jump = False

                    if block.type == 'Pit' and not self.died:
                        self.died = True
                        self.anim_index = 0
                        self.anim_ticks = 0
                        self.die.play()

                    elif block.type == 'Breakable':
                        block.broken = True
                        self.crumble.play()

                elif block.type == 'JumpPad' and self.on_ground:
                    self.vel.y = -4.5
                    self.on_ground = False
                    self.super_jump = True
                    self.jumpad.play()

                elif block.type == 'Exit' and not self.won:
                    public.level += 1
                    self.exit.play()
                    functions.generate_level(True)
                    self.won = True

            self.pos.y = self.rect.y

        for block in self.collided:
            if block.type == 'Sphere' and not public.won:
                block.rect.y -= 20
                public.won = True
                self.pas.play()
                break

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

        self.vel.y += self.gravity

        if self.vel.y > 1:
            self.on_ground = False

        self.anim_ticks += 1

        if self.anim_ticks == self.anim_cap[self.anim_type]:
            self.anim_index = (self.anim_index + 1) % 4
            self.anim_ticks = 0
        else:
            if self.anim_ticks > self.anim_cap[self.anim_type]:
                self.anim_ticks = 0

        if not self.on_ground and not self.died and not public.won:
            if self.vel.y < 0 and not self.super_jump:
                self.anim_type = 3
            elif self.vel.y > 0 or self.super_jump:
                self.anim_type = 2

        elif self.died and not public.won:
            self.anim_type = 4

        elif public.won:
            self.anim_type = 5

        if public.background[0] == 255:
            self.image = dictionaries.inverted_animations[self.anim_type]
        else:
            self.image = dictionaries.animations[self.anim_type]

        if self.died and self.anim_index == 3:
            functions.generate_level(False)
            self.kill()


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
        super().__init__(public.all_sprites, public.text)

        self.image = public.FONTS['Plain'].render(title, False, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10

        self.alpha = 0
        self.alphab = 255
        self.dt = public.clock.tick(60) / 1000
        self.time = 1
        self.title = title
        self.type = 'Title'

    def update(self):
        if self.alpha == 255 or self.alphab == 0:
            self.kill()
            public.text.empty()

        if self.time > 0:
            self.time -= self.dt

        elif self.time <= 0:
            if self.alpha != 255:
                self.alpha += 5

            if self.alphab != 0:
                self.alphab -= 5

        if public.background[0] != 0:
            self.image = public.FONTS['Plain'].render(self.title, False, (self.alpha, self.alpha, self.alpha))
        elif public.background[0] == 0:
            self.image = public.FONTS['Plain'].render(self.title, False, (self.alphab, self.alphab, self.alphab))

    def draw(self):
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
    def __init__(self, pos, color):
        super().__init__(public.all_sprites, public.blocks)

        self.image = dictionaries.animations[6]
        self.rect = self.image[0].get_rect(topleft=pos)

        self.type = 'Exit'
        self.color = color
        self.anim_index = 0
        self.anim_ticks = 0

    def update(self):
        self.anim_ticks += 1

        if self.anim_ticks == 10:
            self.anim_ticks = 0
            self.anim_index = (self.anim_index + 1) % 4

    def draw(self):
        if self.color[0] == public.background[0]:
            surf = pygame.Surface(self.image[self.anim_index].get_size(), pygame.SRCALPHA)
            surf.fill((0, 0, 0, 0))

        elif self.color[0] != public.background[0]:
            if self.color[0] == 255:
                self.image = dictionaries.inverted_animations[6]
                surf = self.image[self.anim_index]

            elif self.color[0] == 192:
                self.image = dictionaries.grey_animations[6]
                surf = self.image[self.anim_index]  

            elif self.color[0] == 0:
                self.image = dictionaries.animations[6]
                surf = self.image[self.anim_index]            

        public.screen.blit(surf, self.rect)


class Pit(pygame.sprite.Sprite):
    def __init__(self, pos, orientation, color):
        self.image = dictionaries.animations
        super().__init__(public.all_sprites, public.blocks)

        self.image = dictionaries.animations[7]
        self.rect = self.image[0].get_rect(topleft=pos)

        self.type = 'Pit'
        self.color = color
        self.anim_index = 0
        self.anim_ticks = 0
        self.orientation = orientation

    def update(self):
        self.anim_ticks += 1

        if self.anim_ticks == 10:
            self.anim_ticks = 0
            self.anim_index = (self.anim_index + 1) % 4

    def draw(self):

        if self.color[0] == public.background[0]:
            surf = pygame.Surface(self.image[self.anim_index].get_size(), pygame.SRCALPHA)
            surf.fill((0, 0, 0, 0))

        elif self.color[0] != public.background[0]:
            if self.color[0] == 255:
                self.image = dictionaries.inverted_animations[7]
                surf = self.image[self.anim_index]

            elif self.color[0] == 192:
                self.image = dictionaries.grey_animations[7]
                surf = self.image[self.anim_index] 

            elif self.color[0] == 0:
                self.image = dictionaries.animations[7]
                surf = self.image[self.anim_index]

        if self.orientation:
            surf = pygame.transform.flip(surf, False, True)

        public.screen.blit(surf, self.rect)


class BreakableBlock(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__(public.all_sprites, public.blocks)

        self.image = pygame.Surface((20, 10), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)

        self.type = 'Breakable'
        self.color = color
        self.broken = False
        self.pos = pygame.math.Vector2(pos)
        self.vel = 0

    def update(self):
        if self.broken:
            self.vel += 0.09

        self.pos.y += self.vel
        self.rect.center = self.pos

        if self.pos.y > public.SHEIGHT + 10:
            self.kill()

        if self.color[0] == public.background[0]:
            self.image.fill((self.color[0], self.color[1], self.color[2], 0))
        elif self.color[0] != public.background[0]:
            self.image.fill((self.color[0], self.color[1], self.color[2], 255))

    def draw(self):
        public.screen.blit(self.image, self.rect)


class JumpPad(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__(public.all_sprites, public.blocks)

        self.image = dictionaries.animations[8]
        self.rect = self.image[0].get_rect(topleft=pos)

        self.type = 'JumpPad'
        self.color = color
        self.anim_index = 0
        self.anim_ticks = 0

    def update(self):
        self.anim_ticks += 1

        if self.anim_ticks == 15:
            self.anim_ticks = 0
            self.anim_index = (self.anim_index + 1) % 4

    def draw(self):
        if self.color[0] == public.background[0]:
            surf = pygame.Surface(self.image[self.anim_index].get_size(), pygame.SRCALPHA)
            surf.fill((0, 0, 0, 0))

        elif self.color[0] != public.background[0]:
            if self.color[0] == 255:
                self.image = dictionaries.inverted_animations[8]
                surf = self.image[self.anim_index]

            elif self.color[0] == 192:
                self.image = dictionaries.grey_animations[8]
                surf = self.image[self.anim_index] 

            elif self.color[0] == 0:
                self.image = dictionaries.animations[8]
                surf = self.image[self.anim_index]

        public.screen.blit(surf, self.rect)
   

class Test(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__(public.all_sprites, public.blocks)

        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)

        self.image.fill(color)
        self.type = 'none'
        self.color = color

    def draw(self):
        public.screen.blit(self.image, self.rect)


class Sphere(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__(public.all_sprites, public.blocks)

        self.image = dictionaries.animations[9]
        self.rect = self.image[0].get_rect(topleft=pos)

        self.type = 'Sphere'
        self.color = color
        self.anim_index = 0
        self.anim_ticks = 0

    def update(self):
        self.anim_ticks += 1

        if self.anim_ticks == 10:
            self.anim_ticks = 0
            self.anim_index = (self.anim_index + 1) % 23

    def draw(self):          

        public.screen.blit(self.image[self.anim_index], self.rect)