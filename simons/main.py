import numpy as np
import glob

from matplotlib import pyplot as plt
from align_image_code import get_points, get_point
from scipy.spatial import Delaunay
from scipy.interpolate import interp2d
from skimage.draw import polygon

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
    return result

def main():
    im1 = plt.imread("./alison.jpg")/255.
    im2 = plt.imread("./dcheung.jpg")/255.

    ## Bells
    #im3 = plt.imread("./simon3.jpg")/255.
    #get_points(im1, im2)
    #get_point(im3)
    #face1, face2 = np.load("./faces.npy")
    #femshape = face2 - face1
    #face3 = np.load("./bells.npy")
    #tri = Delaunay(face3+0.25*femshape)
    #plt.imsave("./fs1.jpg", morph(im3, im3, face3, face3+0.5*femshape, tri, 0, 1))
    #tri = Delaunay(face3+0.50*femshape)
    #plt.imsave("./fs2.jpg", morph(im3, im3, face3, face3+1.0*femshape, tri, 0, 1))
    #tri = Delaunay(face3+0.75*femshape)
    #plt.imsave("./fs3.jpg", morph(im3, im3, face3, face3+1.5*femshape, tri, 0, 1))

    ## Correspondences
    # get_points(im1, im2)

    face1, face2 = np.load("./faces.npy")
    tri = Delaunay((face1+face2)/2)

    ## Caricature
    #plt.imsave("./car1.jpg", morph(im1, im2, face1, face2, tri, -0.5, 1))
    #plt.imsave("./car2.jpg", morph(im1, im2, face1, face2, tri, -1, 1))

    ## Mid-way Face
    #plt.figure()
    #plt.imshow(im1)
    #plt.triplot(face1[:,0], face1[:,1], tri.simplices.copy())
    #plt.axis('off')
    #plt.savefig("./trisimon.jpg", bbox_inches='tight', pad_inches=0)
    #plt.figure()
    #plt.imshow(im2)
    #plt.triplot(face2[:,0], face2[:,1], tri.simplices.copy())
    #plt.axis('off')
    #plt.savefig("./trimoa.jpg", bbox_inches='tight', pad_inches=0)
    plt.imsave("./china.jpg", morph(im1, im2, face1, face2, tri, 0.5, 0.5))

    ## Morph Sequence
    #for step in range(46):
        #plt.imsave(("./moa%02d.jpg" % step), morph(im1, im2, face1, face2, tri,\
            #step/45., step/45.))

    ## Danes
    #images = np.empty([33,480,640,3])
    #faces = np.empty([33,62,2])
    #count = 0
    #for filename in glob.glob("./*-2m.asf"):
        #with open(filename, 'r') as f:
            #lines = f.readlines()
            #images[count] = plt.imread(lines[-1].strip('\n'))/255.
            #lines = np.array([line.split() for line in lines[16:74]])
            #faces[count,:-4,:] = lines[:,2:4]
            #faces[count,-4:,:] = [[0,0],[1,0],[0,1],[1,1]]
            #faces[count] = faces[count]*[639,479]
        #count += 1
    #theface = np.average(faces, axis=0)
    #tri = Delaunay(theface)
    #mean = np.zeros(images[0].shape)
    #for i in range(len(images)):
        #data = morph(images[i], images[i], faces[i], theface, tri, 0, 1)
        #if (i%10 == 0):
            #plt.imsave(("./dane%02d.jpg" % i), data)
        #mean += (1./len(images))*data
    #plt.imsave("./dane.jpg", mean)

if __name__ == "__main__":
    main()
