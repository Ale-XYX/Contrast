import pygame
import public
import sprites
import functions


def main():
    player = functions.generate_level()
    splitter = sprites.Splitter()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if player.on_ground:
                        player.vel.y = -3
                        player.on_ground = False

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
        player.vel.x *= 0.90

        public.all_sprites.update()

        # Draw
        public.screen.fill(public.BLACK)

        for sprite in public.all_sprites:
            sprite.draw()

        pygame.display.flip()
        public.clock.tick(public.FPS)
