import numpy as np
import math


class Bird:
    def __init__(self):
        self.pos = np.array([50, 450])
        self.velocity = np.array([0, 0])
        self.radius = 20
        self.fitness = 0

        self.dead = False
        self.died = False

        # Sees: [Y velocity, X distance to Pipe, Y change in pipe]
        self.sees = []

    def jump(self):
        if not self.dead:
            self.velocity[1] = max(min(25, self.velocity[1] - 16), -10)

    def update(self):
        if not self.dead:
            self.velocity[1] = max(min(25, self.velocity[1] + 1), -15)
            self.pos += self.velocity
            self.fitness += 0.25
        # else:
        #     self.pos += self.velocity
        #     if self.pos[1] >= 900 - self.radius:
        #         self.died = True
        #     self.velocity[1] = max(min(30, self.velocity[1] + 8), -40)

    def update_sees(self, leftMost):
        self.sees = [self.velocity[1], leftMost.point[0] - self.pos[0], leftMost.point[1] - self.pos[1] + 85]

    def checkPipePass(self, pipes):
        for pipe in pipes:
            if pipe.point[0] + 95 == self.pos[0]:
                self.fitness += 5
                pipe.passedBird = True
                break

    def checkCollision(self, pipes):
        for pipe in pipes:
            if not self.dead:
                for i in range(pipe.point[0], pipe.point[0] + 75):
                    if math.hypot(i - self.pos[0], pipe.bottom - self.pos[1]) < self.radius:
                        self.dead = True
                        break

            if not self.dead:
                for i in range(pipe.bottom):
                    if math.hypot(pipe.point[0] - self.pos[0], i - self.pos[1]) < self.radius:
                        self.dead = True
                        break

            if not self.dead:
                for i in range(pipe.point[0], pipe.point[0] + 75):
                    if math.hypot(i - self.pos[0], pipe.bottom + 150 - self.pos[1]) < self.radius:
                        self.dead = True
                        break

            if not self.dead:
                for i in range(pipe.bottom + 150, 900):
                    if math.hypot(pipe.point[0] - self.pos[0], i - self.pos[1]) < self.radius:
                        self.dead = True
                        break

        if self.pos[1] > 900 or self.pos[1] < 0:
            self.dead = True

        if not self.dead:
            self.checkPipePass(pipes)

        # if self.dead:
        #     self.velocity = np.array([0, -40])

    def makeDecision(self):
        pass
