from dataset import *
from sys import *
import subprocess

env = {}

for k in argv[1:]:
        tmp = k.split("=")
        env.update({tmp[0]:tmp[1]})

if 'files' in env:
	net = subprocess.check_output (env['files'] , shell=True)
	rocfiles = net.strip().split('\n')

if 'file' in env:
	f = open(env['file'])
	lines = f.readlines()
	f.close()
	X = float64([i.strip().split()[0] for i in lines])
	Y = float64([i.strip().split()[1] for i in lines])


	drawROC("aa", list(X),list(Y))
	exit()

g_x = linspace(0.0,1.0, 10000)
g_y = linspace(0.0,1.0, 10000)

plt.close('all')
p, (ax1) = plt.subplots(1)
ax1.grid(True)
ax1.plot(g_x, g_y, '--b', label="Guideline")
ax1.set_xscale('log')
ls = ['-','--','.-']
index = 0;
for file_name in rocfiles:
	print file_name
	fd = open(file_name)
	lines = fd.readlines()
	fd.close()
	f = float64([i.strip().split()[0] for i in lines])
	d = float64([i.strip().split()[1] for i in lines])
	err = 0.0
	roc_x = []
	roc_y = []
	auc = 0.0
        roc_x, roc_y, auc, fap = roc(list(f),list(d))
	ax1.plot(roc_x, roc_y, ls[index/7], linewidth=2, label=file_name+"(AUC: %f / FAP 0.1%% : %2.2f%%)"%(auc, fap*100.0))
	index = index + 1
plt.xlabel('False Alarm Probability')
plt.ylabel('Efficiency')
plt.legend(loc=0, prop={'size':8})
plt.show()


