import os
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
                    print(credits)

        public.screen.fill(public.BLACK)

        if not credits:
            public.screen.blit(keytext, ((public.SWIDTH / 2) - keytext.get_width() // 2, 290))
            public.screen.blit(logo, ((public.SWIDTH / 2) - logo.get_width() // 2, ((public.SHEIGHT / 2) - logo.get_height() // 2)))
        elif credits:
            public.screen.blit(img, ((public.SWIDTH / 2) - img.get_width() // 2, ((public.SHEIGHT / 2) - img.get_height() // 2)))

        pygame.display.flip()
        public.clock.tick(60)


def main():
    entrance = functions.generate_level()
    player = sprites.Player(public.spawn, public.all_sprites)
    splitter = sprites.Splitter()
    flip = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'res', 'switch.wav'))
    denied = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'res', 'disallowed.wav'))
    dt = public.clock.tick(60) / 1000
    cooldown = 0

    pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'res', 'soundtrack.wav')).play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if player.on_ground:
                        player.jump.play()
                        player.vel.y = -3
                        player.on_ground = False

                elif event.key == pygame.K_e and cooldown <= 0:
                    inside = False

                    for sprite in public.blocks:
                        if sprite.rect.collidepoint(player.rect.center):
                            inside = True

                    if not inside:
                        flip.play()
                        if public.background[0] == 0:
                            public.background = (255, 255, 255)
                        elif public.background[0] == 255:
                            public.background = (0, 0, 0)
                        cooldown = 2
                    else:
                        denied.play()
                        cooldown = 1

        # Logic
        key = pygame.key.get_pressed()
        if key[pygame.K_d]:
            player.vel.x += 0.1
            player.anim_type = 1
            player.direction = 'Right'

        elif key[pygame.K_a]:
            player.vel.x -= 0.1
            player.anim_type = 1
            player.direction = 'Left'

        else:
            player.anim_type = 0

        player.vel.x = functions.clamp(player.vel.x, -10.0, 10.0)
        player.pos.x += player.vel.x
        player.vel.x *= 0.93

        if cooldown >= 0:
            cooldown = cooldown - dt

        public.all_sprites.update()
        functions.update_clouds()

        # Draw
        public.screen.fill(public.background)

        for sprite in public.clouds:
            sprite.draw()

        for sprite in public.all_sprites:
            if sprite.type != 'Player':
                sprite.draw()

        player.draw()

        pygame.display.flip()
        public.clock.tick(public.FPS)
