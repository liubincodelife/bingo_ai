mkdir result_img
python ./test.py --model ./allconv5_deploy.prototxt  --weights ./allconv5__iter_30000.caffemodel --src ../../../../../../datas/test/segmentation  --dst ./result_img  --testsize 224 2>&1 | tee logtest.txt
