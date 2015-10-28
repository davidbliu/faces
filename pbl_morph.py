from scipy.spatial import Delaunay
import numpy.linalg as la
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import *
from get_points import *
import sys
import morph

from config import *

def average_points(p1, p2, t=0.5):
    avg = []
    for i in range(len(p1)):
        point1 = p1[i]
        point2 = p2[i]
        avg0 = point1[0]*t+point2[0]*(1.-t)
        avg1 = point1[1]*t+point2[1]*(1.-t)
        avg.append([avg0, avg1])
    return avg

def barycentric_coords(vertices, point):
        T = (np.array(vertices[:-1])-vertices[-1]).T
        v = np.dot(la.inv(T), np.array(point)-vertices[-1])
        v.resize(len(vertices))
        v[-1] = 1-v.sum()
        return v

def create_morphed(im1, im2, p1, p2, t = 0.5):
    print 'hi'
    p1=np.array(p1)
    p2=np.array(p2)
    points = np.array(average_points(p1, p2, t))
    tri = Delaunay(points)
    output = np.zeros(im1.shape)
    for x in range(output.shape[0]):
        for y in range(output.shape[1]):
            pt = np.array([x,y])
            s = tri.find_simplex(pt)
            # if s != -1:
                # simplex = tri.simplices[s]
                # t3 = points[simplex]
                # t1 = p1[simplex]
                # t2 = p2[simplex]
                # # # find barycentric coordinate in output triangle
                # b = barycentric_coords(t3, pt)
                # coord1 = t1[0]*b[0]+t1[1]*b[1]+t1[2]*b[2]
                # coord2 = t2[0]*b[0]+t2[1]*b[1]+t2[2]*b[2]
                # coord1 = np.floor(coord1)
                # coord2 = np.floor(coord2)
                # x1, y1 = coord1
                # x2, y2 = coord2
                # output[x,y]=(im1[x1,y1]*t  + im2[x2,y2]*(1-t))/255.
    return output

def create_morphed_movie(im1, im2, p1, p2):
    t=0.
    iteration = 0
    while t<1:
        t += 0.02
        iteration += 1
        print 'computing morph for t='+str(t)
        output = create_morphed(im1, im2, p1, p2, t)
        imsave('results/ray_andrea'+str(iteration)+'.png',output)

if __name__=='__main__':
        f1 = sys.argv[1]
        f2 = sys.argv[2]
        im1 = plt.imread(FACES_DIR+f1+'.jpg')
        im2 = plt.imread(FACES_DIR+f2+'.jpg')
        p1 = pickle.load(open(POINTS_DIR+f1+'.p'))
        p2 = pickle.load(open(POINTS_DIR+f2+'.p'))
        o = morph.create_morphed(im1, im2, p1, p2)
        # save morph
        imname = f1+'_'+f2
        imsave(MORPH_DIR+imname+'.png',o)
        plt.imshow(o)
        plt.show()
