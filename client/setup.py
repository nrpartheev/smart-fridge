import cv2
import time
import requests
import io
import os
from chat import say

def setup(itemname):
    display_time = 10
    output_folder = "bounding_box_frames/" 
    frame_rate = 1  
    start_time = time.time()
    cap = cv2.VideoCapture(0)
    while True:
        print("count")
        ret, frame = cap.read()
        height, width = frame.shape[:2]

        box_width = width // 2
        box_height = height

        start_x = (width - box_width) // 2
        start_y = 0
        end_x = start_x + box_width
        end_y = start_y + box_height

        content = frame[start_y:end_y, start_x:end_x]

        elapsed_time = int(time.time() - start_time)

        if elapsed_time < display_time:
            timer = display_time - elapsed_time
            cv2.putText(frame, f"Timer: {timer}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
        cv2.rectangle(frame, (start_x-1, start_y-1), (end_x+1, end_y+1), (0, 255, 0), 1)
        cv2.imshow('Camera Feed', frame)

        if elapsed_time % frame_rate == 0 and elapsed_time > 0:
            file_name = f"frame_{elapsed_time}.png"
            cv2.imwrite(f"{output_folder}{file_name}", content)

        if elapsed_time >= display_time:
            break

    os.system("zip -r bound.zip bounding_box_frames")

    with open(f"bound.zip", 'rb') as file:
        files = {'file': ("bound.zip", file, 'application/zip')}
        try:
            response = requests.post('http://127.0.0.1:5000/setup?item='+itemname, files=files)
        except requests.RequestException as e:
            print(f"Error sending image: {e}")
    
    os.system("rm bound.zip")
    say("Scanning has been successfully completed. It will take sometime for change to be reflected.")



