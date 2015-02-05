from sys import *
from openann import *
from numpy import *
from time import *

dropout = False
d_rate = 0.5

env = {}
for k in argv[1:]:
	tmp = k.split("=")
	env.update({tmp[0]:tmp[1]})

network_set = int64(env['network'].split(','))

net_file = "MBSGD"+env['network'].replace(',','_')

if 'dropout' in env:
	dropout = env['dropout'].lower() == 'true'
	net_file += "_dropout_"+env['dropout']

if 'd_rate' in env:
	d_rate = float(env['d_rate'])
	net_file += "_rate" + env['d_rate']

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
net.set_regularization(0.0, 0.01, 0.0)
net.input_layer(D)
if dropout:
	net.dropout_layer(d_rate)

for i in network_set:
	net.fully_connected_layer(i, Activation.RECTIFIER)
	if dropout:
		net.dropout_layer(d_rate)

net.output_layer(F, Activation.SOFTMAX)

start = time()
#stop_dict = {"maximal_iterations": 4000, "minimal_value_differences" : 1e-5}
#lma = LMA(stop_dict)
#lma.optimize(net, dataset)

optimizer = MBSGD({"maximal_iterations": 500}, learning_rate=0.7, learning_rate_decay=0.999, min_learning_rate=0.001, momentum=0.5, batch_size=16)
Log.set_info() # Deactivate debug output
optimizer.optimize(net, dataset)
end = time()
net.save(net_file+".net")

err = (array([Y[n] - net.predict(X[n]) for n in range(N)])**2).sum(axis=-1).mean()
print err, end-start

