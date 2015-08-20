#!/usr/bin/python
from sys import *
from dataset import *


env = {}
for k in argv[1:]:
	tmp = k.split("=")
	env.update({tmp[0]:tmp[1]})

N,D,F,X,Y = openAnnfile(env['file'])

tab = int64(env['tab'])
ch = int64(env['ch'])
ax = ()
plt.close('all')

f, ax = plt.subplots(4)

for i in range(4):
	for j in range(ch):
		print tab+i*ch+j
		ax[i].plot(X[::,tab+i*ch+j:tab+i*ch+j+1])

plt.show()

