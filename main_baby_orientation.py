#!/usr/bin/env python
# coding: utf-8
import cv2
import mxnet as mx
from mtcnn_detector import MtcnnDetector
import os
import shutil
import time
import sys
import exifread

detector = MtcnnDetector(model_folder='model', minsize = 200, ctx=mx.cpu(0), num_worker = 4 , accurate_landmark = False)


#img = cv2.imread('test2.jpg')
#directory='/data_6tb_backup/Linus_Timelapse/faces/20170218/'
if len(sys.argv) > 1:
    directory=sys.argv[1]
    if directory=="":
        raise ValueError("no directory given")
    startdate=sys.argv[2]
    if startdate=="":
        raise ValueError("no startdate given")
    #face_dir='/data_6tb/Linus_Timelapse/faces/'
    datedirs=sorted( os.listdir( directory ) )
    count=0

    # store previous and next file for copying later if a face is found in the current file
    max_sourouding_files=2
    prevfile=None
    force_nextfile=False

    for d in datedirs:
      # if f.endswith(".jpg"):
        # filedate=f.split("_")[2]
     try:
      if int(d)>=int(startdate):
        files=sorted( os.listdir( os.path.join( directory,d) ) )
        for f in files:
          if os.path.exists( os.path.join( directory.replace('faces','chips') , d , 'chip_'+f.rstrip('.jpg')+'_0.jpg') )==False: #check if this chip already exists - skip if true
            current_file = os.path.join( directory,d,f)
            print f
            img  = cv2.imread( current_file )
            #rotate image 90 degrees for detector - lossless
            img = cv2.transpose(img)
            img = cv2.flip(img, 1)  # transpose+flip(1)=CW
            # run detector
            results = detector.detect_face(img)

            if results is not None:

                total_boxes = results[0]
                points = results[1]

                # get frame date
                # timestamp=time.strftime('%d.%m.%Y', time.gmtime(os.path.getctime( current_file )))
                exiffile = open( current_file , 'rb')
                tags = exifread.process_file(exiffile, stop_tag='DateTimeOriginal')
                tsarray = str( tags["EXIF DateTimeOriginal"] ).split(" ")[0].split(":")
                #timestamp  = tsarray[2] + "." + tsarray[1] + "." + tsarray[0]
                timestamp = ".".join( reversed(tsarray) )
                exiffile.close()

                # extract aligned face chips
                chips = detector.extract_image_chips( img, points, 768, 1.0, timestamp )
                for i, chip in enumerate(chips):
                    #cv2.imshow('chip_'+str(i), chip)
                    outDir=os.path.join( directory.replace('faces','chips') , d)
                    if not os.path.isdir( outDir):
                        os.makedirs( outDir )
                        print "makedir " + outDir
                    outFile=os.path.join( outDir , 'chip_'+f.rstrip('.jpg')+"_"+str(i)+'.jpg')
                    cv2.imwrite( outFile, chip)
                    print outFile
     except ValueError:
      pass

# --------------
# test on camera
# --------------
'''
camera = cv2.VideoCapture(0)
while True:
    grab, frame = camera.read()
    img = cv2.resize(frame, (320,180))

    t1 = time.time()
    results = detector.detect_face(img)
    print 'time: ',time.time() - t1

    if results is None:
        continue

    total_boxes = results[0]
    points = results[1]

    draw = img.copy()
    for b in total_boxes:
        cv2.rectangle(draw, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), (255, 255, 255))

    for p in points:
        for i in range(5):
            cv2.circle(draw, (p[i], p[i + 5]), 1, (255, 0, 0), 2)
    cv2.imshow("detection result", draw)
    cv2.waitKey(30)
'''
