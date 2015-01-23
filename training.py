from sys import *
from openann import *
from numpy import *
from time import *

env = {}
for k in argv[1:]:
	tmp = k.split("=")
	env.update({tmp[0]:tmp[1]})

network_set = int64(env['network'].split(','))

f = open(env['file'], 'r')

line = f.readline()
input_vector = line.split()

N = int(input_vector[0])
D = int(input_vector[1])
F = int(input_vector[2])

lines = f.readlines()
X = float64([i.strip().split() for i in lines[::2]])
Y = float64([i.strip().split() for i in lines[1::2]])
f.close()

dataset = DataSet(X, Y)

RandomNumberGenerator().seed(0)

net = Net()
net.input_layer(D)

for i in network_set:
	net.fully_connected_layer(i, Activation.LOGISTIC)
net.output_layer(F, Activation.LOGISTIC)
stop_dict = {"maximal_iterations": 4000, "minimal_value_differences" : 1e-4}
lma = LMA(stop_dict)
lma.optimize(net, dataset)
net.save("tmp.net")

err = 0.0
for n in range(N):
	err = ((Y[n] - net.predict(X[n]))**2).mean()
print err

