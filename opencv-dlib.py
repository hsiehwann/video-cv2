import dlib
import cv2


cap = cv2.VideoCapture('mv.mp4')  # 開啟影片檔案

w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 取得畫面尺寸
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 使用 XVID 編碼
cap.set(cv2.CAP_PROP_POS_MSEC, 10000)  # 從第 10 秒開始撥放

# 建立 VideoWriter 物件，輸出影片至 output.avi，FPS 值為 20.0
out = cv2.VideoWriter('mv.mp4', fourcc, fps, (w, h))

detector = dlib.get_frontal_face_detector()  # Dlib 的人臉偵測器

while (cap.isOpened() and cap.get(cv2.CAP_PROP_POS_MSEC)) < 20000:  # 以迴圈從影片檔案讀取影格，並顯示出來
    ret, frame = cap.read()
    if ret:

        face_rects, scores, idx = detector.run(frame, 0, -.5)  # 偵測人臉
        for i, d in enumerate(face_rects):  # 取出所有偵測的結果
            x1 = d.left();
            y1 = d.top();
            x2 = d.right();
            y2 = d.bottom()
            text = f'{scores[i]:.2f}, ({idx[i]:0.0f})'

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4, cv2.LINE_AA)  # 以方框標示偵測的人臉
            cv2.putText(frame, text, (x1, y1), cv2.FONT_HERSHEY_DUPLEX,  # 標示分數
                        0.7, (255, 255, 255), 1, cv2.LINE_AA)

        cv2.imshow('Face Detection', frame)  # 顯示結果
        out.write(frame)  # 寫入影格

    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
out.release()
cv2.destroyAllWindows()
cv2.waitKey(1)