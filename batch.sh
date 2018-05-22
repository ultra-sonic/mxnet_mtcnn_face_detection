#./main.py
export PYTHONPATH=$PYTHONPATH:"/usr/local/lib/python2.7/site-packages/"
pushd /home/omarkowski/dev/mxnet_mtcnn_face_detection
rootdir="/data_100G/Linus_Timelapse"
dirs=$rootdir/201[0-9][0-9][0-9][0-9][0-9]
for dir in $dirs;
do
	if [ -d "$dir" ]; then
		echo "------"
		echo $dir
		./main_baby.py $dir
		if [ $? -eq 0 ]
		then
		  sleep 5 # wait just in case the last file handle has not been properly closed yet
		  mv $dir "$rootdir/processed/"
		fi
	else # if dir does not exist
		echo "No dir found - something is wring - sending a mail."
		echo "No images found for yesterday!" | mutt -s "Linus Timelapse // possible problem"  owski.himself@gmail.com
	fi
done
popd
# rsync -av /data_6tb/Linus_Timelapse/faces/ /data_6tb_backup/Linus_Timelapse/faces/
# read -p "Enter please..."
