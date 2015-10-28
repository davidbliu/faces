import pbl_controlpoints as cp
import matplotlib.pyplot as plt

im = plt.imread('./faces/david.jpg')
points = cp.load_points('david')

for p in points:
    print p[0]
    print p[1]
    print '...'
    im[p[0], p[1]]*=0.

plt.imshow(im)
plt.show()
