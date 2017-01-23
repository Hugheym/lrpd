

from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import random
import time
from scipy.misc import imread
from scipy.misc import imresize
import matplotlib.image as mpimg
from scipy.ndimage import filters
import urllib
import os
import json
import cPickle   

LINK_MALE_FILENAME = "link_male_actors.txt"
LINK_FEMALE_FILENAME = "link_female_actors.txt"
IMPORTED_IMAGE_IDS = "imported_ids"
UNPROCESSED__DIR = "uncropped"
if os.name=="nt": #if windows 
    UNPROCESSED__DIR+="\\"
    print UNPROCESSED__DIR
else:
    UNPROCESSED__DIR+="/"


#act = list(set([a.split("\t")[0] for a in open(LINK_FILENAME).readlines()]))
act =['Fran Drescher', 'America Ferrera', 'Kristin Chenoweth', 'Alec Baldwin', 'Bill Hader', 'Steve Carell']

def timeout(func, args=(), kwargs={}, timeout_duration=1, default=None):
    '''From:
    http://code.activestate.com/recipes/473878-timeout-function-using-threading/'''
    import threading
    class InterruptableThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = None

        def run(self):
            try:
                self.result = func(*args, **kwargs)
            except:
                self.result = default

    it = InterruptableThread()
    it.start()
    it.join(timeout_duration)
    if it.isAlive():
        return False
    else:
        return it.result

testfile = urllib.URLopener()            


face_locations = {} #dict of  filename -> (xmin, ymin, xmax, ymax)

def get_bounds(line):
    tokens = line.replace(",", " ").split()
    x1  = tokens[5]
    y1 = tokens[6]
    x2 = tokens[7]
    y2 = tokens[8]
    return (x1, y1, x2, y2)

loaded_already = []

for filename in os.listdir("uncropped"):
    loaded_already.append(int(filename.split("_")[0]))
loaded_already = set(loaded_already)



#Note: you need to create the uncropped folder first in order 
#for this to work
for a in act:
    name = a.split()[1].lower()
    for link in (LINK_FEMALE_FILENAME, LINK_MALE_FILENAME):
        for line in open(link):
            if a in line:
                identifier = line.split()[3]
                filename = identifier+"_"+name+"_"+'.'+line.split()[4].split('.')[-1]
                if int(identifier) not in loaded_already:
                    
                    #A version without timeout (uncomment in case you need to 
                    #unsupress exceptions, which timeout() does)
                    #testfile.retrieve(line.split()[4], "uncropped/"+filename)
                    #timeout is used to stop downloading images which take too long to download
                    if not os.path.exists(UNPROCESSED__DIR+filename):            
                        timeout(testfile.retrieve, (line.split()[4],UNPROCESSED__DIR+filename), {}, 0.3)
                        print filename
                else: 
                    print identifier+ " " + "already loaded"
                face_locations[filename] = get_bounds(line)


            
        
          
with open("face_locations.json", "w+") as fp:
    json.dump(face_locations, fp, skipkeys=True)
    #cPickle.dumps(face_locations)