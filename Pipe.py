import random, pygame


class Pipe:
    def __init__(self, x):
        bottom = random.randint(150, 700)
        self.pipeTop = pygame.Rect(x, 0, 75, bottom)
        self.pipeBottom = pygame.Rect(x, bottom + 150, 75, 900)

    def update(self):
        self.pipeTop = self.pipeTop.move(-5, 0)
        self.pipeBottom = self.pipeBottom.move(-5, 0)

        if self.pipeTop.collidepoint(-75, 1):
            self.pipeTop = self.pipeTop.move(1050, 0)
            self.pipeBottom = self.pipeBottom.move(1050, 0)
