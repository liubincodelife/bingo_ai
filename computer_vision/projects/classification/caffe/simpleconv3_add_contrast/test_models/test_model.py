#_*_ coding:utf8
import sys
sys.path.insert(0, '/Users/longpeng/opts/Caffe_Long/python/')
import caffe
import os,shutil
import numpy as np
from PIL import Image as PILImage
from PIL import ImageMath
import matplotlib.pyplot as plt
import time
import cv2

debug=True
import argparse
def parse_args():
   parser = argparse.ArgumentParser(description='test resnet model for portrait segmentation')
   parser.add_argument('--model', dest='model_proto', help='the model', default='test.prototxt', type=str)
   parser.add_argument('--weights', dest='model_weight', help='the weights', default='./test.caffemodel', type=str)
   parser.add_argument('--testsize', dest='testsize', help='inference size', default=60,type=int)
   parser.add_argument('--src', dest='imglist', help='the src image folder', type=str, default='./')
   parser.add_argument('--gt', dest='gt', help='the gt', type=int, default=0)
   args = parser.parse_args()
   return args

def start_test(model_proto,model_weight,imglist,testsize):
   caffe.set_mode_cpu()
   net = caffe.Net(model_proto, model_weight, caffe.TEST)
   imgs = open(imglist)
   
   count = 0
   acc = 0

   for imgname in imgs:
      imgpath,imglabel = imgname.strip().split(' ')
      img = cv2.imread(imgpath)
      if img is None:
          print "---------img is empty---------",imgpath
          continue
      
      img = cv2.resize(img,(testsize,testsize))

      transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
      transformer.set_mean('data', np.array([104.008,116.669,122.675]))
      transformer.set_transpose('data', (2,0,1))
              
      out = net.forward_all(data=np.asarray([transformer.preprocess('data', img)]))
         
      result = out['prob'][0]
      probneutral = result[0]
      print "prob neutral",probneutral 
     
      probsmile = result[1]
      print "prob smile",probsmile
      problabel = -1
      probstr = 'none'
      if probneutral >= probsmile and imglabel == '0':
          acc = acc + 1
      elif probneutral <= probsmile and imglabel == '1':
          acc = acc + 1
      count = count + 1
   
   print "acc=",float(acc)/float(count) 

if __name__ == '__main__':
    args = parse_args()
    start_test(args.model_proto,args.model_weight,args.imglist,args.testsize)
