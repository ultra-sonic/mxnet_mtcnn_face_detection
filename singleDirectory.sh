#./main.py
export PYTHONPATH=$PYTHONPATH:"/usr/local/lib/python2.7/site-packages/"
pushd /home/omarkowski/dev/mxnet_mtcnn_face_detection
dir=$1
echo "------"
echo $dir
./main_baby.py $dir
if [ $? -eq 0 ]
then
  sleep 5 # wait just in case the last file handle has not been properly closed yet
  mv $dir /data_6tb/Linus_Timelapse/processed/
fi
popd
rsync -av /data_6tb/Linus_Timelapse/faces/ /data_6tb_backup/Linus_Timelapse/faces/
