import tensorflow as tf
import sys
sys.path.append("./deploy")
from imports.models import segmentation_block, feathering_block
import numpy as np
import cv2
import os


def segmentation(img_path):
    testsize = 128
    x = tf.placeholder(tf.float32, [1, testsize, testsize, 3])
    binaryseg = segmentation_block(x)
    softseg = feathering_block(x, binaryseg)

    useSrcImg = True

    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        sess.run(init)
        saver = tf.train.Saver()
        saver.restore(sess, "./deploy/ckpt-55000")

        imagename = img_path
        print("imagename = ", imagename)
        splitname = imagename.rsplit('/', 1)[1]
        prevname = splitname.split('.')[0]
        '''
        img = cv2.imread(imagename)
        img = cv2.resize(img, (testsize, testsize))
        img = img.astype(np.float32)
        print("img shape = ", img.shape, "img type = ", type(img))
        cv2.namedWindow("img cv", 0)
        cv2.imshow("img cv", img.astype(np.uint8))
        '''
        img2 = tf.read_file(imagename)
        img2 = tf.cast(tf.image.decode_jpeg(img2, channels=3), dtype=tf.float32)
        img2 = tf.image.resize_images(img2, 1 * [testsize, testsize])  # 1,128,128,3
        print("img2 shape = ", img2.shape, "img2 type = ", type(img2))
        img2 = img2.eval()
        print("imgnumpy shape = ", img2.shape, "imgnumpy type =", type(img2))
        # cv2.namedWindow("img tf", 0)
        # cv2.imshow("img tf", img2.astype(np.uint8))

        imgs = np.zeros([1, testsize, testsize, 3], dtype=np.float32)
        imgs[0:1, ] = img2
        print("imgs shape = ", imgs.shape)
        binaryseg_, softseg_ = sess.run([binaryseg, softseg], feed_dict={x: imgs})
        softseg_ = np.squeeze(softseg_)
        binaryseg_ = np.squeeze(binaryseg_)[:, :, 0:1]
        #softsegname = "./result/" + prevname + "_softseg.jpg"
        #hardsegname = "./result/" + prevname + "_hardseg.jpg"
        # print("softsegname", softsegname)
        # print (softseg_.shape,type(softseg_))
        # print("hardsegname", softsegname)
        # print (binaryseg_.shape,type(softseg_))

        srcImg = cv2.imread(imagename)
        srcHeight = srcImg.shape[0]
        srcWeight = srcImg.shape[1]

        outHeight = srcHeight
        outWeight = srcWeight

        if not useSrcImg:
            outHeight = testsize
            outWeight = testsize

        alpha = cv2.merge((softseg_, softseg_, softseg_))

        if not useSrcImg:
            srcImg = cv2.resize(srcImg, (testsize, testsize))
        else:
            alpha = cv2.resize(alpha, (outWeight, outHeight))
        alpha = alpha.astype(float)
        foreground = np.multiply(alpha, srcImg.astype(np.float32))

        background = np.zeros([outHeight, outWeight, 3], np.uint8)
        background[:, :, 0] = np.zeros([outHeight, outWeight]) + 255
        background[:, :, 1] = np.zeros([outHeight, outWeight]) + 255
        background[:, :, 2] = np.zeros([outHeight, outWeight]) + 255
        background = background.astype(float)
        background = cv2.multiply(1 - alpha, background)
        outImg = foreground + background

        outname = "./app/static/downloads/" + prevname + "_out.jpg"
        #cv2.imwrite(hardsegname, (binaryseg_ * 255.0).astype(np.uint8))
        #cv2.imwrite(softsegname, (softseg_ * 255.0).astype(np.uint8))
        cv2.imwrite(outname, outImg.astype(np.uint8))
        '''
        cv2.namedWindow("hardseg", 0)
        cv2.namedWindow("softseg", 0)
        cv2.imshow("hardseg", (binaryseg_ * 255.0).astype(np.uint8))
        cv2.imshow("softseg", (softseg_ * 255.0).astype(np.uint8))
        cv2.namedWindow("foreground", 0)
        cv2.imshow("foreground", foreground.astype(np.uint8))
        cv2.namedWindow("background", 0)
        cv2.imshow("background", background.astype(np.uint8))
        cv2.namedWindow("out", 0)
        cv2.imshow("out", outImg.astype(np.uint8))

        cv2.waitKey(0)
        '''
        return outname


if __name__ == '__main__':
    path = sys.argv[1]
    segmentation(path)