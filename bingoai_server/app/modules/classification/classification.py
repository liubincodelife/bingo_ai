import cv2
import numpy as np
import dlib
import sys
import os
import caffe
import time


PREDICTOR_PATH = "./models/shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(PREDICTOR_PATH)
detector = dlib.get_frontal_face_detector()

cascade_path = '/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml'
cascade = cv2.CascadeClassifier(cascade_path)


class EmotionNet:
    def __init__(self, mode, test_size):
        if mode == 0:
            caffe.set_mode_gpu()
            caffe.set_device(0)
        else:
            caffe.set_mode_cpu()
        self.model_proto = "./app/modules/classification/deploy/deploy.prototxt"
        self.model_weight = "./app/modules/classification/deploy/mobilenet_finetune_iter_20000.caffemodel"
        self.emotion_net = caffe.Net(self.model_proto, self.model_weight, caffe.TEST)
        self.img_size = int(test_size)

    def get_emotion_type(self, img_path, enable_crop):
        start_time = time.time()
        input_img = cv2.imread(img_path)
        roi_img, mark_img_name = getRoi(input_img, img_path)
        mouth_img = cv2.resize(roi_img, (128, 128))
        img_height, img_width, channel = mouth_img.shape

        if enable_crop == 1:
            # print("use crop")
            cropx = (img_width - self.img_size) // 2
            cropy = (img_height - self.img_size) // 2
            mouth_img = mouth_img[cropy:cropy + self.img_size, cropx:cropx + self.img_size, 0:channel]
        else:
            mouth_img = cv2.resize(mouth_img, (self.img_size, self.img_size), interpolation=cv2.INTER_NEAREST)

        transformer = caffe.io.Transformer({'data': self.emotion_net.blobs['data'].data.shape})
        transformer.set_mean('data', np.array([104.008, 116.669, 122.675]))
        transformer.set_transpose('data', (2, 0, 1))

        out = self.emotion_net.forward_all(data=np.asarray([transformer.preprocess('data', mouth_img)]))
        end_time = time.time()
        print("used time: ", (end_time - start_time) * 1000, "ms")
        result = out['classifier'][0]
        print("result=", result)
        emotion_type = np.argmax(result)

        return emotion_type, result[emotion_type][0][0], mark_img_name


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
        # cv2.putText(im, str(idx), pos,
        #            fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
        #            fontScale=0.4,
        #            color=(0, 0, 255))
        cv2.circle(im, pos, 2, (255, 0, 0), -1, cv2.LINE_AA)
    return im


def getRoi(img, img_path):
    # print("image shape=", img.shape)
    landmarks = get_landmarks(img)
    # print("landmarks", landmarks.shape)
    file_name = img_path.rsplit('/', 1)[1]
    # print("feature name: ", file_name)
    new_name = file_name.split('.', 1)[0]
    new_name = new_name + "_mark.jpg"
    # print("new_name: ", new_name)
    featureImg = annotate_landmarks(img, landmarks)
    save_path = os.path.join("./app/static/downloads", new_name)
    # print("save_path: ", save_path)
    cv2.imwrite(save_path, featureImg)

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

    # print("xmin=", xmin)
    # print("xmax=", xmax)
    # print("ymin=", ymin)
    # print("ymax=", ymax)

    roiwidth = xmax - xmin
    roiheight = ymax - ymin

    roi = img[ymin:ymax, xmin:xmax, 0:3]
    # cv2.imshow('roi src', roi)
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
    return roi, new_name


emotionNet = EmotionNet(1, 96)


def classification(img_path):
    print("img_path = ", img_path)
    emotion, confidence, mark_img_name = emotionNet.get_emotion_type(img_path, 1)
    print("emotion = ", emotion)
    return emotion, confidence, mark_img_name


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
        roi_name = "./roi_img/" + prefix + "_roi" + ".jpg"
        print(roi_name)
        faceImg = cv2.imread(image_path, 1)
        roiImg = getRoi(faceImg)
        roiImg = cv2.resize(roiImg, (128, 128))
        cv2.imwrite(roi_name, roiImg)
