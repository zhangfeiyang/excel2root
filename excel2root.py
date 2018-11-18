#!/usr/bin/env python
from ROOT import *

from array import array
N = 2502
def list_from_excel(filename):
	
	file = open(filename,'r')
	lines = file.readlines()
	
	time = []
	app = []

	N = len(lines)
	for i in range(5,N):
		time.append(float(lines[i].split(',')[0]))
		app.append(float(lines[i].split(',')[1].strip('\n')))
	return time,app

def get_peak(times,apps):
    
    mini_app = min(apps)
    mini_index = apps.index(mini_app)

    return mini_app,mini_index

def get_baseline(times,apps):
    
    peak,index = get_peak(times,apps)
    
    baseline = 0
    conts = 0
    for i in range(0,int(index/2)) + range(int((index+N)/2),N-1):
        conts += 1
        baseline += apps[i]

    baseline /= conts
    return baseline

def get_area(times,apps,baseline):
	
        area = 0
        mini_app,mini_index = get_peak(times,apps)

	for i in range(mini_index-50,min(mini_index+100,N)):
		area += apps[i] - baseline
	return area

def treeFill(tree,dirname,fileid,time2,time3,time4,app2,app3,app4,area2,area3,area4,baseline2,baseline3,baseline4):

	times,apps = list_from_excel(dirname+'/C2Trace'+fileid+'.csv')
	N = len(times)
	for i in range(N):
		time2[i] = times[i]
		app2[i] = apps[i]
        baseline2[0] = get_baseline(times,apps)
	area2[0] = get_area(times,apps,baseline2[0])

	times,apps = list_from_excel(dirname+'/C3Trace'+fileid+'.csv')
	N = len(times)
	for i in range(N):
		time3[i] = times[i]
		app3[i] = apps[i]
        baseline3[0] = get_baseline(times,apps)
	area3[0] = get_area(times,apps,baseline3[0])

	times,apps = list_from_excel(dirname+'/C4Trace'+fileid+'.csv')
	N = len(times)
	for i in range(N):
		time4[i] = times[i]
                apps[i] = -apps[i]
		app4[i] = apps[i]
        baseline4[0] = get_baseline(times,apps)
	area4[0] = get_area(times,apps,baseline4[0])

	tree.Fill()
	
def dir2root(dirname):
	
	time2 = array('d',N*[0])
	app2 = array('d', N*[0])
	area2 = array('d',[0])
	baseline2 = array('d',[0])

	time3 = array('d',N*[0])
	app3 = array('d', N*[0])
	area3 = array('d',[0])
	baseline3 = array('d',[0])

	time4 = array('d',N*[0])
	app4 = array('d', N*[0])
	area4 = array('d',[0])
	baseline4 = array('d',[0])

	file = TFile(dirname+'.root','recreate')
	
	tree = TTree('tree','')

	tree.Branch('time2',time2,'time2['+str(N)+']/D')
	tree.Branch('app2',app2,'app2['+str(N)+']/D')
	tree.Branch('area2',area2,'area2/D')
	tree.Branch('baseline2',baseline2,'baseline2/D')

	tree.Branch('time3',time3,'time3['+str(N)+']/D')
	tree.Branch('app3',app3,'app3['+str(N)+']/D')
	tree.Branch('area3',area3,'area3/D')
	tree.Branch('baseline3',baseline3,'baseline3/D')

	tree.Branch('time4',time4,'time4['+str(N)+']/D')
	tree.Branch('app4',app4,'app4['+str(N)+']/D')
	tree.Branch('area4',area4,'area4/D')
	tree.Branch('baseline4',baseline4,'baseline4/D')

	import os
	filenames =  os.listdir(dirname)
	filenames = filter(lambda x:'C4' in x,filenames)
	
	for filename in filenames:
		fileid = filename[7:12]	
		treeFill(tree,dirname,fileid,time2,time3,time4,app2,app3,app4,area2,area3,area4,baseline2,baseline3,baseline4)			


	tree.Write()	

	file.Close()
	
if __name__ == '__main__':
	
	import sys
	dirname = sys.argv[1]
	dir2root(dirname)	
