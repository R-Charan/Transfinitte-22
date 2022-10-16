# Importing header files 
import imutils
import numpy as np
import requests
import cv2
import matplotlib.pyplot as plt

#Assigning URL for communication

# url = "http://10.2.228.93:8080/shot.jpg"

url = "http://192.68.4.1:80"


import torch

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

#display lines based on Hough Space calculations

def line_display(image,lines):
	line_image = np.zeros_like(image)
	if lines is not None:
		for line in lines:
			x1,y1,x2,y2 = line.reshape(4)
			cv2.line(line_image , (x1,y1),(x2,y2) , (255,0,0) , 10)
	return line_image

# Canny

def Canny(image):
    image = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(image , 100 ,200)
    return canny

# Region of Interest

def ROI(image):
    height = image.shape[0]
    width = image.shape[1]
    region =np.array([[(0,height),(width/2 , height/2), (width , height)]] , dtype=np.int32)
    mask = np.zeros_like(image)
    cv2.fillPoly(mask , region, 255)
    masked_image = cv2.bitwise_and(image , mask)
    return masked_image

# While loop to continuously fetching data from the Url

while True:
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img = imutils.resize(img, width=640, height=480)
    results = model(img)
    canny = Canny(img)
    masked = ROI(canny)
    lines = cv2.HoughLinesP(masked , 2, np.pi/180, 100, np.array([]),minLineLength =40 , maxLineGap =5)
    line_value = line_display(img, lines)
    combo = cv2.addWeighted(img , 0.8 , line_value ,1,1 )
    full_combo = cv2.addWeighted(combo , 0.8 , np.squeeze(results.render()) ,1,1 )
    cv2.imshow("Lane" , full_combo)    
     


    # Press Esc key to exit
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()