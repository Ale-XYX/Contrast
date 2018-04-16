import pygame
import public
import sprites

splitter = sprites.Splitter()

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1
            elif event.type == pygame.KEYDOWN:
                pass

        # Logic
        public.all_sprites.update()

        # Draw
        public.screen.fill(public.BLACK)

        for sprite in public.all_sprites:
            sprite.draw()

        pygame.display.flip()
        public.clock.tick(public.FPS)
