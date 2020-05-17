from os.path import dirname, basename, isfile, join
import glob

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = ['CONFIG', 'ConnectionGenome', 'Evaluator', 'Genome', 'GenomeFitnessPair', 'InnovationNumber', 'NeuralNetwork', 'Neuron', 'NodeGenome', 'NodeType', 'Species']