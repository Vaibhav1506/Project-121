from distutils.archive_util import make_archive
import re
import cv2 
import time
from cv2 import merge
import numpy as np

fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_videofile = cv2.VideoWriter('Output.avi', fourcc, 20.0, (640,480))
web_cap = cv2.VideoCapture(0)

time.sleep(2)
bg = 0

for i in range(0,60):
    ret, bg = web_cap.read()

bg = np.flip(bg, axis = 1)

while(web_cap.isOpened()):
    ret, img = web_cap.read()
    
    if not ret:
        break
    img = np.flip(img, axis = 1)
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    l_black = np.array([104,153,70])
    u_black = np.array([30,30,0])
    mask_1 = cv2.inRange(hsv, l_black, u_black)
    
    l_black = np.array([104,153,70])
    u_black = np.array([30,30,0])
    mask_2 = cv2.inRange(hsv, l_black, u_black)
    
    mask_1 = mask_1 + mask_2

    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_DILATE, np.ones((3,3), np.uint8))

    mask_2 = cv2.bitwise_not(mask_1)

    res_1 = cv2.bitwise_and(img, img, mask = mask_2)
    res_2 = cv2.bitwise_and(bg, bg, mask = mask_1)

    final_Output = cv2.addWeighted(res_1, 1, res_2, 1, 0)
    output_videofile.write(final_Output)

    cv2.imshow("INVISIBILITY CLOAK", final_Output)
    cv2.waitKey(1)

web_cap.release()

output_videofile.release()

cv2.destroyAllWindows()