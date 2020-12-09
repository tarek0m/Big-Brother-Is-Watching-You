import cv2
import numpy as np
from objects_count import *


""" identify the objects """
def objects_detector(class_names, net, frame, thresh_of_obj, nms_threshold, objects_dict, object_flag):
    '''
    TO BE CONTINUED...
    '''
    classIds, confs, bbox = net.detect(frame, confThreshold= thresh_of_obj)
    bbox = list(bbox)
    confs = list(np.array(confs).reshape(1, -1)[0])
    confs = list(map(float, confs))

    indices = cv2.dnn.NMSBoxes(bbox, confs, thresh_of_obj, nms_threshold= nms_threshold)

    for i in indices:
        i = i[0]
        box = bbox[i]
        x, y, w, h = box[:]
        cv2.rectangle(frame,(x, y), (x+w, y+h),color=(0,255,0),thickness=2)
        cv2.putText(frame,class_names[classIds[i][0]-1].upper(),(box[0],box[1]),
                    cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),1, cv2.LINE_AA)
        cv2.putText(frame,f'{str(round(confs[0]*100,2))}%',(box[0],box[1]+20),
                    cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),1, cv2.LINE_AA)
        
        objects_counter(objects_dict, class_names[classIds[i][0]-1])