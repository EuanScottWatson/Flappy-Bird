import random
from NEAT.CONFIG import *
from NEAT.NodeType import *
from NEAT.ConnectionGenome import *
from NEAT.NodeGenome import *


def crossover(parent1, parent2):
    child = Genome()

    for node in parent1.nodes.values():
        child.addNode(node)

    for p1Connection in parent1.connections.values():
        if p1Connection.innovationNo in parent2.connections.keys():
            childConnection = p1Connection.copy() if bool(random.getrandbits(1)) else parent2.connections[
                p1Connection.innovationNo]
            child.addConnection(childConnection)
        else:
            child.addConnection(p1Connection.copy)

    return child


def getAverageWeightDifference(g1, g2):
    matchingGenes = 0
    weightDifference = 0

    connectionOneKeys = list(g1.connections.keys())
    connectionOneKeys.sort()
    connectionTwoKeys = list(g2.connections.keys())
    connectionTwoKeys.sort()
    highestInnovation = max(connectionOneKeys[-1], connectionTwoKeys[-1])

    for i in range(0, highestInnovation + 1):
        if i in g1.connections.keys() and i in g2.connections.keys():
            matchingGenes += 1
            weightDifference += abs(g1.connections[i].weight - g2.connections[i].weight)

    return weightDifference / matchingGenes


def getExcessDisjointConnections(g1, g2, count, i, b1, b2):
    if (i in g1.connections.keys()) and (i in g2.connections.keys()):
        if g1.connections[i] is None and b1 and g2.connections[i] is not None:
            count += 1
        elif g2.connections[i] is None and b2 and g1.connections[i] is not None:
            count += 1

    return count


def getDisjointExcessNodes(g1, g2, count, i, b1, b2):
    if (i in g1.nodes.keys()) and (i in g2.nodes.keys()):
        if g1.nodes[i] is None and b1 and g2.nodes[i] is not None:
            count += 1
        elif g2.nodes[i] is None and b2 and g1.nodes[i] is not None:
            count += 1

    return count


def countExcessDisjoint(genome1, genome2):
    excessGenes = 0
    disjointGenes = 0

    nodeOneKeys = list(genome1.nodes.keys())
    nodeOneKeys.sort()
    nodeTwoKeys = list(genome2.nodes.keys())
    nodeTwoKeys.sort()
    highestInnovation = max(nodeOneKeys[-1], nodeTwoKeys[-1])

    for i in range(0, highestInnovation + 1):
        excessGenes = getDisjointExcessNodes(genome1, genome2, excessGenes, i, nodeOneKeys[-1] < i,
                                             nodeTwoKeys[-1] < i)
        disjointGenes = getDisjointExcessNodes(genome1, genome2, disjointGenes, i, nodeOneKeys[-1] > i,
                                               nodeTwoKeys[-1] > i)

    connectionOneKeys = list(genome1.connections.keys())
    connectionOneKeys.sort()
    connectionTwoKeys = list(genome2.connections.keys())
    connectionTwoKeys.sort()
    highestInnovation = max(connectionOneKeys[-1], connectionTwoKeys[-1])

    for i in range(0, highestInnovation + 1):
        excessGenes = getExcessDisjointConnections(genome1, genome2, excessGenes, i, connectionOneKeys[1] < i,
                                                   connectionTwoKeys[-1] < i)
        disjointGenes = getExcessDisjointConnections(genome1, genome2, disjointGenes, i,
                                                     connectionOneKeys[1] > i, connectionTwoKeys[-1] > i)

    return [excessGenes, disjointGenes]


def compatibilityDistance(genome1, genome2, c1, c2, c3):
    excessDisjoint = countExcessDisjoint(genome1, genome2)
    avWeightDifference = getAverageWeightDifference(genome1, genome2)
    return c1 * excessDisjoint[0] + c2 * excessDisjoint[1] + c3 * avWeightDifference


class Genome:
    def __init__(self, starter=None):
        self.nodes = {}
        self.connections = {}
        self.config = Configuration()

        if starter:
            for i in starter.nodes.keys():
                self.nodes[i] = starter.nodes[i].copy()

            for i in starter.connections.keys():
                self.connections[i] = starter.connections[i].copy()

    def addNode(self, node):
        self.nodes[node.id] = node

    def addConnection(self, connection):
        self.connections[connection.innovationNo] = connection

    def mutation(self):
        for connection in self.connections.values():
            if random.random() < self.config.MUTATION_THRESHOLD:
                connection.setWeight(connection.weight * (random.random() * 4 - 2))
            else:
                connection.setWeight(random.random() * 4 - 2)

    def newConnectionMutation(self, connectionInnovation):
        keys = self.nodes.keys()
        node1 = self.nodes.get(random.choice(list(keys)))
        node2 = self.nodes.get(random.choice(list(keys)))

        weight = random.random() * 4 - 2

        if (node1.type == NodeType.HIDDEN and node2.type == NodeType.INPUT) or (
                node1.type == NodeType.OUTPUT and node2.type == NodeType.HIDDEN) or (
                node1.type == NodeType.OUTPUT and node2.type == NodeType.INPUT):
            node1, node2 = node2, node1

        if node1.type != node2.type:
            exists = False
            for connection in self.connections.values():
                if connection.inputNode == node1.id and connection.outputNode == node2.id:
                    exists = True
                    break

            if not exists:
                newConnection = ConnectionGenome(node1.id, node2.id, weight, True,
                                                 connectionInnovation.getInnovationNo())
                self.connections[newConnection.innovationNo] = newConnection

    def newNodeMutation(self, connectionInnovation, nodeInnovation):
        keys = self.connections.keys()
        connection = self.connections[random.choice(list(keys))]
        connection.disable()

        node1 = self.nodes[connection.inputNode]
        node2 = self.nodes[connection.outputNode]
        newNode = NodeGenome(NodeType.HIDDEN, nodeInnovation.getInnovationNo())

        connection1 = ConnectionGenome(node1.id, newNode.id, 1, True, connectionInnovation.getInnovationNo())
        connection2 = ConnectionGenome(newNode.id, node2.id, connection.weight, True,
                                       connectionInnovation.getInnovationNo())

        self.nodes[newNode.id] = newNode
        self.connections[connection1.innovationNo] = connection1
        self.connections[connection2.innovationNo] = connection2

    def print(self):
        for n in self.nodes.values():
            print(n.id)

        for c in self.connections.values():
            print("\nInnovation: ", c.innovationNo)
            print("Conneciton: ", c.inputNode.id, "->", c.outputNode.id)
            print("Enabled: ", c.active)
            print("Weight: ", c.weight)
