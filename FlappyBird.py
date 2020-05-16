import pygame, os
from pygame.locals import *
from Bird import *


class Game:
    def __init__(self):
        self.bird = Bird()

    def display(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.bird.pos, 20, 1)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return True
                if event.key == K_SPACE:
                    self.bird.jump()

    def display_screen(self, screen):
        screen.fill((0, 0, 0))

        self.display(screen)

        pygame.display.update()
        pygame.display.flip()

    def run_logic(self):
        self.bird.update()


def main():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Flappy Bird")

    os.environ['SDL_VIDEO_CENTERED'] = "True"

    width, height = 600, 900

    screen = pygame.display.set_mode((width, height))

    done = False
    clock = pygame.time.Clock()
    game = Game()

    while not done:
        done = game.events()
        game.run_logic()
        game.display_screen(screen)

        clock.tick(24)


if __name__ == "__main__":
    main()
