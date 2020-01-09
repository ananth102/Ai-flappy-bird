from random import random
from random import seed
from math import exp
import copy

# 1 hidden layer 4 now


def create_network(num_inputs, num_nuerons, num_output):
    net = list()
    hidden_layer = []
    for i in range(num_nuerons):
        node = {"weights": []}
        for j in range(num_inputs + 1):
            node["weights"].append(random())
        hidden_layer.append(node)
    net.append(hidden_layer)
    output_layer = []
    for i in range(num_output):
        node = {"weights": []}
        for j in range(num_nuerons + 1):
            node["weights"].append(random())
        output_layer.append(node)
    net = [hidden_layer, output_layer]
    return net


def activation(weights, input):
    sum = weights[-1]  # aka bias
    for i in range(len(weights)-1):
        sum += weights[i] * input[i]
    return 1.0 / (1.0 + exp(-sum))


def forward_prop(net, begin_input):
    inputs = begin_input
    for layer in net:
        new_input = []
        for nueron in layer:
            act = activation(nueron["weights"], inputs)
            new_input.append(act)

        inputs = new_input
    return inputs


# derivitive of sigmoid


def transfer_derivative(output):
    return output * (1.0 - output)


def backprog(network, initial):
    pass


class NN():
    def __init__(self, num_inputs, num_nuerons, num_output, see):
        self.num_inputs = num_inputs
        self.num_nuerons = num_nuerons
        self.num_output = num_output
        seed(see)
        self.net = list()
        hidden_layer = []
        for i in range(num_nuerons):
            node = {"weights": []}
            for j in range(num_inputs + 1):
                node["weights"].append(random())
            hidden_layer.append(node)
        self.net.append(hidden_layer)
        output_layer = []
        for i in range(num_output):
            node = {"weights": []}
            for j in range(num_nuerons + 1):
                node["weights"].append(random())
            output_layer.append(node)
        self.net = [hidden_layer, output_layer]

    def forward_prop(self, begin_input):
        inputs = begin_input
        for layer in self.net:
            new_input = []
            for nueron in layer:
                act = activation(nueron["weights"], inputs)
                new_input.append(act)

            inputs = new_input
        return inputs

    def copyNN(self):
        ne = list()
        hidden_layer = []
        for i in range(self.num_nuerons):
            node = {"weights": []}
            for j in range(self.num_inputs + 1):
                node["weights"].append(self.net[0][i]["weights"][j])
            hidden_layer.append(node)
        ne.append(hidden_layer)
        output_layer = []
        for i in range(self.num_output):
            node = {"weights": []}
            for j in range(self.num_nuerons + 1):
                node["weights"].append(self.net[1][i]["weights"][j])
            output_layer.append(node)
        ne = [hidden_layer, output_layer]
        return [hidden_layer, output_layer]


# seed(1)
net = create_network(2, 1, 2)
# print(net[0][0]["weights"])
woof = [1, 0]
out = forward_prop(net, woof)
print(out)
