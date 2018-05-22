rootdir="/data_100G/Linus_Timelapse/chips"
files="$rootdir/201710*/*.jpg"
for f in $files;
do
	echo "------"
	echo $f
	/home/omarkowski/dev/mxnet-face/attribute/predict.sh $f
	if [ $? -eq 0 ]
	then
	  cp $f "${rootdir}Smiling/"
	fi
	
done
#read -p "Enter please..."
