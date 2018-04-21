import os
import sys
import pygame
import public
import sprites
import functions

pygame.display.set_caption('Contrast')
pygame.display.set_icon(pygame.image.load(os.path.join(os.path.dirname(__file__), 'res', 'icon.png')))
functions.generate_clouds()


def title():
    keytext = public.FONTS['BigBoi'].render('ENTER TO BEGIN; ? FOR CREDITS', False, (255, 255, 255))
    img = pygame.image.load(os.path.join(os.path.dirname(__file__), 'res', 'credits.png'))
    logo = pygame.image.load(os.path.join(os.path.dirname(__file__), 'res', 'logo.png'))
    credits = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 1
                elif event.key == pygame.K_RETURN:
                    main()
                    return 1
                elif event.key == pygame.K_SLASH:
                    if credits:
                        credits = False
                    elif not credits:
                        credits = True

        public.screen.fill(public.BLACK)

        if not credits:
            public.screen.blit(keytext, ((public.SWIDTH / 2) - keytext.get_width() // 2, 290))
            public.screen.blit(logo, ((public.SWIDTH / 2) - logo.get_width() // 2, ((public.SHEIGHT / 2) - logo.get_height() // 2)))
        elif credits:
            public.screen.blit(img, ((public.SWIDTH / 2) - img.get_width() // 2, ((public.SHEIGHT / 2) - img.get_height() // 2)))

        pygame.display.flip()
        public.clock.tick(60)


def main():
    functions.generate_level(True)
    flip = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'res', 'switch.wav'))
    denied = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'res', 'disallowed.wav'))
    dt = public.clock.tick(60) / 1000
    cooldown = 0
    breakables = []
    pad = pygame.image.load(os.path.join(os.path.dirname(__file__), 'res', 'padding.png'))

    strack = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'res', 'soundtrack.wav'))
    wtrack = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'res', 'wtrack.wav'))
    strack.play(-1)
    v = True
    a = 0
    s = pygame.Surface((800, 483), pygame.SRCALPHA)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and not public.player.died and not public.won:
                    if public.player.on_ground:
                        public.player.jump.play()
                        public.player.vel.y = -3
                        public.player.on_ground = False

                elif event.key == pygame.K_SPACE and cooldown <= 0 and not public.player.died and not public.won:
                    inside = False

                    for sprite in public.blocks:
                        if sprite.rect.collidepoint(public.player.rect.center):
                            inside = True

                    if not inside:
                        flip.play()
                        if public.background[0] == 0:
                            public.background = (255, 255, 255)
                        elif public.background[0] == 255:
                            public.background = (0, 0, 0)
                        cooldown = 1
                    else:
                        denied.play()
                        cooldown = 1

        # Logic
        key = pygame.key.get_pressed()

        if key[pygame.K_d] and not public.player.died and not public.won:
            public.player.vel.x += 0.1
            public.player.anim_type = 1
            public.player.direction = 'Right'

        elif key[pygame.K_a] and not public.player.died and not public.won:
            public.player.vel.x -= 0.1
            public.player.anim_type = 1
            public.player.direction = 'Left'

        elif public.player.anim_type != 4 and public.player.anim_type != 5:
            public.player.anim_type = 0

        public.player.vel.x = functions.clamp(public.player.vel.x, -10.0, 10.0)
        public.player.pos.x += public.player.vel.x
        public.player.vel.x *= 0.93

        if cooldown >= 0:
            cooldown = cooldown - dt

        if len(public.player.groups()) == 0:
            public.player = sprites.Player(public.spawn, public.all_sprites)

        if public.level == 14 and v:
            strack.stop()
            wtrack.play(-1)
            v = False
        if public.won:
            if a != 255:
                a += 1
            elif a == 255:
                end()
                return 1

        public.all_sprites.update()
        functions.update_clouds()

        # Draw
        public.screen.fill(public.background)

        for sprite in public.breakables:
            sprite.draw()

        for sprite in public.clouds:
            sprite.draw()

        for sprite in public.all_sprites:
            if sprite.type == 'Breakable':
                public.breakables.append(sprite)

            if sprite.type != 'Player' or sprite.type != 'Title':
                sprite.draw()

        public.player.draw()

        for sprite in public.text:
            sprite.draw()

        if public.padding:
            public.screen.blit(pad, (0, 0))

        s.fill((0, 0, 0, a))
        public.screen.blit(s, (0, 0))


        pygame.display.flip()
        public.clock.tick(public.FPS)


def end():
    a = 0
    txt = public.FONTS['BigBoi'].render('A Game By TEAM-ABSTRACTANDROID', False, (a, a, a))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if a != 255:
            a += 5
        txt = public.FONTS['BigBoi'].render('A Game By TEAM-ABSTRACTANDROID', False, (a, a, a))

        public.screen.fill(public.BLACK)

        public.screen.blit(txt, ((public.SWIDTH / 2) - txt.get_width() // 2, ((public.SHEIGHT / 2) - txt.get_height() // 2)))
        pygame.display.flip()
        public.clock.tick(60)