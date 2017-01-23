# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 23:49:35 2017

@author: hugh
"""
import numpy as np
from scipy.misc import imread


def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
    return 1/(1+np.exp(-x))



np.random.seed(1)
thetas = 2*np.random.random(size=(32*32)) -1 #mean 0

actor_A = "hader"   #associate level 1
actor_B = "carell" #associate level 0

batchsize=60
d = {}

X = np.zeros(shape=(batchsize*2, 32*32))
Y = np.zeros(shape=(batchsize*2))
i=0
dirname=".\processed\\"
for filename in os.listdir(dirname):
    if(i>=batchsize*2):
        continue
    actor = filename.split("_")[1]
    if(actor==actor_A or actor==actor_B):    
        im = imread(dirname+filename)
        im = im.flatten()
        X[i]=im        
        if(actor==actor_A):
            Y[i]=1
        else:
            Y[i]=0
        i+=1
for iter in xrange(100000):
    xcpy=X
    predicted = nonlin(np.dot(xcpy, thetas))
    err = Y-predicted
    delta = err*nonlin(predicted, True)
    thetas+=np.dot(xcpy.T, delta)

t = thetas.reshape((32,32))    

xcpy=X
predicted = nonlin(np.dot(xcpy, thetas))
err = Y-predicted
    
        
    