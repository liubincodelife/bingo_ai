python test_model.py --model ./deploy.prototxt --weights ./mobilenet_finetune_iter_20000.caffemodel --src ../all_shuffle_val.txt --testsize 96 2>&1 | tee test_log.txt
