import cv2
import numpy as np
import caffe
import dlib
import sys
import os

PREDICTOR_PATH = "../../../models/shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(PREDICTOR_PATH)
detector = dlib.get_frontal_face_detector()

cascade_path = '/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml'
cascade = cv2.CascadeClassifier(cascade_path)


# This is using the Dlib Face Detector . Better result more time taking
def get_landmarks(img):
    rects = detector(img, 1)
    rect = rects[0]
    print(type(rect.width()))
    if len(rects) == 0:
        return None, None

    return np.matrix([[p.x, p.y] for p in predictor(img, rects[0]).parts()])


def get_landmarks2(img):
    rects = cascade.detectMultiScale(img, 1.3,5)
    x, y, w, h = rects[0]
    rect=dlib.rectangle(x, y, x+w, y+h)
    return np.matrix([[p.x, p.y] for p in predictor(img, rect).parts()])


def annotate_landmarks(img, landmarks):
    im = img.copy()
    for idx, point in enumerate(landmarks):
        pos = (point[0, 0], point[0, 1])
        cv2.putText(im, str(idx), pos,
                    fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                    fontScale=0.4,
                    color=(0, 0, 255))
        cv2.circle(im, pos, 5, color=(0, 255, 255))
    return im


def getRoi(img):
    print("image shape=", img.shape)
    landmarks = get_landmarks(img)
    print("landmarks", landmarks.shape)

    xmin = 10000
    xmax = 0
    ymin = 10000
    ymax = 0

    for i in range(48, 67):
        x = landmarks[i, 0]
        y = landmarks[i, 1]
        if x < xmin:
            xmin = x
        if x > xmax:
            xmax = x
        if y < ymin:
            ymin = y
        if y > ymax:
            ymax = y

    print("xmin=", xmin)
    print("xmax=", xmax)
    print("ymin=", ymin)
    print("ymax=", ymax)

    roiwidth = xmax - xmin
    roiheight = ymax - ymin

    roi = img[ymin:ymax, xmin:xmax, 0:3]
    cv2.imshow('roi src', roi)
    if roiwidth > roiheight:
        dstlen = 1.5 * roiwidth
    else:
        dstlen = 1.5 * roiheight

    diff_xlen = dstlen - roiwidth
    diff_ylen = dstlen - roiheight

    newx = xmin
    newy = ymin

    imagerows, imagecols, channel = img.shape
    if newx >= diff_xlen / 2 and newx + roiwidth + diff_xlen / 2 < imagecols:
        newx = newx - diff_xlen / 2
    elif newx < diff_xlen / 2:
        newx = 0
    else:
        newx = imagecols - dstlen

    if newy >= diff_ylen / 2 and newy + roiheight + diff_ylen / 2 < imagerows:
        newy = newy - diff_ylen / 2
    elif newy < diff_ylen / 2:
        newy = 0
    else:
        newy = imagecols - dstlen

    roi = img[int(newy):int(newy + dstlen), int(newx):int(newx + dstlen), 0:3]
    return roi


if __name__ == '__main__':
    img_folder = sys.argv[1]
    img_list = os.listdir(img_folder)
    print(img_list)
    for img in img_list:
        img_name = img.strip()
        print(img_name)
        prefix = img_name.split('.')[0]
        last = img_name.split('.')[1]
        print(prefix)
        print(last)
        image_path = "./test_img/" + img_name
        print(image_path)
        roi_name = "./roi_img/" + prefix + "_crop" + ".jpg"
        print(roi_name)
        faceImg = cv2.imread(image_path, 1)
        roiImg = getRoi(faceImg)
        roiImg = cv2.resize(roiImg, (128, 128))
        cv2.imwrite(roi_name, roiImg)
