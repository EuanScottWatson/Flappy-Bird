import numpy as np
import math


class Bird:
    def __init__(self):
        self.pos = np.array([50, 450])
        self.velocity = np.array([0, 0])
        self.radius = 20

    def jump(self):
        self.velocity[1] = max(min(25, self.velocity[1] - 16), -15)

    def update(self):
        self.velocity[1] = max(min(25, self.velocity[1] + 1), -15)
        self.pos += self.velocity

    def checkCollision(self, pipes):
        collided = False
        for pipe in pipes:
            if not collided:
                for i in range(pipe.point[0], pipe.point[0] + 75):
                    if math.hypot(i-self.pos[0], pipe.bottom - self.pos[1]) < self.radius:
                        collided = True
                        break

            if not collided:
                for i in range(pipe.bottom):
                    if math.hypot(pipe.point[0] - self.pos[0], i - self.pos[1]) < self.radius:
                        collided = True
                        break

            if not collided:
                for i in range(pipe.point[0], pipe.point[0] + 75):
                    if math.hypot(i - self.pos[0], pipe.bottom + 150 - self.pos[1]) < self.radius:
                        collided = True
                        break

            if not collided:
                for i in range(pipe.bottom + 150, 900):
                    if math.hypot(pipe.point[0] - self.pos[0], i - self.pos[1]) < self.radius:
                        collided = True
                        break

        if collided:
            print("Dead")

