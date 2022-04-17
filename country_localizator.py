
# importing required libraries
import cv2
from matplotlib import pyplot as plt

plt.close('all')

# reads an input image
x=397 
y=165
w=1125 # width of the canvas
h=750 # height of the canvas
background = cv2.imread('africa.PNG',0)[y:y+h, x:x+w]
after = cv2.imread('saotome.PNG',0)[y:y+h, x:x+w]

diff = cv2.absdiff(background, after)
ret,thresh = cv2.threshold(diff,10,255,cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


cXlist=[]
cYlist=[]
for c in contours:
    # calculate moments for each contour
    M = cv2.moments(c)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cXlist.append(cX)
        cYlist.append(cY)
    else:
        cX, cY = 0, 0

i=0
# cv2.circle(thresh, (cXlist[i], cYlist[i]), 5, (255, 0, 0), -1)
# cv2.putText(thresh, "centroid", (cXlist[i] - 25, cYlist[i] - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
print(cXlist[i])
print(cYlist[i])
plt.imshow(thresh)
plt.show()

# https://learnopencv.com/find-center-of-blob-centroid-using-opencv-cpp-python/
# https://stackoverflow.com/questions/27035672/cv-extract-differences-between-two-images
