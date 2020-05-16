import random, pygame
import numpy as np


class Pipe:
    def __init__(self, x):
        self.bottom = random.randint(150, 700)
        self.point = np.array([x, self.bottom])
        self.pipeTop = pygame.Rect(x, 0, 75, self.bottom)
        self.pipeBottom = pygame.Rect(x, self.bottom + 150, 75, 900)

    def update(self):
        self.pipeTop = self.pipeTop.move(-5, 0)
        self.pipeBottom = self.pipeBottom.move(-5, 0)
        self.point += np.array([-5, 0])

        if self.pipeTop.collidepoint(-75, 1):
            self.pipeTop = self.pipeTop.move(1050, 0)
            self.pipeBottom = self.pipeBottom.move(1050, 0)
            self.point = np.array([1050, self.bottom])

