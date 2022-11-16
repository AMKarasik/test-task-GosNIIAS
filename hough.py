import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import hough_line, hough_line_peaks


def find_inter(k1, b1, k2, b2):
    """
        y = k1 * x + b1
        y = k2 * x + b2
    """
    if k2 != k1:
        x = - (b2 - b1) / (k2 - k1)
        y = k1 * x + b1
        return x, y
    else:
        return None


image = cv2.imread('/rect_pics_gen/11.png')  # open image
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  # to gray
gray = cv2.GaussianBlur(gray, (3, 3), 0)  # some blur
# cv2.imwrite("gray.png", gray)  # save gray image

edged = cv2.Canny(gray, 0, 10)  # leave only the borders
# cv2.imwrite("edged.png", edged)   # save edged image

using_angles = np.linspace(-np.pi / 2, np.pi / 2, 1800)  # introduce angles array

halfspace, theta, dist = hough_line(edged, using_angles)

# draw Hough Accumulator
plt.figure(figsize=(15, 10))
plt.title('Hough Accumulator', size=30)
plt.imshow(halfspace, cmap='gray')
plt.savefig('accumulator.png')

angle_list = []

fig, axes = plt.subplots(1, 2, figsize=(20, 8))
ax = axes.ravel()

# draw edged rectangle
ax[0].imshow(edged, cmap='gray')
ax[0].set_title('Edged rectangle', size=30)
ax[0].set_axis_off()

ax[1].imshow(edged, cmap='gray')

origin = np.array((0, edged.shape[1]))
lines = []

# draw straight lines along the borders using Hough Transform
for _, angle, dist in zip(*hough_line_peaks(halfspace, theta, dist)):
    y0, y1 = (dist - origin * np.cos(angle)) / np.sin(angle)
    ax[1].plot(origin, (y0, y1), '-r')
    lines += [(1 / np.tan(angle), dist / np.sin(angle))]
    print(np.degrees(angle), dist)

inter = []

# lines intersection
for i in range(len(lines)):
    for j in range(i+1, len(lines)):
        print(f"intersection of lines{lines[i]} and {lines[j]}:", end=' ')
        point = find_inter(lines[i][0], lines[i][1], lines[j][0], lines[j][1])
        if point != None:
            x, y = point
            if abs(x) > 1000 or abs(y) > 1000:
                print("NO INTERSECTION")
            else:
                print(x, y)
                inter += [(-x, y)]

# draw intersection points
ax[1].plot([i[0] for i in inter], [i[1] for i in inter], 'yo', markersize=12)
ax[1].set_xlim(origin)
ax[1].set_ylim((edged.shape[0], 0))
ax[1].set_title('Detected rectangle', size=30)
plt.savefig('detection.png')
plt.show()
