import cv2


""" operatoins on frame """
def frame_ops(frame, source_frame, thresh_of_delta):
    '''
    operate the main operations on the frame:
        (cvt to 1 channel grayscale)
        (blur using a Gaussian kernel to remove the Gaussian noise)
        (blur using a box filter):
            It simply takes the average of all the pixels
            under the kernel area and replaces the central element
    returns <tuple> (morph_img, gray_frame)
    '''
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gaussian_frame = cv2.GaussianBlur(gray_frame, (11, 11), 0)
    blur_frame = cv2.blur(gaussian_frame, (3, 3))

    gray_frame = blur_frame

    if source_frame is None:
        source_frame = gray_frame
    else:
        pass

    # the change in pixels between the current and the previous frame
    frame_delta = cv2.absdiff(source_frame, gray_frame)

    # change the delta frame pixels with values > thresh_of_delta to white (1) 
    # and the others to black (0)
    thresh = cv2.threshold(frame_delta, thresh_of_delta, 225, cv2.THRESH_BINARY)[1]
    modified_thresh = cv2.dilate(thresh, None, iterations=4)
    modified_thresh = cv2.erode(modified_thresh, None, iterations=2)

    return (modified_thresh, gray_frame)
