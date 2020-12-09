import cv2
from datetime import datetime


""" capture the smiles """
def smile_detector(frame, gray_frame, face_cascade, smile_cascade, smile_flag, smiles_list, smiles_time):
    '''
    using haarcascade, this function search for faces in frame 
    then search for beautiful smiles in faces
    and finally take a picture for that frame 
    and save the time of the happy momment to be a good memory
    '''

    faces = face_cascade.detectMultiScale(gray_frame, 1.1, 4)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray_frame[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        smiles = smile_cascade.detectMultiScale(roi_gray, 1.2, 15)

        for (xs, ys, ws, hs) in smiles:
            smile_flag = 1
            cv2.rectangle(roi_color, (xs, ys), (xs+ws, ys+hs), (0, 0, 255), 2)

        smiles_list.append(smile_flag)

    # to save memory
    smiles_list = smiles_list[-2:]

    # to save images of each smile when it starts, and save the when
    if smiles_list[-1] == 1 and smiles_list[-2] == 0:
        cv2.imwrite(f"out\\imgs\\smile{datetime.now().strftime(r'%d%m%Y%H%M%S')}.jpg", frame)
        smiles_time.append(datetime.now().strftime(r'%A %d %B %Y %I:%M:%S %p'))

    return smiles_list