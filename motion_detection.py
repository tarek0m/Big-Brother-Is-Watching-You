import cv2
from datetime import datetime


""" detect the motion """
def motion_detector(frame, cnts, cap_flag, motion_flag, status_list, motion_time, out):
    '''
    detect the motion using the value of contours
    writes the state of movement
    write the date and time on live videos
    '''
    text = 'No Motion'        
    for cnt in cnts:
        if cv2.contourArea(cnt) < 700:
            continue

        text = 'Motion'

        motion_flag = 1
        #(x, y, w, h) = cv2.boundingRect(cnt)
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)

    status_list.append(motion_flag)

    # to save memory
    status_list = status_list[-2:]

    if status_list[-1] == 1 and status_list[-2] == 0:
        motion_time.append(datetime.now())

    if status_list[-1] == 0 and status_list[-2] == 1:
        motion_time.append(datetime.now())

    font = cv2.FONT_HERSHEY_SIMPLEX

    cv2.putText(frame, f'[+] Room Status: {text}', (10, 20), font, 0.5, (0, 0 ,255), 1, cv2.LINE_AA)

    if cap_flag == 1:
        cv2.putText(frame, datetime.now().strftime(r'%A %d %B %Y %I:%M:%S %p'), 
                    (10, frame.shape[0]-10), font, 0.5, (0, 0 ,255), 1, cv2.LINE_AA)

    # write in case of motion
    if motion_flag == 1:
        out.write(frame)
    
    return (motion_flag, status_list)