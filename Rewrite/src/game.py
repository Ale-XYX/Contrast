import pygame
import public
import sprites
import functions
import dictionaries

pygame.display.set_caption('Contrast')
pygame.display.set_icon(dictionaries.MEDIA['icon'])


def title():
    info_text = public.FONT_LG.render(
        'ENTER TO BEGIN; ? FOR CREDITS', False, public.WHITE)
    in_credits = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SLASH:
                    if in_credits:
                        in_credits = False

                    elif not in_credits:
                        in_credits = True

                elif event.key == pygame.K_RETURN:
                    game()
                    return 0

        public.screen.fill(public.BLACK)

        if not in_credits:
            public.screen.blit(dictionaries.MEDIA['logo'], functions.center(
                dictionaries.MEDIA['logo']))
            public.screen.blit(info_text,
                               (functions.center(info_text)[0], 290))

        elif in_credits:
            public.screen.blit(dictionaries.MEDIA['credits'], functions.center(
                dictionaries.MEDIA['credits']))

        pygame.display.flip()
        public.clock.tick(60)


def game():
    dictionaries.MEDIA['greetings'].play(-1)
    functions.generate_level(True)
    functions.generate_clouds()

    dt = public.clock.tick(public.FPS) / 1000
    cooldown = 0
    cover_alpha = 0
    cover_surf = pygame.Surface((public.SWIDTH, public.SHEIGHT))
    cover_surf.set_alpha(cover_alpha)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and public.player.on_ground and \
                        not public.player.died and not public.player.won:
                    dictionaries.MEDIA['jump'].play()
                    public.player.vel.y = -3
                    public.player.on_ground = False

                elif event.key == pygame.K_SPACE and cooldown <= 0 and \
                        not public.player.died and not public.player.won:
                    inside = False

                    for sprite in public.blocks:
                        print(sprite.rect.colliderect(public.player.rect))
                        if sprite.rect.colliderect(public.player.rect):
                            inside = True

                    if not inside:
                        dictionaries.MEDIA['flip'].play()
                        public.bg_type = 0 if public.bg_type == 255 else 255
                        cooldown = 1

                    else:
                        dictionaries.MEDIA['denied'].play()
                        cooldown = 1

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] and not public.player.died and \
                not public.player.won:
            public.player.vel.x += 0.1
            public.player.direction = 'R'
            public.player.accelerating = True

        elif keys[pygame.K_a] and not public.player.died and \
                not public.player.won:
            public.player.vel.x -= 0.1
            public.player.direction = 'L'
            public.player.accelerating = True

        else:
            public.player.accelerating = False

        if cooldown > 0:
            cooldown -= dt

        if public.player.won and cover_alpha != 255:
            cover_alpha += 1
            cover_surf.set_alpha(cover_alpha)

            if cover_alpha == 255:
                end()
                return 0

        public.all_sprites.update()

        sorted_sprites = sorted(
            public.all_sprites.sprites(), key=lambda x: x.layer)

        public.screen.fill([public.bg_type] * 3)

        for sprite in sorted_sprites:
            sprite.draw()

        if public.wrapping: public.screen.blit(dictionaries.MEDIA['wrap_gradient'], (0, 0))
        public.screen.blit(cover_surf, (0, 0))

        pygame.display.flip()
        public.clock.tick(60)


def end():
    text_alpha = 0
    info_text = public.FONT_LG.render(
        'A GAME BY TEAM-ABSTRACTANDROID', False, public.WHITE)
    info_text.set_alpha(text_alpha)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 0

        if text_alpha != 255:
            text_alpha += 5
            info_text.set_alpha(text_alpha)

        public.screen.fill(public.BLACK)

        public.screen.blit(info_text, functions.center(info_text))

        pygame.display.flip()
        public.clock.tick(60)