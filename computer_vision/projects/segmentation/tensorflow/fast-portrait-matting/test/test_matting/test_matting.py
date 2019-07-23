import numpy as np
import cv2

foreground = cv2.imread("foreground.jpg")
print("foreground shape = ", foreground.shape)
## 先将通道分离
#b,g,r,a = cv2.split(foreGroundImage)

#得到PNG图像前景部分，在这个图片中就是除去Alpha通道的部分
#foreground = cv2.merge((b,g,r))

#得到PNG图像的alpha通道，即alpha掩模
#alpha = cv2.merge((a,a,a))
alpha = cv2.imread("alpha_mask.jpg")
print("alpha shape = ", alpha.shape)

background = cv2.imread("background.jpg")
print("background shape = ", background.shape)

cv2.namedWindow("foreground", 0)
cv2.namedWindow("background", 0)
cv2.namedWindow("alpha", 0)
cv2.imshow("foreground", foreground)
cv2.imshow("background", background)
cv2.imshow("alpha", alpha)
#因为下面要进行乘法运算故将数据类型设为float，防止溢出
foreground = foreground.astype(float)
background = background.astype(float)

#cv2.imwrite("alpha.jpg",alpha)
#将alpha的值归一化在0-1之间，作为加权系数
alpha = alpha.astype(float)/255

cv2.imshow("alpha",alpha)

#将前景和背景进行加权，每个像素的加权系数即为alpha掩模对应位置像素的值，前景部分为1，背景部分为0
foreground = cv2.multiply(alpha,foreground)
cv2.namedWindow("middle fore", 0)
cv2.imshow("middle fore", foreground/255)
background = cv2.multiply(1-alpha,background)
cv2.namedWindow("middle back", 0)
cv2.imshow("middle back", background/255)

outImage = foreground + background

#cv2.imwrite("outImage.jpg",outImage)
cv2.namedWindow("outImg", 0)
cv2.imshow("outImg",outImage/255)
cv2.waitKey(0)
