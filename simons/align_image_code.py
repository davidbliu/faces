import numpy as np
import matplotlib.pyplot as plt

def get_points(im1, im2):
    edge1 = im1.shape[0] - 1
    edge2 = im1.shape[1] - 1
    box = np.array([[0,0],[edge2,0],[0,edge1],[edge2,edge1]])

    plt.imshow(im1)
    print("Select left, right of forehead.")
    fore1 = np.array(plt.ginput(2))
    print("Select in, peak, out of L/R eyebrows.")
    brows1 = np.array(plt.ginput(6))
    print("Select left, right, top, bottom of L/R eyes.")
    eyes1 = np.array(plt.ginput(8))
    print("Select left, right, tip, bottom of nose.")
    nose1 = np.array(plt.ginput(4))
    print("Select left, right, top, bottom of mouth.")
    mouth1 = np.array(plt.ginput(4))
    print("Select left, right of chin.")
    chin1 = np.array(plt.ginput(2))
    print("Select eyebrow, eye, nose, mouth of L/R face.")
    ears1 = np.array(plt.ginput(8))
    plt.close()
    plt.imshow(im2)
    print("Select left, right of forehead.")
    fore2 = np.array(plt.ginput(2))
    print("Select in, peak, out of L/R eyebrows.")
    brows2 = np.array(plt.ginput(6))
    print("Select left, right, top, bottom of L/R eyes.")
    eyes2 = np.array(plt.ginput(8))
    print("Select left, right, tip, bottom of nose.")
    nose2 = np.array(plt.ginput(4))
    print("Select left, right, top, bottom of mouth.")
    mouth2 = np.array(plt.ginput(4))
    print("Select left, right of chin.")
    chin2 = np.array(plt.ginput(2))
    print("Select eyebrow, eye, nose, mouth of L/R face.")
    ears2 = np.array(plt.ginput(8))
    plt.close()

    face1 = np.concatenate((fore1, brows1, eyes1, nose1, mouth1, chin1, ears1, box))
    face2 = np.concatenate((fore2, brows2, eyes2, nose2, mouth2, chin2, ears2, box))
    np.save("./faces.npy", (face1, face2))

def get_point(im1):
    edge1 = im1.shape[0] - 1
    edge2 = im1.shape[1] - 1
    box = np.array([[0,0],[edge2,0],[0,edge1],[edge2,edge1]])

    plt.imshow(im1)
    print("Select left, right of forehead.")
    fore1 = np.array(plt.ginput(2))
    print("Select in, peak, out of L/R eyebrows.")
    brows1 = np.array(plt.ginput(6))
    print("Select left, right, top, bottom of L/R eyes.")
    eyes1 = np.array(plt.ginput(8))
    print("Select left, right, tip, bottom of nose.")
    nose1 = np.array(plt.ginput(4))
    print("Select left, right, top, bottom of mouth.")
    mouth1 = np.array(plt.ginput(4))
    print("Select left, right of chin.")
    chin1 = np.array(plt.ginput(2))
    print("Select eyebrow, eye, nose, mouth of L/R face.")
    ears1 = np.array(plt.ginput(8))
    plt.close()

    face1 = np.concatenate((fore1, brows1, eyes1, nose1, mouth1, chin1, ears1, box))
    np.save("./bells.npy", face1)
