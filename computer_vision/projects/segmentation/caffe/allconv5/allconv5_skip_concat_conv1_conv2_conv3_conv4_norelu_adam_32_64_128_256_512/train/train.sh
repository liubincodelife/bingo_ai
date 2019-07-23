SOLVER=./allconv5.solver
/home/liubin/Workspaces/DeepLearning/caffe_bingo/build/tools/caffe train -solver $SOLVER -gpu 0 2>&1 | tee log.txt
	
