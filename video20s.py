import numpy as np
import cv2

RECT = ((320, 20), (570, 390))
(left, top), (right, bottom) = RECT

def roiarea(frame):                  # 取出 ROI 子畫面
    return frame[top:bottom, left:right]

def replaceroi(frame, roi):             # 將 ROI 區域貼回到原畫面
    frame[top:bottom, left:right] = roi
    return frame

cap = cv2.VideoCapture('C:/Users/Tibame_T14/Desktop/opencv-video/video20s.MP4')
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('C:/Users/Tibame_T14/Desktop/opencv-video/output20s.mp4', fourcc, fps, (900,  500))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.resize(frame, (900, 500), interpolation=cv2.INTER_NEAREST)
    #frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

#roi
    if cap.get(cv2.CAP_PROP_POS_MSEC) <= 4000:
        frame = cv2.flip(frame, 1)
        roi = roiarea(frame)
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)  # BGR to HSV
        frame = replaceroi(frame, roi)  # 將處理完的子畫面貼回到原本畫面中
        cv2.rectangle(frame, RECT[0], RECT[1], (0, 0, 255), 2)
        text = '1.ROI'
        cv2.putText(frame, text, (650, 100), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 255, 255), 2, cv2.LINE_AA)

#canny
    if 4000 < cap.get(cv2.CAP_PROP_POS_MSEC) <= 8000:
        frame = cv2.Canny(frame, 120, 200)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        text = '2.CANNY'
        cv2.putText(frame, text, (650, 100), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (255, 255, 255), 2, cv2.LINE_AA)

#gray
    if 8000 < cap.get(cv2.CAP_PROP_POS_MSEC) <= 12000:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        text = '3.BGR2GRAY'
        cv2.putText(frame, text, (650, 100), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 0, 0), 2, cv2.LINE_AA)

#BGR2RGB
    if 12000 < cap.get(cv2.CAP_PROP_POS_MSEC) <= 16000:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        text = '4.BGR2RGB'
        cv2.putText(frame, text, (650, 100), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 127, 255), 2, cv2.LINE_AA)

#gradient
    if 16000 < cap.get(cv2.CAP_PROP_POS_MSEC) <= 24000:
        kernel = np.ones((3, 3), np.uint8)
        frame = cv2.morphologyEx(frame, cv2.MORPH_GRADIENT, kernel)
        text = '5.GRADIENT'
        cv2.putText(frame, text, (650, 100), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('frame', frame)
    out.write(frame)
    if cv2.waitKey(12) == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
cv2.waitKey(1)

