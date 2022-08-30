
# TODO: make "run" method


import random
#from scipy.stats import truncnorm
#import numpy as np


#def truncated_normal(mean=0, sd=1, low=0, upp=10):
    #return truncnorm((low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)


nRobots = 0
layers = 3
nodes = 16
inputs = 5
outputs = 5
robots = {}

#def sigmoid(x):
    #return 1 / (1 * np.exp(-x))

class robot:

    def __init__(self, fitness, weights, biases, delete):
        self.fitness = fitness
        self.weights = weights
        self.biases = biases
        self.delete = delete


    def Calculate(self, pX, pY, pRotation, speed, asteroids):
        pass
        
        #for w in weights:
            #wsplit = w.split('-')
            #if wsplit[3] == '1':
            





        #return forward, back, right, left, shoot


    def setRand(self):
        for i in range(inputs):
            for n in range(nodes):
                if random.choice([0,1]) == 0:
                    self.weights['w-In-{}-{}-{}'.format(i, 1, n)] = round(random.uniform(-1, 1), 3)

        for l in range(layers-1):
            for i in range(nodes):
                for n in range(nodes):
                    self.weights['w-{}-{}-{}-{}'.format(l + 1, i, l + 2, n)] = round(random.uniform(-1, 1), 3)

        for n in range(nodes):
            for o in range(outputs):
                self.weights['w-{}-{}-Out-{}'.format(layers, n, o)] = round(random.uniform(-1, 1), 3)

        for l in range(layers):
            for n in range(nodes):
                self.biases['node-{}-{}'.format(l, n)] = round(random.uniform(0, 1), 3)


    def evolve(self):

        for w in self.weights:
            w += round(random.uniform(-0.1, 0.1), 3)
            if w > 1:
                w = 1
            if w < -1:
                w = -1

        for b in self.biases:
            b += round(random.uniform(-0.1, 0.1), 3)
            if b > 1:
                b = 1
            if b < 0:
                b = 0
        createRobot(obs=[self.weights, self.biases])

        self.delete = True


def createRobot(obs=None):

    if obs is None:
        robo = robot(0, {}, {}, False)
        robo.setRand()
        robots['rob{}'.format(nRobots)] = robo

    else:
        weights = obs[0]
        biases = obs[1]
        nWeights = {}
        nBiases = {}
        for w in weights:
            nWeights[w] = weights[w]
        for b in biases:
            nBiases[b] = biases[b]

        robo = robot(0, nWeights, nBiases, False)
        robots['rob{}'.format(nRobots)] = robo
    nRobots += 1



class NeuralNetwork:

    def __init__(self, IN_Nodes, H1_Nodes, H2_Nodes, H3_Nodes, OUT_Nodes, Learning_Rate):
        self.IN_Nodes = IN_Nodes
        self.H1_Nodes = H1_Nodes
        self.H2_Nodes = H2_Nodes
        self.H3_Nodes = H3_Nodes
        self.OUT_Nodes = OUT_Nodes
        self.Learning_Rate = Learning_Rate
        self.create_weight_matrices()

    def create_weight_matrices(self):
        """ A method to initialize the weight matrices of the neural network"""
        rad = 1 / np.sqrt(self.IN_Nodes)
        X = truncated_normal(mean=0, sd=1, low=-rad, upp=rad)
        self.weights_in_hidden1 = X.rvs((self.H1_Nodes, self.IN_Nodes))

        rad = 1 / np.sqrt(self.H1_Nodes)
        X = truncated_normal(mean=0, sd=1, low=-rad, upp=rad)
        self.weights_hidden1_hidden2 = X.rvs((self.H2_Nodes, self.H1_Nodes))

        rad = 1 / np.sqrt(self.H2_Nodes)
        X = truncated_normal(mean=0, sd=1, low=-rad, upp=rad)
        self.weights_hidden2_hidden3 = X.rvs((self.H3_Nodes, self.H2_Nodes))

        rad = 1 / np.sqrt(self.H3_Nodes)
        X = truncated_normal(mean=0, sd=1, low=-rad, upp=rad)
        self.weights_hidden_out = X.rvs((self.OUT_Nodes, self.H3_Nodes))

    def run(self, input_vector):
        """
        running the network with an input vector input_vector.
        input_vector can be tuple, list or ndarray
        """

        # turning the input vector into a column vector
        input_vector = np.array(input_vector, ndmin=2).T
        output_vector = np.dot(self.weights_in_hidden1, input_vector)
        output_vector = activation_function(output_vector)

        output_vector = np.dot(self.weights_hidden_out, output_vector)
        output_vector = activation_function(output_vector)

        return output_vector