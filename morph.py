""" main morphing code all here """
import numpy as np
import glob

from matplotlib import pyplot as plt
from scipy.spatial import Delaunay
from scipy.interpolate import interp2d
from skimage.draw import polygon
import pickle



def average_points(p1, p2, t=0.5):
    avg = []
    for i in range(len(p1)):
        point1 = p1[i]
        point2 = p2[i]
        avg0 = point1[0]*t+point2[0]*(1.-t)
        avg1 = point1[1]*t+point2[1]*(1.-t)
        avg.append([avg0, avg1])
    return avg


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

def computeAffine(tri1_pts, tri2_pts):
    tri1 = np.ones([3,3])
    tri2 = np.ones([3,3])
    tri1[:,:-1] = tri1_pts[:,[1,0]]
    tri2[:,:-1] = tri2_pts[:,[1,0]]
    return np.dot(tri2.T, np.linalg.inv(tri1.T))

def morph(im1, im2, im1_pts, im2_pts, tri, warp_frac, dissolve_frac):
    result = np.empty(im1.shape)
    for triangle in tri.simplices:
        pts1 = im1_pts[triangle]
        pts2 = im2_pts[triangle]
        pts3 = warp_frac*pts1 + (1-warp_frac)*pts2
        A = computeAffine(pts3, pts1)
        B = computeAffine(pts3, pts2)
        rr, cc = polygon(pts3[:,1], pts3[:,0])
        vector = np.ones([3, len(rr)])
        vector[0] = rr
        vector[1] = cc
        A = np.dot(A, vector).astype(int)
        B = np.dot(B, vector).astype(int)
        result[rr, cc] = dissolve_frac*im1[A[0], A[1]] +\
                (1-dissolve_frac)*im2[B[0], B[1]]
    return result/255.

# Morph 2 images together
def create_morphed(im1, im2, p1, p2, t = 0.5):
    p1 = [x[::-1] for x in p1]
    p2 = [x[::-1] for x in p2]
    p1 = np.array(p1)
    p2 = np.array(p2)
    points = average_points(p1, p2)
    tri = Delaunay(points)
    o = morph(im1, im2, p1, p2, tri, t, t)
    return o

# Morph a dictionary of images and a dictionary of points together
def create_meanface(images, points):
    pts = []
    for p in points:
        pts.append([x[::-1] for x in p])
    avgPoints = get_average(pts)
    tri = Delaunay(avgPoints)
    meanface = np.zeros(images[0].shape)
    for i in range(len(images)):
        pts = [x[::-1] for x in points[i]]
        pts =  np.array(pts)
        o = morph(images[i], images[i], pts , avgPoints, tri, 0, 1)
        meanface += (1./len(images))*o
    return meanface
    
if __name__=='__main__':
    print 'testing this script'
    p1 = pickle.load(open('./points/simon.p', 'rb'))
    p2 = pickle.load(open('./points/david.p', 'rb'))
    im1 = plt.imread('./faces/simon.jpg')
    im2 = plt.imread('./faces/david.jpg')
    # o = create_morphed(im1, im2, p1, p2)
    o = create_meanface([im1,im2], [p1,p2])
    plt.imshow(o)
    plt.show()

