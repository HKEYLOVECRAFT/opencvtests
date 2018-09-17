import cv2
import datetime
import numpy as np
import time
import requests

# start video capture, get first frame and convert it to grayscale
cap = cv2.VideoCapture(0)
ret, first_frame = cap.read()
first_frame_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)

# convert first frame to array and get its dimensions
first = np.asarray(first_frame_gray)
first_rows, first_cols = first.shape

roi = None

# initialize Time variables
currentTime = time.time()
# - float(15) to skip the first loop of "if currentTime - previousTime >= 15.0:"
previousTime = time.time() - float(15)
print currentTime, previousTime

# start looping over the frames
while(cap.isOpened()):

    # if streaming ends or frame is not received, end loop
    (grabbed, frame) = cap.read()

    if not grabbed:
        break

    # convert current frame to grayscale
    current_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    current = np.asarray(current_frame_gray)


    if roi is not None:
        # roi = (x, y, w, h)

        # crop frame to given parameters
        cropped = current[int(roi[1]): int(roi[1]+roi[3]), int(roi[0]): int(roi[0]+roi[2])]

        # copy rows and columns from cropped frame
        first_rows, first_cols = cropped.shape

        # pts = right top, right bottom, left top, left bottom
        pts = [int(roi[1]), int(roi[1]+roi[3]), int(roi[0]), int(roi[0]+roi[2])]
        cv2.rectangle(current, (pts[2], pts[0]), (pts[3], pts[1]), (255, 255, 255), 2)

        current = cropped

        # crop first frame to given parameters
        first = first_frame_gray[int(roi[1]): int(roi[1]+roi[3]), int(roi[0]): int(roi[0]+roi[2])]

    # threshold the image, so that every pixel value below 20 will be set to zero and above 20
    # to 255
    ret, thresh = cv2.threshold(first - current, 20, 255, cv2.THRESH_BINARY)

    # calculate the nonzero pixels in thresh frame
    diff = float(cv2.countNonZero(thresh))

    # divide the diff value with the total number of pixels in frame
    diff_value = float(diff / (first_rows * first_cols)) * 100

    # check to see if it's time to update frames. That is, if the difference
    # between the current time and last time the frames were updated is bigger than the interval
    currentTime = time.time()
    if currentTime - previousTime >= 15.0:

        # save the last time frames were updated
        previousTime = currentTime

        if diff_value >= 75:

            timestamp = datetime.datetime.now().strftime("%A %d %m %Y %H:%M:%S")
            params = {"difference": int(diff_value), "time": timestamp}
            r = requests.post("http://localhost:8080/data", data=params)
            print(r)

        # draw the text and timestamp on the frame
        cv2.putText(current_frame_gray, "Difference: {}%".format(str(round(diff_value,1))), (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(current_frame_gray, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
            (10, current_frame_gray.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)

        # show the frames and wait until user presses a key
        cv2.imshow('Current', current_frame_gray)
        cv2.imshow('Threshold', thresh)
        cv2.imshow('First', first)

    key = cv2.waitKey(1) & 0xFF

    # if 'i' is pressed, go to selectROI mode
    if key == ord('i'):

        fromCenter = False
        showCrosshair = False
        roi = cv2.selectROI("Current", current, fromCenter, showCrosshair)
        print roi

    # if 'q' is pressed, quit program
    if key == ord('q'):
        break

# release capture
cap.release()
cv2.destroyAllWindows()