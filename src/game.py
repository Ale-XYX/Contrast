import re
import bz2
import pygame
import public
import sprites
import functions
import dictionaries
import random


def title(debug):
    pygame.display.set_caption('Contrast')
    pygame.display.set_icon(pygame.image.fromstring(bz2.decompress(
        dictionaries.MEDIA['icon']), (32, 32), 'RGBA'))

    info_text = public.FONT_LG.render(
        'ENTER TO BEGIN', False, [public.WHITE] * 3)

    if len(debug) != 1:
        public.music = False
        m = re.search('map_(.+?).tmx', debug[1])

        if m:
            public.level = int(m.group(1))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game()
                    return 0

        public.screen.fill([public.BLACK] * 3)

        public.screen.blit(dictionaries.IMAGES['Logo'], functions.center(
            dictionaries.IMAGES['Logo']))
        public.screen.blit(info_text,
                           (functions.center(info_text)[0], 290))

        pygame.display.flip()
        public.clock.tick(public.FPS)


def game():
    if public.music:
        dictionaries.MEDIA['greetings'].play(-1)

    functions.generate_level(True)
    functions.generate_clouds()

    dt = public.clock.tick(public.FPS) / 1000
    cover_alpha = 0
    cover_surf = pygame.Surface((public.SWIDTH, public.SHEIGHT))
    cover_surf.set_alpha(cover_alpha)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    public.player.jump()

                elif event.key == pygame.K_SPACE:
                    public.player.flip()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] and not (public.player.died or public.player.won):

            public.player.move('right')

        elif keys[pygame.K_a] and not (public.player.died or public.player.won):

            public.player.move('left')

        else:
            public.player.accelerating = False

        if public.player.won and cover_alpha != 255:
            cover_alpha += 1
            cover_surf.set_alpha(cover_alpha)

            if cover_alpha == 255:
                end('A GAME BY TEAM-ABSTRACTANDROID')
                return 0

        if public.level == public.level_max:
            end('More levels to come soon!')
            return 0

        public.all_sprites.update()

        sorted_sprites = sorted(
            public.all_sprites.sprites(), key=lambda x: x.layer)

        public.screen.fill([public.bg_type] * 3)

        for sprite in sorted_sprites:
            sprite.draw()

        public.screen.blit(cover_surf, (0, 0))

        pygame.display.flip()
        public.clock.tick(public.FPS)


def end(msg):
    text_alpha = 0
    credits_text = public.FONT_LG.render(
        msg, False, [public.WHITE] * 3)
    credits_text.set_alpha(text_alpha)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 0

        if text_alpha != 255:
            text_alpha += 5
            credits_text.set_alpha(text_alpha)

        public.screen.fill([public.BLACK] * 3)

        public.screen.blit(credits_text, functions.center(credits_text))

        pygame.display.flip()
        public.clock.tick(public.FPS)

# :^)
