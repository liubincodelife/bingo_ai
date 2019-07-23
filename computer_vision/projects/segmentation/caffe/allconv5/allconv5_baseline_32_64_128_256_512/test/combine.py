import os
import cv2
import numpy as np
import sys
results = np.zeros((2*224,5*224,3),np.uint8)
images = os.listdir(sys.argv[1])
i = 0
for image in images:
   imagepath = os.path.join(sys.argv[1],image)
   img = cv2.imread(imagepath,1)
   h = i/5
   w = i%5
   i = i+1
   results[h*224:h*224+224,w*224:w*224+224] = img
cv2.imwrite('combine.jpg',results)

