mkdir result_img
python ./test.py --model ./resnet18_deploy.prototxt  --weights ./resnet18__iter_30000.caffemodel --src ../../../../../datas/test/segmentation  --dst ./result_img  --testsize 224 2>&1 | tee logtest.txt
