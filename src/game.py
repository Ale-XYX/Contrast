import os
import pygame
import public
import sprites
import functions

pygame.display.set_caption('Contrast')
pygame.mixer.pre_init(44100,-16,2, 1024*4)


def main():
    functions.generate_clouds()
    entrance = functions.generate_level()
    player = sprites.Player(public.spawn, public.all_sprites)
    splitter = sprites.Splitter()
    pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'res', 'soundtrack.wav')).play(-1)

    dt = public.clock.tick(60) / 1000
    cooldown = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if player.on_ground:
                        player.vel.y = -3
                        player.on_ground = False

                elif event.key == pygame.K_e and cooldown <= 0:
                    inside = False

                    for sprite in public.blocks:
                        if sprite.rect.collidepoint(player.rect.center):
                            inside = True

                    if not inside:
                        if public.background[0] == 0:
                            public.background = (255, 255, 255)
                        elif public.background[0] == 255:
                            public.background = (0, 0, 0)
                        cooldown = 2

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
