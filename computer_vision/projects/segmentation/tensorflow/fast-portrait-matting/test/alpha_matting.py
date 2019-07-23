import numpy as np
import cv2
import os
import sys

    
'''
if __name__ == '__main__':
    testsize = 128
    alphaImagePath = sys.argv[1]
    srcImagePath = sys.argv[2]
    alphaImg = cv2.imread(alphaImagePath)
    srcImg = cv2.imread(srcImagePath)
    srcImg = cv2.resize(srcImg, (testsize, testsize))
    cv2.namedWindow("alpha img", 0)
    cv2.namedWindow("src img", 0)
    cv2.imshow("alpha img", alphaImg)
    cv2.imshow("src img", srcImg)
    print("alphaImg shape = ", alphaImg.shape, "alphaImg type = ", type(alphaImg))
    print("srcImg shape = ", srcImg.shape, "srcImg type = ", type(srcImg))
    alpha = alphaImg.astype(float)/255
    foreground = np.multiply(alpha, srcImg.astype(np.float32))
    background = np.zeros([testsize, testsize, 3], np.uint8)
    background[:, :, 0] = np.zeros([testsize, testsize]) + 255
    background = background.astype(float)
    background = cv2.multiply(1-alpha,background)
    outImg = foreground + background
    cv2.namedWindow("out", 0)
    cv2.imshow("out", outImg/255)
    cv2.namedWindow("background", 0)
    cv2.imshow("background", background/255)
    cv2.namedWindow("foreground img", 0)
    cv2.imshow("foreground img", foreground/255)
    cv2.waitKey(0)
'''

if __name__ == '__main__':
    testsize = 128
    alphaImagePath = sys.argv[1]
    srcImagePath = sys.argv[2]
    alphaImg = cv2.imread(alphaImagePath)
    srcImg = cv2.imread(srcImagePath)
    srcShape = srcImg.shape
    srcHeight = int(srcShape[0])
    srcWeight = int(srcShape[1])
    print("srcHeight = ", srcHeight)
    print("srcWeight = ", srcWeight)
    #srcImg = cv2.resize(srcImg, (testsize, testsize))
    size = (srcHeight, srcWeight)
    alphaImg = cv2.resize(alphaImg, (600, 800))
    cv2.namedWindow("alpha img", 0)
    cv2.namedWindow("src img", 0)
    cv2.imshow("alpha img", alphaImg)
    cv2.imshow("src img", srcImg)
    print("alphaImg shape = ", alphaImg.shape, "alphaImg type = ", type(alphaImg))
    print("srcImg shape = ", srcImg.shape, "srcImg type = ", type(srcImg))
    alpha = alphaImg.astype(float)/255
    foreground = np.multiply(alpha, srcImg.astype(np.float32))
    background = np.zeros([srcHeight, srcWeight, 3], np.uint8)
    background[:, :, 0] = np.zeros([srcHeight, srcWeight]) + 255
    background = background.astype(float)
    background = cv2.multiply(1-alpha,background)
    outImg = foreground + background
    cv2.namedWindow("out", 0)
    cv2.imshow("out", outImg/255)
    cv2.namedWindow("background", 0)
    cv2.imshow("background", background/255)
    cv2.namedWindow("foreground img", 0)
    cv2.imshow("foreground img", foreground/255)
    cv2.waitKey(0)

