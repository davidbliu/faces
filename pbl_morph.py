import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import *
import sys
import pickle
import morph
from config import *

def create_morphed_movie(im1, im2, p1, p2):
    t=0.
    iteration = 0
    while t<1:
        t += 0.02
        iteration += 1
        print 'computing morph for t='+str(t)
        output = morph.create_morphed(im1, im2, p1, p2, t)
        imsave('results/dalice'+str(iteration)+'.png',output)

if __name__=='__main__':
    im1 = plt.imread('./faces/me.jpg')
    im2 = plt.imread('./faces/alice2.jpg')
    p1 = pickle.load(open('./points/me.p'))
    p2 = pickle.load(open('./points/alice2.p'))
    create_morphed_movie(im1,im2,p1,p2)
