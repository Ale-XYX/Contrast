import pygame
import public
import sprites
import functions


def main():
    functions.generate_level()
    splitter = sprites.Splitter()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    for sprite in public.all_sprites:
                        if sprite.type == 'Player':
                            if sprite.on_ground:
                                sprite.vel.y = -3
                                sprite.on_ground = False

        # Logic
        key = pygame.key.get_pressed()
        if key[pygame.K_d]:
            for sprite in public.all_sprites:
                if sprite.type == 'Player':
                    sprite.vel.x += 0.1
                    break

        if key[pygame.K_a]:
            for sprite in public.all_sprites:
                if sprite.type == 'Player':
                    sprite.vel.x -= 0.1
                    break

        for sprite in public.all_sprites:
            if sprite.type == 'Player':
                sprite.vel.x = functions.clamp(sprite.vel.x, -10.0, 10.0)
                sprite.pos.x += sprite.vel.x
                sprite.vel.x *= 0.95

        public.all_sprites.update()

        # Draw
        public.screen.fill(public.BLACK)

        for sprite in public.all_sprites:
            sprite.draw()

        pygame.display.flip()
        public.clock.tick(public.FPS)
