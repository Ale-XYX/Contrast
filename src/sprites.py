import pygame
import random
import public
import dictionaries
import functions


# TODO: Add ground ticks attribute that determines ticks since touching ground, if larger than 4 that means person can jump
class Ox(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(public.all_sprites)

        self.image = dictionaries.ANIMS[0]
        self.invert = dictionaries.I_ANIMS[0]
        self.rect = self.image[0].get_rect(topleft=pos)

        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2()

        self.layer = 4
        self.won = False
        self.died = False
        self.type = 'Player'
        self.collided = None
        self.on_ground = True
        self.direction = 'R'
        self.jumping = False
        self.flip_cooldown = 0
        self.super_jump = False
        self.accelerating = False
        self.dt = public.clock.tick(public.FPS) / 1000

        self.anim_index = 0
        self.anim_type = 0
        self.anim_ticks = 0
        self.anim_caps = [75, 10, 25, 25, 13, 20]

    def update(self):
        self.pos.x += self.vel.x
        self.rect.x = self.pos.x

        self.collided = pygame.sprite.spritecollide(self, public.blocks, False)
        for block in self.collided:
            if block.color != public.bg_type:
                if self.vel.x > 0.05:
                    self.rect.right = block.rect.left if block.type not in \
                        ['Exit', 'Jumpad', 'RGBSphere'] else self.rect.right

                elif self.vel.x < 0.05:
                    self.rect.left = block.rect.right if block.type not in \
                        ['Exit', 'Jumpad', 'RGBSphere'] else self.rect.left

                self.accelerating = False if block.type not in \
                    ['Exit', 'Jumpad'] else True

                self.pos.x = self.rect.x

                if block.type == 'Pit' and not self.died:
                    self.died = True
                    self.anim_ticks = 0
                    self.anim_index = 0
                    dictionaries.MEDIA['died'].play()

                elif block.type == 'Exit' and not self.died:
                    public.level += 1
                    functions.generate_level(True)
                    dictionaries.MEDIA['finish'].play()

                    if public.level == 14:
                        dictionaries.MEDIA['greetings'].stop()
                        dictionaries.MEDIA['deathly'].play(-1)

                    self.kill()

                elif block.type == 'Breakable':
                    dictionaries.MEDIA['crumble'].play()
                    block.broken = True

                elif block.type == 'Jumpad' and not self.died and not \
                        self.super_jump:
                    dictionaries.MEDIA['jumpad'].play()
                    self.vel.y = -4.5
                    self.on_ground = False
                    self.super_jump = True

                elif block.type == 'RGBSphere':
                    dictionaries.MEDIA['collect'].play()
                    block.rect.y -= 10
                    self.won = True

        self.pos.y += self.vel.y
        self.rect.y = self.pos.y

        self.collided = pygame.sprite.spritecollide(self, public.blocks, False)
        for block in self.collided:
            if block.color != public.bg_type:
                if self.vel.y > 0:
                    self.rect.bottom = block.rect.top if block.type not in \
                        ['Exit', 'Jumpad', 'RGBSphere'] else self.rect.bottom

                elif self.vel.y < 0:
                    self.rect.top = block.rect.bottom if block.type not in \
                        ['Exit', 'Jumpad', 'RGBSphere'] else self.rect.top

                self.super_jump = False if block.type != 'Exit' else True
                self.jumping = False if block.type != 'Exit' else False
                self.on_ground = True if block.type not in \
                    ['Jumpad', 'Exit'] else False
                self.vel.y = 0 if block.type not in \
                    ['Exit', 'Jumpad', 'RGBSphere'] else self.vel.y

                self.pos.y = self.rect.y

                if block.type == 'Pit' and not self.died:
                    self.died = True
                    self.anim_ticks = 0
                    self.anim_index = 0
                    dictionaries.MEDIA['died'].play()

                elif block.type == 'Exit' and not self.died:
                    public.level += 1
                    functions.generate_level(True)
                    dictionaries.MEDIA['finish'].play()

                    if public.level == 14:
                        dictionaries.MEDIA['greetings'].stop()
                        dictionaries.MEDIA['deathly'].play(-1)

                    self.kill()

                elif block.type == 'Breakable':
                    dictionaries.MEDIA['crumble'].play()
                    block.broken = True

                elif block.type == 'Jumpad' and not self.died and not \
                        self.super_jump:
                    dictionaries.MEDIA['jumpad'].play()
                    self.vel.y = -4.5
                    self.on_ground = False
                    self.super_jump = True

                elif block.type == 'RGBSphere':
                    dictionaries.MEDIA['collect'].play()
                    block.rect.y -= 10
                    self.won = True

        if self.rect.right >= public.SWIDTH:
            if public.wrapping:
                self.rect.left = 1

            elif not public.wrapping:
                self.rect.right = public.SWIDTH
                self.vel.x = 0
                self.anim_type = 0
                self.accelerating = False

            self.pos.x = self.rect.left

        elif self.rect.left <= 0:
            if public.wrapping:
                self.rect.right = public.SWIDTH - 1

            elif not public.wrapping:
                self.rect.left = 1
                self.vel.x = 0
                self.anim_type = 0
                self.accelerating = False

            self.pos.x = self.rect.left

        self.vel.y += public.GRAVITY
        self.on_ground = (
            False if self.vel.y < -0.5 or self.vel.y > 0.5 else True
            ) if not self.jumping else self.on_ground

        public.player.vel.x = functions.clamp(public.player.vel.x, -10.0, 10.0)
        public.player.pos.x += public.player.vel.x
        public.player.vel.x *= 0.925

        self.anim_ticks += 1

        if self.anim_ticks == self.anim_caps[self.anim_type]:
            self.anim_index = (self.anim_index + 1) % 4
            self.anim_ticks = 0

        else:
            if self.anim_ticks > self.anim_caps[self.anim_type]:
                self.anim_ticks = 0

        self.anim_type = 1 if self.accelerating else 0

        self.anim_type = (
            2 if self.vel.y < 0 else 3 if self.vel.y > 0 else self.anim_type) \
            if not self.on_ground else self.anim_type
        self.anim_type = 3 if self.vel.y > 1 or self.super_jump else \
            self.anim_type

        self.anim_type = 4 if self.died else self.anim_type
        self.anim_type = 5 if self.won else self.anim_type

        if self.died and self.anim_index == 3:
            functions.generate_level(False)

        self.image = dictionaries.ANIMS[self.anim_type]
        self.invert = dictionaries.I_ANIMS[self.anim_type]

        self.flip_cooldown -= self.dt if self.flip_cooldown > 0 else 0

    def draw(self):
        prep_surf = self.image[self.anim_index] if public.bg_type == 0 else \
            self.invert[self.anim_index]
        prep_surf = pygame.transform.flip(prep_surf, True, False) \
            if self.direction == 'L' else prep_surf

        public.screen.blit(prep_surf, self.rect)

    def jump(self):
        if self.on_ground and not self.died and not self.won:
            self.vel.y = -3
            self.jumping = True
            self.on_ground = False
            dictionaries.MEDIA['jump'].play()

    def flip(self):
        if self.flip_cooldown <= 0 and not self.died and not self.won:
            inside = False

            for sprite in public.blocks:
                if sprite.rect.colliderect(self.rect):
                    inside = True

            if not inside:
                dictionaries.MEDIA['flip'].play()
                public.bg_type = 0 if public.bg_type == 255 else 255

            else:
                dictionaries.MEDIA['denied'].play()

            self.flip_cooldown = 1


class Block(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__(public.all_sprites, public.blocks)

        self.image = pygame.Surface((20, 20))
        self.transparent = self.image.copy()
        self.rect = self.image.get_rect(topleft=pos)

        self.type = 'Block'
        self.color = color
        self.layer = 3

        self.image.fill([self.color] * 3)
        self.transparent.set_alpha(0)

    def draw(self):
        prep_surf = self.transparent if public.bg_type == self.color else \
            self.image

        public.screen.blit(prep_surf, self.rect)


class Pit(pygame.sprite.Sprite):
    def __init__(self, pos, color, direction):
        super().__init__(public.all_sprites, public.blocks)

        self.image = dictionaries.I_ANIMS[7] if color == 255 else \
            dictionaries.ANIMS[7] if color == 0 else dictionaries.G_ANIMS[7]
        self.image = [
            pygame.transform.flip(image, False, True) for image in self.image
            ] if direction == 'D' else self.image
        self.transparent = pygame.Surface(self.image[0].get_size())

        self.rect = self.image[0].get_rect(topleft=pos)
        self.rect.y = self.rect.y + 10 if direction == 'U' else self.rect.y

        self.type = 'Pit'
        self.color = color
        self.layer = 3

        self.anim_index = 0
        self.anim_ticks = 0

        self.transparent.set_alpha(0)

    def update(self):
        self.anim_ticks += 1

        if self.anim_ticks == 10:
            self.anim_ticks = 0
            self.anim_index = (self.anim_index + 1) % 4

    def draw(self):
        prep_surf = self.transparent if public.bg_type == self.color else \
            self.image[self.anim_index]

        public.screen.blit(prep_surf, self.rect)


class Exit(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__(public.all_sprites, public.blocks)

        self.image = dictionaries.I_ANIMS[6] if color == 255 else \
            dictionaries.ANIMS[6] if color == 0 else dictionaries.G_ANIMS[6]
        self.rect = self.image[0].get_rect(topleft=pos)
        self.transparent = surf = pygame.Surface(self.image[0].get_size())

        self.type = 'Exit'
        self.color = color
        self.layer = 3

        self.anim_index = 0
        self.anim_ticks = 0

        self.transparent.set_alpha(0)

    def update(self):
        self.anim_ticks += 1

        if self.anim_ticks == 10:
            self.anim_ticks = 0
            self.anim_index = (self.anim_index + 1) % 4

    def draw(self):
        prep_surf = self.transparent if public.bg_type == self.color else \
            self.image[self.anim_index]

        public.screen.blit(prep_surf, self.rect)


class Breakable(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__(public.all_sprites, public.blocks)

        self.image = pygame.Surface((20, 10))
        self.transparent = self.image.copy()
        self.rect = self.image.get_rect(topleft=pos)

        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2()
        self.type = 'Breakable'
        self.broken = False
        self.color = color
        self.layer = 2
        self.alpha = 255

        self.image.fill([self.color] * 3)

        self.transparent.set_alpha(0)

    def update(self):
        self.vel.y += public.GRAVITY - 0.01 if self.broken else 0
        self.alpha -= 5 if self.broken and self.alpha != 0 else 0
        self.pos += self.vel
        self.rect.topleft = self.pos

        if self.alpha == 0:
            self.kill()

        self.image.set_alpha(self.alpha)

    def draw(self):
        prep_surf = self.transparent if public.bg_type == self.color else \
            self.image

        public.screen.blit(prep_surf, self.rect)


class Jumpad(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__(public.all_sprites, public.blocks)

        self.image = dictionaries.I_ANIMS[8] if color == 255 else \
            dictionaries.ANIMS[8] if color == 0 else dictionaries.G_ANIMS[8]
        self.transparent = pygame.Surface((20, 10))
        self.rect = self.image[0].get_rect(topleft=pos)
        self.rect.y += 10

        self.type = 'Jumpad'
        self.color = color
        self.layer = 3

        self.anim_index = 0
        self.anim_ticks = 0

        self.transparent.set_alpha(0)

    def update(self):
        self.anim_ticks += 1

        if self.anim_ticks == 10:
            self.anim_ticks = 0
            self.anim_index = (self.anim_index + 1) % 4

    def draw(self):
        prep_surf = self.transparent if public.bg_type == self.color else \
            self.image[self.anim_index]

        public.screen.blit(prep_surf, self.rect)


class RGBSphere(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__(public.all_sprites, public.blocks)

        self.image = dictionaries.ANIMS[9]
        self.rect = self.image[0].get_rect(topleft=pos)
        self.rect.x += 5
        self.rect.y += 5

        self.type = 'RGBSphere'
        self.color = color
        self.layer = 3

        self.anim_index = 0
        self.anim_ticks = 0

    def update(self):
        self.anim_ticks += 1

        if self.anim_ticks == 10:
            self.anim_ticks = 0
            self.anim_index = (self.anim_index + 1) % 24

    def draw(self):
        public.screen.blit(self.image[self.anim_index], self.rect)


class Cloud(pygame.sprite.Sprite):
    def __init__(self, pos, cloud_type):
        super().__init__(public.all_sprites)

        self.image = dictionaries.MEDIA['cloud_' + str(cloud_type)]
        self.rect = self.image.get_rect(center=pos)

        self.pos = pygame.math.Vector2(pos)
        self.vel = [0.2, 0.5][cloud_type]
        self.layer = cloud_type
        self.type = 'Cloud'

    def update(self):
        self.pos.x -= self.vel
        self.rect.center = self.pos

        if self.pos.x < -20 or self.pos.x > public.SWIDTH + 10:
            self.kill()

            generated_int = random.randint(0, 1)
            cloud = Cloud(
                (public.SWIDTH + 10,
                    random.randint(0, public.SHEIGHT)), generated_int)

    def draw(self):
        public.screen.blit(self.image, self.rect)


class Title(pygame.sprite.Sprite):
    def __init__(self, text):
        super().__init__(public.all_sprites)

        self.image = public.FONT_SM.render(text, False, (255, 255, 255))
        self.rect = self.image.get_rect(topleft=(10, 10))

        self.dt = public.clock.tick(public.FPS) / 1000
        self.timer = 1
        self.alpha = 255
        self.layer = 4
        self.text = text
        self.type = 'Title'

    def update(self):
        if self.timer > 0:
            self.timer -= self.dt

        elif self.timer <= 0 and self.alpha != 0:
            self.alpha -= 5

            if self.alpha == 0:
                self.kill()

        self.image = public.FONT_SM.render(
            self.text, False, [0 if public.bg_type == 255 else 255] * 3)
        self.image.set_alpha(self.alpha)

    def draw(self):
        public.screen.blit(self.image, self.rect)


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(public.all_sprites, public.blocks)

        self.image = pygame.Surface((800, 3))
        self.rect = self.image.get_rect(topleft=(0, 480))

        self.layer = 3
        self.type = 'Block'
        self.color = 192

        self.image.fill([self.color] * 3)

    def draw(self):
        public.screen.blit(self.image, self.rect)
