import os
from pygame.locals import *
from Bird import *
from Pipe import *
from NEAT.NeuralNetwork import *
from NEAT.InnovationNumber import *
from NEAT.Evaluator import *
from NEAT.NodeGenome import *
from NEAT.NodeType import *
from NEAT.ConnectionGenome import *


class Game:
    def __init__(self):
        self.bird = Bird()
        self.pipes = [Pipe(800), Pipe(1200), Pipe(1600)]
        self.bestFitness = 0

        self.genome = Genome()
        self.nodeInnovationNo = InnovationNumber()
        self.connectionInnovationNo = InnovationNumber()
        self.initGenome()

        self.evaluator = Evaluator(10, self.genome, self.nodeInnovationNo, self.connectionInnovationNo)

    def initGenome(self):
        n1 = NodeGenome(NodeType.INPUT, self.nodeInnovationNo.getInnovationNo())
        n2 = NodeGenome(NodeType.INPUT, self.nodeInnovationNo.getInnovationNo())
        n3 = NodeGenome(NodeType.INPUT, self.nodeInnovationNo.getInnovationNo())
        n4 = NodeGenome(NodeType.OUTPUT, self.nodeInnovationNo.getInnovationNo())

        self.genome.addNode(n1)
        self.genome.addNode(n2)
        self.genome.addNode(n3)
        self.genome.addNode(n4)

        self.genome.addConnection(
            ConnectionGenome(n1.id, n4.id, random.random() * 4 - 2, True, self.connectionInnovationNo.getInnovationNo()))
        self.genome.addConnection(
            ConnectionGenome(n2.id, n4.id, random.random() * 4 - 2, True, self.connectionInnovationNo.getInnovationNo()))
        self.genome.addConnection(
            ConnectionGenome(n3.id, n4.id, random.random() * 4 - 2, True, self.connectionInnovationNo.getInnovationNo()))

    def display(self, screen):
        for pipe in self.pipes:
            pygame.draw.rect(screen, (255, 255, 255), pipe.pipeTop, 0)
            pygame.draw.rect(screen, (255, 255, 255), pipe.pipeBottom, 0)
        for bird in self.evaluator.birds:
            if not bird.dead:
                pygame.draw.circle(screen, (255, 255, 255), bird.pos, bird.radius, 1)
            else:
                pygame.draw.circle(screen, (255, 0, 0), bird.pos, bird.radius, 1)

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
        for pipe in self.pipes:
            pipe.update()
        for i in range(self.evaluator.populationSize):
            bird = self.evaluator.birds[i]
            bird.update()
            bird.update_sees(self.getLeftmostPipe())
            bird.checkCollision(self.pipes)

            neuralnetwork = NeuralNetwork(self.evaluator.population[i])
            if neuralnetwork.feedForward(bird.sees)[0] > 0.75:
                bird.jump()

        # Check if they're all dead
        dead = True
        for bird in self.evaluator.birds:
            dead = dead and bird.dead

        if dead:
            self.evaluator.evaluate()
            self.reset()

    def reset(self):
        self.pipes = [Pipe(800), Pipe(1200), Pipe(1600)]


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
