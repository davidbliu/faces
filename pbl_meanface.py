from scipy.spatial import Delaunay
import numpy.linalg as la
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import *
import os
import pickle
import sys
from config import *
FILTER = []
MODE = ''
# FILTER = ['alice', 'jensen', 'tiffany']

def barycentric_coords(vertices, point):
        T = (np.array(vertices[:-1])-vertices[-1]).T
        v = np.dot(la.inv(T), np.array(point)-vertices[-1])
        v.resize(len(vertices))
        v[-1] = 1-v.sum()
        return v

def get_average(pts):
    numpoints = len(pts[0]) 
    f = 1./len(pts)
    avg = []
    for i in range(numpoints):
        avgx = 0.
        avgy = 0.
        for points in pts:
            pt = points[i]
            avgx += pt[0]*f
            avgy += pt[1]*f
        avg.append((avgx, avgy))
    return np.array(avg)

def create_meanface(points, images):
    points = [np.array(p) for p in points]
    # TODO: remove last 4 points from each except im1
    avg = get_average(points)
    tri = Delaunay(avg)
    # compute output image
    output = np.zeros(images[0].shape)
    factor = 1./len(points)
    for x in range(output.shape[0]):
        for y in range(output.shape[1]):
            pt = np.array([x,y])
            s = tri.find_simplex(pt)
            if s!=-1:
                simplex = tri.simplices[s]
                avgTri = avg[simplex]
                b = barycentric_coords(avgTri, pt)
                v = output[x,y]
                for i in range(len(points)):
                    currTri = points[i][simplex]
                    im = images[i]
                    x1, y1 = np.floor(currTri[0]*b[0]+currTri[1]*b[1]+currTri[2]*b[2])
                    v += (factor * im[x1, y1])/255.
                    output[x,y] = v 
    return output

def males():
    with open('males.txt', 'r') as infile:
        males = [x.strip() for x in infile]
        return males

def read_control_points(fname):
    with open(POINTS_DIR+fname+'.p', 'rb') as ifile:
        return pickle.load(ifile)

if __name__=='__main__':
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

    print 'generating meanface for '+ ','.join(fnames)
    control_points = [read_control_points(x) for x in fnames]
    images = [plt.imread(FACES_DIR+fname+'.jpg') for fname in fnames]

    output = create_meanface(control_points, images)
    if FILTER and len(FILTER)>=2:
        imname = '_'.join(FILTER)
    imsave(MORPH_DIR+imname+'.png',output) 
    plt.imshow(output)
    plt.show()
