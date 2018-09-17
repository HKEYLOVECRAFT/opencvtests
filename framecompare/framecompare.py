import cv2
import datetime
import numpy as np

# start video capture, get first frame and convert it to grayscale
cap = cv2.VideoCapture("v4l2src ! video/x-raw,format=NV12,width=640,height=480 ! videoconvert ! appsink")
ret, first_frame = cap.read()
first_frame_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)

# convert first frame to array and get its dimensions
first = np.asarray(first_frame_gray)
first_rows, first_cols = first.shape

# start looping over the frames
while(cap.isOpened()):

    # if streaming ends or frame is not received, end loop
    (grabbed, frame) = cap.read()

    if not grabbed:
        break

    # convert current frame to grayscale
    current_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    current = np.asarray(current_frame_gray)

    # threshold the image, so that every pixel value below 125 will be set to zero and above 125 
    # to 255
    ret, thresh = cv2.threshold(first - current, 125, 255, cv2.THRESH_BINARY)


    # calculate the nonzero pixels in thresh frame
    diff = float(cv2.countNonZero(thresh))

    # divide the diff value with the total number of pixels in frame (480 x 640)
    diff_value = float(diff / (first_rows * first_cols)) * 100

    # draw the text and timestamp on the frame
    cv2.putText(current_frame_gray, "Difference: {}%".format(str(round(diff_value,1))), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(current_frame_gray, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, current_frame_gray.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 			255), 1)

    # show the current and threshold frames, press q to exit
    cv2.imshow('Current', current)
    cv2.imshow('Threshold', thresh)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release capture
cap.release()
cv2.destroyAllWindows()
