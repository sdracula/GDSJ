import sys
import cv2
import numpy as np

ball_color = 'green'

color_dist = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([6, 255, 255])},
              'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
              'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
              }
cap = cv2.VideoCapture(0)
cv2.namedWindow('camera', cv2.WINDOW_AUTOSIZE)
while cap.isOpened():
    ret, frame = cap.read()
    
    if ret:
        if frame is not None:
            gs_frame = cv2.GaussianBlur(frame, (5, 5), 0)                     # 高斯模糊
            hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)                 # 转化成HSV图像
            erode_hsv = cv2.erode(hsv, None, iterations=2)                   # 腐蚀 粗的变细

            inRange_hsv1 = cv2.inRange(erode_hsv, color_dist['green']['Lower'], color_dist['green']['Upper'])
            inRange_hsv2 = cv2.inRange(erode_hsv, color_dist['blue']['Lower'], color_dist['blue']['Upper'])
            inRange_hsv3 = cv2.inRange(erode_hsv, color_dist['red']['Lower'], color_dist['red']['Upper'])
            #inRange_hsv4 = cv2.inRange(erode_hsv, color_dist['grey']['Lower'], color_dist['grey']['Upper'])
            cnts1 = cv2.findContours(inRange_hsv1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            cnts2 = cv2.findContours(inRange_hsv2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            cnts3 = cv2.findContours(inRange_hsv3.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            #cnts4 = cv2.findContours(inRange_hsv3.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

            if cnts3!=[] :
                c3 = max(cnts3, key=cv2.contourArea)
                rect3 = cv2.minAreaRect(c3)
                box3 = cv2.boxPoints(rect3)
                cv2.drawContours(frame, [np.int0(box3)], -1, (0, 255, 255), 2)

            if cnts1!=[]:
                leng = len(cnts1)
                
                cnts31=sorted(cnts1, key = lambda a: cv2.contourArea(a), reverse=True)
            #     c1 = max(cnts1,key=cv2.contourArea)
            #     # if 1.2*cv2.contourArea(c3)<cv2.contourArea(c1):
            #     #     cnts31=sorted(cnts1, key = lambda a: cv2.contourArea(a), reverse=True)
            #     #     c1 = cnts31[1]
            #     #     print(1)
            #     # else:
            #     #     c1 = max(cnts1,key=cv2.contourArea)
            #     #     print(2)
            # #c4 = max(cnts4, key=cv2.contourArea)

            #改成长宽比判断 若长宽比异常，结束
                if leng == 1:
                    c1 = cnts31[0]
                    rect1 = cv2.minAreaRect(c1)
                    box1 = cv2.boxPoints(rect1)            

                if leng >= 2:
                    c11 = cnts31[0]
                    rect11 = cv2.minAreaRect(c11)
                    c12 = cnts31[1]
                    rect12 = cv2.minAreaRect(c12)
                    print(rect11[0][1],rect12[0][1])
                    if rect11[0][1]<rect12[0][1]:           
                    #rect4 = cv2.minAreaRect(c4)
                        box1 = cv2.boxPoints(rect11)
                    else:
                        box1 = cv2.boxPoints(rect12)
                #box4 = cv2.boxPoints(rect3)
                
                cv2.drawContours(frame, [np.int0(box1)], -1, (0, 255, 255), 2)

            if cnts2!=[] :
                c2 = max(cnts2, key=cv2.contourArea)
                rect2 = cv2.minAreaRect(c2)
                box2 = cv2.boxPoints(rect2)
                cv2.drawContours(frame, [np.int0(box2)], -1, (0, 255, 255), 2)

            

            cv2.imshow('camera', frame)
            a = cv2.waitKey(2)
            if a == ord('1'):
                sys.exit(1)
        else:
            print("无画面")
    else:
        print("无法读取摄像头！")
cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows() 
