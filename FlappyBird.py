import os
from pygame.locals import *
from Bird import *
from Pipe import *
from NEATt import *


class Game:
    def __init__(self):
        self.bird = Bird()
        self.pipes = [Pipe(800), Pipe(1050), Pipe(1300), Pipe(1550)]
        self.bestFitness = 0

        self.genome = Genome()
        self.nodeInnovationNo = InnovationNumber()
        self.connectionInnovationNo = InnovationNumber()
        self.initGenome()

        self.evaluator = Evaluator(10, self.genome, self.nodeInnovationNo, self.connectionInnovationNo)

    def initGenome(self):
        n1 = NodeGenome(self.nodeInnovationNo.getInnovationNo(), NodeType.INPUT)
        n2 = NodeGenome(self.nodeInnovationNo.getInnovationNo(), NodeType.INPUT)
        n3 = NodeGenome(self.nodeInnovationNo.getInnovationNo(), NodeType.INPUT)
        n4 = NodeGenome(self.nodeInnovationNo.getInnovationNo(), NodeType.INPUT)

        self.genome.addNode(n1)
        self.genome.addNode(n2)
        self.genome.addNode(n3)
        self.genome.addNode(n4)

        self.genome.addConnection(
            ConnectionGenome(n1, n4, random.random() * 4 - 2, True, self.connectionInnovationNo.getInnovationNo()))
        self.genome.addConnection(
            ConnectionGenome(n2, n4, random.random() * 4 - 2, True, self.connectionInnovationNo.getInnovationNo()))
        self.genome.addConnection(
            ConnectionGenome(n3, n4, random.random() * 4 - 2, True, self.connectionInnovationNo.getInnovationNo()))

    def display(self, screen):
        for pipe in self.pipes:
            pygame.draw.rect(screen, (255, 255, 255), pipe.pipeTop, 0)
            pygame.draw.rect(screen, (255, 255, 255), pipe.pipeBottom, 0)
        if not self.bird.dead:
            pygame.draw.circle(screen, (255, 255, 255), self.bird.pos, self.bird.radius, 1)
        else:
            pygame.draw.circle(screen, (255, 0, 0), self.bird.pos, self.bird.radius, 1)

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

    def getLeftmostPipe(self):
        pipeDict = dict((pipe.point[0], pipe) for pipe in self.pipes)
        leftMost = min(pipeDict.items(), key=lambda x: x[0])[1]

        if leftMost.passedBird:
            leftMost = self.pipes[(self.pipes.index(leftMost) + 1) % 4]

        return leftMost

    def run_logic(self):
        self.bird.update()
        self.bird.update_sees(self.getLeftmostPipe())

        if not self.bird.dead:
            for pipe in self.pipes:
                pipe.update()
            self.bird.checkCollision(self.pipes)

        if self.bird.died:
            self.reset()

        self.getLeftmostPipe()

    def reset(self):
        self.bestFitness = max(self.bestFitness, self.bird.fitness)
        self.bird = Bird()
        self.pipes = [Pipe(800), Pipe(1050), Pipe(1300), Pipe(1550)]
        print(self.bestFitness)


def main():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Flappy Bird")

    os.environ['SDL_VIDEO_CENTERED'] = "True"

    width, height = 800, 900

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
