#########################################################################
# Author: longpeng2008to2012@gmail.com
#########################################################################
SOLVER=./mobilenet_solver.prototxt
WEIGHTS=./mobilenet.caffemodel
#/home/liubin/Workspaces/DeepLearning/caffe_bingo/build/tools/caffe train -solver $SOLVER -weights $WEIGHTS -gpu 0 2>&1 | tee log.txt 
/home/liubin/Workspaces/DeepLearning/caffe_bingo/build/tools/caffe train -solver $SOLVER  -gpu 0 2>&1 | tee log.txt 
#/home/longpeng/opts/1_Caffe_Long/build/tools/caffe train -solver $SOLVER -gpu 0 2>&1 | tee log.txt 
