import sys
from random import randint

import cv2

tracker_types = ["BOOSTING", "MIL", "KCF", "TLD", "MEDIANFLOW", "MOSSE", "CSRT"]
tracker_type = "CSRT"

if tracker_type == "BOOSTING":
    tracker = cv2.legacy.TrackerBoosting_create()
elif tracker_type == "MIL":
    tracker = cv2.legacy.TrackerMIL_create()
elif tracker_type == "KCF":
    tracker = cv2.legacy.TrackerKCF_create()
elif tracker_type == "TLD":
    tracker = cv2.legacy.TrackerTLD_create()
elif tracker_type == "MEDIANFLOW":
    tracker = cv2.legacy.TrackerMedianFlow_create()
elif tracker_type == "MOSSE":
    tracker = cv2.legacy.TrackerMOSSE_create()
elif tracker_type == "CSRT":
    tracker = cv2.legacy.TrackerCSRT_create()

video = cv2.VideoCapture("/home/coral/Desktop/object tracking/race.mp4")
if not video.isOpened():
    print("error loading the video")
    sys.exit()

ok,frame = video.read()

if not ok:
    print("error")
    sys.exit()

bbox = cv2.selectROI(frame)
print(bbox)

ok = tracker.init(frame , bbox)

colors = (randint(0,255), randint(0,255), randint(0,255))
print(colors)

while True:

    ok,frame = video.read()

    if not ok:
        break

    ok, bbox = tracker.update(frame)

    if ok == True:

        (x,y,w,h) = [int(v) for v in bbox]
        cv2.rectangle(frame, (x,y), (x+w, y+h), colors, 2)

    else :

        cv2.putText(frame, "Tracking Failure" , (100,80), cv2.FONT_HERSHEY_SIMPLEX, .75, (0,0,255),2 )

    cv2.putText(frame, tracker_type, (100,50), cv2.FONT_HERSHEY_SIMPLEX, .75, (0,0,255), 2)

    cv2.imshow("Tracking", frame)

    if cv2.waitKey(1) & 0XFF == 27 :
        break


print(tracker)