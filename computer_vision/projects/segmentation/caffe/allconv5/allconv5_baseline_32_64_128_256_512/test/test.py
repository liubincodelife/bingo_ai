#coding=utf8
import sys
#sys.path.insert(0, '/Users/momo/Desktop/Caffe_Long/python/')
import caffe
import os
import numpy as np
from PIL import Image as PILImage
import matplotlib.pyplot as plt
import time
import cv2
#import Image

pallete = [0,0,0,
255, 255, 255]

debug=False
import argparse

usecaffeioread=False

def parse_args():
   parser = argparse.ArgumentParser(description='test resnet model for portrait segmentation')
   parser.add_argument('--model', dest='model_proto', help='the model', default='train_val_res18_matting_prob.prototxt', type=str)
   parser.add_argument('--weights', dest='model_weight', help='the weights', default='./res18_iter_25000.caffemodel', type=str)
   parser.add_argument('--src', dest='img_folder', help='the src', type=str, default='./')
   parser.add_argument('--label', dest='label_folder', help='the label', type=str, default='./')
   parser.add_argument('--dst', dest='dst_folder', help='the dst', type=str, default='./test_results')
   parser.add_argument('--testsize', dest='testsize', help='the testsize', type=int, default=100)
   args = parser.parse_args()
   return args


def start_test(model_proto,model_weight,img_folder,dst_folder,testsize):
   net = caffe.Net(model_proto, model_weight, caffe.TEST)

   if not os.path.exists(dst_folder):
      os.mkdir(dst_folder)

   val_list =  os.listdir(img_folder)
   print ("----images num=",len(val_list))

   for line in val_list:
      img_name = line.strip()
      
      img_id = img_name.split('.')[0]
      img_path = os.path.join(img_folder,img_name)
      
      print ("img_path=",img_path)

      start_time = time.time()
      im  =  caffe.io.load_image(img_path) ###大图有时候读取失败
      if not usecaffeioread: 
         im = cv2.imread(img_path).astype(np.float)
      
      ###---if resize
      height,width,channel = im.shape
      newwidth = int(testsize)
      newheight = newwidth
      #newheight = float(height) / float(width) * newwidth
      im = cv2.resize(im,(int(newwidth),int(newwidth)),interpolation = cv2.INTER_NEAREST)

      im_input = im[np.newaxis, :, :]
      im_input = np.transpose(im_input, (0, 3, 1, 2))
      print ("im shape=",im.shape)
      print ("im_input shape=",im_input.shape)
      net.blobs['data'].reshape(*im_input.shape)

      print ("img_shape=",net.blobs['data'].shape)

      transformer  =  caffe.io.Transformer({'data':  net.blobs['data'].data.shape})
      transformer.set_mean('data',  np.array([104.008,116.669,122.675]))
      transformer.set_transpose('data',  (2,0,1))
      if usecaffeioread: 
         transformer.set_channel_swap('data',  (2,1,0))  ##if using not cv2.imread
         transformer.set_raw_scale('data',  255.0) ##if using not cv2.imread
      t0  =  time.time()
      out  =  net.forward(data=np.asarray([transformer.preprocess('data',  im)]))
      
      end_time = time.time()
      print ("used time=",(end_time - start_time)*1000,"ms")
      res  =  out['prob'] ###网络输出大小，1×channel*height*width

      res  =  np.squeeze(res)
      res  =  np.transpose(res, [1,2,0])

      res_label  =  np.argmax(res,axis=2)
      res_label = (res_label).astype(np.uint8)
       
      height,width = res_label.shape
      
      if not usecaffeioread:
         print ("input is bgr")
         rgbsrc = im.astype(np.uint8)
      else:
         rgbsrc = cv2.cvtColor((im*255.0).astype(np.uint8),cv2.COLOR_RGB2BGR)

      result = cv2.cvtColor(rgbsrc,cv2.COLOR_BGR2BGRA)
      height,width,channel = result.shape
      for i in range(height):
         for j in range(width):
            if res_label[i,j]==1:
               result[i,j][3] = 255
               result[i,j][2] = 255
     
      cv2.imwrite(os.path.join(dst_folder,img_name),result)

      if debug:
         cv2.imshow("result",result)
         k = cv2.waitKey(0)
         if k == ord('q'):
            return

if __name__ == '__main__':
    args = parse_args()
    start_test(args.model_proto,args.model_weight,args.img_folder,args.dst_folder,args.testsize)
