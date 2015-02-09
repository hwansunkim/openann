from dataset import *
from sys import *

env = {}

for k in argv[1:]:
	tmp = k.split("=")
	env.update({tmp[0]:tmp[1]})

a,b,c,x,y = openAnnfile(env['file'])

net = Net()
net.load(env['network'])

f = []
d = list(y)

for n in range(a):
    f += [net.predict(x[n])[0][0]]
    err = ((y[n] - net.predict(x[n]))**2).mean()

drawROC(env['network'].split('.net')[0],f,d)

