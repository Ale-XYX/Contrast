import bz2
import pygame
import public
import sprites
import functions
import dictionaries
import random


def title():
    pygame.display.set_caption('Contrast')
    pygame.display.set_icon(pygame.image.fromstring(bz2.decompress(
        dictionaries.MEDIA['icon']), (32, 32), 'RGBA'))

    info_text = public.FONT_LG.render(
        'ENTER TO BEGIN', False, [public.WHITE] * 3)

    debug_keys = [ # Maybe theres a way to streamline this?
        pygame.K_k, pygame.K_e, pygame.K_i,
        pygame.K_n, pygame.K_m, pygame.K_u,
        pygame.K_s, pygame.K_c, pygame.K_l,
        pygame.K_v, pygame.K_g, pygame.K_b,
        pygame.K_d, pygame.K_a, pygame.K_1,
        pygame.K_2, pygame.K_3, pygame.K_4,
        pygame.K_5, pygame.K_6, pygame.K_7,
        pygame.K_8, pygame.K_9, pygame.K_0
    ]

    debugging = False
    debug_count = 0
    debug_respond = (
        'K,E,I,N,M,U,S,C,L,V,G,B,D,A,1,2,3,4,5,6,7,8,9,0'.split(',')
    )
    debug_code = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

            elif event.type == pygame.KEYDOWN:

                if event.key in debug_keys and debugging:
                    k = debug_respond[debug_keys.index(event.key)]
                    debug_code.append(k)
                    pygame.display.set_caption(''.join(debug_code))

                elif event.key == pygame.K_SPACE:
                    debug_count += 1

                    if debug_count == 5:
                        pygame.display.set_caption('Real Debug Hours')
                        debugging = True

                elif event.key == pygame.K_BACKSPACE:
                    del debug_code[-1]
                    pygame.display.set_caption(''.join(debug_code))

                elif event.key == pygame.K_RETURN:
                    if debugging:
                        debug_code = ''.join(debug_code)

                        if 'KEINEMUSIK' in debug_code:
                            public.music = False

                        if 'CLEVEL' in debug_code:
                            public.level = int(''.join(list(filter(str.isdigit, debug_code))))

                        pygame.display.set_caption('Contrast')

                    game()
                    return 0

        public.screen.fill([public.BLACK] * 3)

        public.screen.blit(dictionaries.IMAGES['Logo'], functions.center(
            dictionaries.IMAGES['Logo']))
        public.screen.blit(info_text,
                           (functions.center(info_text)[0], 290))

        pygame.display.flip()
        public.clock.tick(public.FPS)


def about():
    return 0


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

        if keys[pygame.K_d] and not public.player.died and \
                not public.player.won:

            if public.player.vel.x < 0.04:
                public.player.pos.x += 1

            public.player.vel.x += 0.1
            public.player.accelerating = True
            public.player.flipped_horizontal = 0

        elif keys[pygame.K_a] and not public.player.died and \
                not public.player.won:

            public.player.vel.x -= 0.1
            public.player.accelerating = True
            public.player.flipped_horizontal = 1

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
