import numpy as np


class Bird:
    def __init__(self):
        self.pos = np.array([50, 450])
        self.velocity = np.array([0, 0])

    def jump(self):
        self.velocity[1] = max(min(25, self.velocity[1] - 16), -15)

    def update(self):
        self.velocity[1] = max(min(25, self.velocity[1] + 1), -15)
        self.pos += self.velocity
