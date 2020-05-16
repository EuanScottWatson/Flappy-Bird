import numpy as np
import math


class Bird:
    def __init__(self):
        self.pos = np.array([50, 450])
        self.velocity = np.array([0, 0])
        self.radius = 20
        self.fitness = 0

    def jump(self):
        self.velocity[1] = max(min(25, self.velocity[1] - 16), -15)

    def update(self):
        self.velocity[1] = max(min(25, self.velocity[1] + 1), -15)
        self.pos += self.velocity
        self.fitness += 0.25

    def checkPipePass(self, pipes):
        for pipe in pipes:
            if pipe.point[0] + 95 == self.pos[0]:
                self.fitness += 5
                break

    def checkCollision(self, pipes):
        dead = False
        for pipe in pipes:
            if not dead:
                for i in range(pipe.point[0], pipe.point[0] + 75):
                    if math.hypot(i-self.pos[0], pipe.bottom - self.pos[1]) < self.radius:
                        dead = True
                        break

            if not dead:
                for i in range(pipe.bottom):
                    if math.hypot(pipe.point[0] - self.pos[0], i - self.pos[1]) < self.radius:
                        dead = True
                        break

            if not dead:
                for i in range(pipe.point[0], pipe.point[0] + 75):
                    if math.hypot(i - self.pos[0], pipe.bottom + 150 - self.pos[1]) < self.radius:
                        dead = True
                        break

            if not dead:
                for i in range(pipe.bottom + 150, 900):
                    if math.hypot(pipe.point[0] - self.pos[0], i - self.pos[1]) < self.radius:
                        dead = True
                        break

        if self.pos[1] > 900 or self.pos[1] < 0:
            dead = True

        if not dead:
            self.checkPipePass(pipes)

        return dead

