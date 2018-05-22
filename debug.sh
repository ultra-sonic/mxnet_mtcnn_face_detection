#./main.py
export PYTHONPATH=$PYTHONPATH:"/usr/local/lib/python2.7/site-packages/"
pushd /home/omarkowski/dev/mxnet_mtcnn_face_detection
./main.py $1
popd
#read -p "Enter please..."