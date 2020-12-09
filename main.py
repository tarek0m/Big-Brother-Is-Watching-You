#! python3

""" imports """
import cv2
import time
from datetime import datetime
import numpy as np
import pandas
import sqlite3
from motion_detection import *
from smile_detection import *
from frame_operations import *
from object_detection import *
from plot import *
from read_csv_files import *



if __name__ == '__main__':

    # DataFrame to visualize the time when motion occurs
    motion_df = pandas.DataFrame(columns=["Start", "End"])

    """ __init__ for frame_ops func """
    thresh_of_delta = 30

    """ __init__ for motion_detector func """
    motion_flag = 0
    status_list = [None, None]
    motion_time = []

    """ __init__ for object_detector func """
    thresh_of_obj = 0.5
    nms_threshold = 0.2
    objects_dict = {}
    object_flag = 0
    class_names = []
    class_file = r'resources\libs\coco.names'
    with open(class_file, 'rt') as f:
        class_names = f.read().rstrip('\n').split('\n')
    config_path = r'resources\libs\ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    weights_path = r'resources\libs\frozen_inference_graph.pb'
    net = cv2.dnn_DetectionModel(weights_path, config_path)
    net.setInputSize(320, 320)
    net.setInputScale(1.0 / 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)

    """ __init__ for smile_detector func """
    face_cascade = cv2.CascadeClassifier(r"resources\libs\haarcascade_frontalface_default.xml")
    smile_cascade = cv2.CascadeClassifier(r"resources\libs\haarcascade_smile.xml")
    smile_flag = 0
    smiles_list = [None, None] # count the smiles and when
    smiles_time = []

    """ capturing the video """
    cap_flag = 0
    vid_src = input("Enter number of cam (0 is default) or video local URL: ")
    if -1 < len(vid_src) < 1:
        vid_src = 0
        cap_flag = 1
    elif vid_src.isnumeric():
        vid_src = int(vid_src)
        cap_flag = 1
    else:
        print("Sorry.. we stopped this functionality for technical issues!\nWe promise we will get it back as soon as possible.")
        exit(0)
    
    cap = cv2.VideoCapture(vid_src)

    x, y = (cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    """ if cap_flag == 1:
        fps = cap.get(cv2.CAP_PROP_FPS) / 6
    else:
        fps = cap.get(cv2.CAP_PROP_FPS) """

    fps = cap.get(cv2.CAP_PROP_FPS) / 6

    out = cv2.VideoWriter(f"out\\vids\\mov{datetime.now().strftime(r'%d%m%Y%H%M%S')}.avi", cv2.VideoWriter_fourcc(*"XVID"), fps, (int(x), int(y)))

    # __init__ for the frame that is compared with
    # the next frame to detect the delta in pixels
    source_frame = None

    """ loop through video frames """
    while True:
        ret, frame = cap.read()
        
        if ret == False:
            # break the loop if can't read the frame
            break

        modified_thresh, gray_frame = frame_ops(frame, source_frame, thresh_of_delta)

        # CHAIN_APPROX_SIMPLE removes the redundent points saving memory
        cnts = cv2.findContours(modified_thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

        objects_detector(class_names, net, frame, thresh_of_obj, nms_threshold, objects_dict, object_flag)

        the_motion_flag, status_list = motion_detector(frame, cnts, cap_flag, motion_flag, status_list, motion_time, out)

        smiles_list = smile_detector(frame, gray_frame, face_cascade, smile_cascade, smile_flag, smiles_list, smiles_time)

        # as inthe next iteration "gray = blur" 
        source_frame = gray_frame

        # show the main frame with the drawings
        cv2.imshow("Vid", frame)

        # (esc) to exit 
        if cv2.waitKey(1) & 0xFF == 27:
            break

    if the_motion_flag == 1:
        motion_time.append(datetime.now())

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # iterate through the times when motion start and end, and save them in a data frame
    for i in range(0, len(motion_time), 2):
        motion_df = motion_df.append({"Start": motion_time[i], "End": motion_time[i+1]}, ignore_index= True)

    # save the data frame in a csv
    motion_df.to_csv(f"out\\logs\\motion{datetime.now().strftime(r'%d%m%Y%H%M%S')}.csv")

    plot(read_csv_files())