#!/usr/bin/env python
# coding: utf-8
import cv2
import mxnet as mx
from mtcnn_detector import MtcnnDetector
import os
import shutil
import time
import sys

#detector = MtcnnDetector(model_folder='model', minsize = 200, ctx=mx.cpu(0), num_worker = 4 , accurate_landmark = False)
detector = MtcnnDetector(model_folder='model', minsize = 200, num_worker = 4 , accurate_landmark = False)


#img = cv2.imread('test2.jpg')
#directory='/data_6tb_backup/Linus_Timelapse/20170218/'
if len(sys.argv) > 1:
    directory=sys.argv[1]
    face_dir=os.path.join ( os.path.dirname( directory.rstrip( "/" ) ) , "faces" , os.path.basename( directory.rstrip("/") ) )  #'/data_100G/Linus_Timelapse/faces/'
    if not os.path.isdir( face_dir ):
        os.makedirs( face_dir )
        print "created faces directory: " + face_dir
    files=sorted( os.listdir( directory ) )
    count=0

    # store previous and next file for copying later if a face is found in the current file
    max_sourouding_files=2
    prevfile=None
    force_nextfile=False

    for f in files:
        if f.endswith(".jpg"):
            current_file = os.path.join( directory,f)
            img  = cv2.imread( current_file )
            #rotate image 90 degrees for detector - lossless
            img = cv2.transpose(img)  
            img = cv2.flip(img, 1)  # transpose+flip(1)=CW
            # run detector
            results = detector.detect_face(img)

            if results is not None:
                target_file=os.path.join( face_dir, f )
                print ">>> Found face in: " + current_file
                if os.path.exists( target_file ) == False:
                    shutil.move( current_file , face_dir )
                #move prevfile and reset it
                #if prevfile:
                #    print "Forced copy of previous file: " + prevfile
                #    shutil.move( prevfile , face_dir )
                #    prevfile=None
                #force_nextfile=True
            #elif force_nextfile:
            #    print "Forced copy of next file: " + f
            #    shutil.move( current_file , face_dir )
            #    force_nextfile=False
            else:
                print "no copy - " + str(count) + " of " + str(len(files))
                prevfile=current_file

            count=count+1
'''    total_boxes = results[0]
    points = results[1]
    
    # extract aligned face chips
    chips = detector.extract_image_chips(img, points, 144, 0.37)
    for i, chip in enumerate(chips):
        cv2.imshow('chip_'+str(i), chip)
        cv2.imwrite('chip_'+str(i)+'.png', chip)

    draw = img.copy()
    for b in total_boxes:
        cv2.rectangle(draw, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), (255, 255, 255))

    for p in points:
        for i in range(5):
            cv2.circle(draw, (p[i], p[i + 5]), 1, (0, 0, 255), 2)

    cv2.imshow("detection result", draw)
    cv2.waitKey(0)
'''

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
