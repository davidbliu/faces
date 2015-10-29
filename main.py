"""
Main morphing file: 
    run as: python main.py list,of,names
""" 
from scipy.spatial import Delaunay
import numpy.linalg as la
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import *
import os
import pickle
import sys
from config import *
import morph

FILTER = []
MODE = ''
MODE = 'male'
MODE = 'female'
def males():
    with open('males.txt', 'r') as infile:
        males = [x.strip() for x in infile]
        return males

def read_control_points(fname):
    with open(POINTS_DIR+fname+'.p', 'rb') as ifile:
        return pickle.load(ifile)

if len(sys.argv)>1:
    FILTER = sys.argv[1].split(',')
fnames = list(set([x.split('.')[0] for x in os.listdir(POINTS_DIR)]))
if FILTER and len(FILTER)>=2:
    fnames = [x for x in fnames if x in FILTER]
imname = 'mean'

if MODE != '' and MODE == 'male':
    fnames = [x for x in fnames if x in males()]
    imname = 'male_mean'
if MODE != '' and MODE == 'female':
    fnames = [x for x in fnames if x not in males()]
    imname = 'female_mean'

print 'morph for '+ ','.join(fnames)
control_points = [read_control_points(x) for x in fnames]
images = [plt.imread(FACES_DIR+fname+'.jpg') for fname in fnames]

output = morph.create_meanface(images, control_points)
if FILTER and len(FILTER)>=2:
    imname = '_'.join(FILTER)
imsave(MORPH_DIR+imname+'.png',output) 
plt.imshow(output)
plt.show()
