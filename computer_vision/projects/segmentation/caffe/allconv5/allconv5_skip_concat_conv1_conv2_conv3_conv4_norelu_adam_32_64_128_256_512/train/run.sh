rm catmasks
rm images
rm models/*
rm log.txt
cp ../../imagematting1702/all_* .
ln -s ../../imagematting1702/images_data/ images_data
ln -s ../../imagematting1702/images_binary_mask/ images_binary_mask
mv allconv6.prototxt allconv4.prototxt
mv allconv6.solver allconv4.solver
mv allconv6.sh allconv4.sh


