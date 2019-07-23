SOLVER=./solver.prototxt
WEIGHTS=./resnet-18.caffemodel
/home/liubin/Workspaces/DeepLearning/caffe_bingo/build/tools/caffe train -solver $SOLVER -weights $WEIGHTS -gpu 0 2>&1 | tee log.txt 
	
