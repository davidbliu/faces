import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math
import numpy as np
import skimage.transform as sktr
from scipy import ndimage
import sys
import pickle
from config import *

def get_points(im1):
    p1 = []

    print '8 points for face'
    plt.imshow(im1)
    p1.append(plt.ginput(8))
    plt.close()


    print '4 points each for left and right eyes'
    plt.imshow(im1)
    p1.append(plt.ginput(8))
    plt.close()
    
    print '4 points for mouth'
    plt.imshow(im1)
    p1.append(plt.ginput(4))
    plt.close()
    print '5 points for nose'
    plt.imshow(im1)
    p1.append(plt.ginput(5))
    plt.close()


    # print '6 for brows'
    # plt.imshow(im1)
    # p1.append(plt.ginput(6))
    # plt.close()
    corners = []
    corners.append((0, 399))
    corners.append((0, 0))
    corners.append((299, 399))
    corners.append((299, 0))
    # # p1.append(corners)

    # print '16 for chin'
    # plt.imshow(im1)
    # p1.append(plt.ginput(16))
    # plt.close()

    # print '4 points each for left and right eyes'
    # plt.imshow(im1)
    # p1.append(plt.ginput(8))
    # plt.close()
    
    # print '6 points for browgame'
    # plt.imshow(im1)
    # p1.append(plt.ginput(6))
    # plt.close()
    # print '8 points for mouth'
    # plt.imshow(im1)
    # p1.append(plt.ginput(8))
    # plt.close()
    # print '6 points for nose'
    # plt.imshow(im1)
    # p1.append(plt.ginput(6))
    # plt.close()

    p1.append(corners)
    points = [item[::-1] for sublist in p1 for item in sublist] 
    
    return points
     


def save_points(points, output_filename):
    with open(POINTS_DIR+output_filename+'.p', 'wb') as ofile:
        pickle.dump(points, ofile)


def load_points(input_filename):
    pts = pickle.load(open(POINTS_DIR+input_filename+'.p', 'rb'))
    return pts

if __name__=='__main__':
    facename = sys.argv[1]
    face_file = FACES_DIR+facename+'.jpg'
    im = plt.imread(face_file)

    points = get_points(im)
    save_points(points, facename)
