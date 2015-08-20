from dataset import *
from sys import *

env = {}

for k in argv[1:]:
	tmp = k.split("=")
	env.update({tmp[0]:tmp[1]})

N,D,F,X,Y = openAnnfile(env['file'])

net = Net()
net.load(env['network'])

f = []
d = list(Y)

for n in range(N):
    f += [net.predict(X[n])[0][0]]
    err = ((Y[n] - net.predict(X[n]))**2).mean()
	
drawROC(env['network'].split('.net')[0],f,d)

