for i in 10000 20000 30000 40000 50000 60000 70000 80000 90000 100000
do
   WEIGHTS=./models/allconv6__iter_""$i"".caffemodel
   ../../caffe/build/tools/caffe test --model=allconv6.prototxt -weights $WEIGHTS -gpu 3 -iterations 125 2>&1 | tee log_test_""$i"".txt
done
