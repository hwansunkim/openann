#!/usr/bin/python
from sys import *
from time import *
from dataset import *

dropout = False
rbm_enable = False

d_rate = 0.5
cdN = 1

stop_dict = {"maximal_iterations": 1000, "minimal_value_differences" : 1e-7}

env = {}
for k in argv[1:]:
	tmp = k.split("=")
	env.update({tmp[0]:tmp[1]})

network_set = int64(env['network'].split(','))

net_file = "net20/"+env['file'].split('/')[-1]

if 'dropout' in env:
	dropout = env['dropout'].lower() == 'true'
	net_file += "_dropout_"+env['dropout']

if 'd_rate' in env:
	d_rate = float(env['d_rate'])
	net_file += "_rate" + env['d_rate']

if 'rbm' in env:
	rbm_enable = True
	rbm_network = int64(env['rbm'].split(','))
	net_file = net_file + "RBM" + env['rbm'].replace(',','_')

if 'maxiter' in env:
	stop_dict['maximal_iterations']=int64(env['maxiter']) 

if 'cdN' in env:
	cdN = int64(env['cdN'])
	net_file = net_file + "cdN" + env['cdN']

net_file = net_file + "MLP" + env['network'].replace(',','_')

N,D,F,X,Y = openAnnfile(env['file'])

dataset = DataSet(X, Y)

RandomNumberGenerator().seed(0)

net = Net()
#net.set_regularization(0.0, 0.01, 0.0)
net.input_layer(D)

if rbm_enable:
	for i in rbm_network:
		net.restricted_boltzmann_machine_layer(i, cdN, 0.01)
if dropout:
	net.dropout_layer(d_rate)

for i in network_set:
	net.fully_connected_layer(i, Activation.LOGISTIC)
	if dropout:
		net.dropout_layer(d_rate)

net.output_layer(F, Activation.LOGISTIC)

lma = LMA(stop_dict)
lma.optimize(net, dataset)
#optimizer = MBSGD(stop_dict, learning_rate=0.7, learning_rate_decay=0.999, min_learning_rate=0.001, momentum=0.5, batch_size=16)
Log.set_info() # Deactivate debug output
#optimizer.optimize(net, dataset)
net.save(net_file+"_%d(%f).net"%(stop_dict['maximal_iterations'],stop_dict['minimal_value_differences']))

err = (array([Y[n] - net.predict(X[n]) for n in range(N)])**2).sum(axis=-1).mean()
print err, end-start

