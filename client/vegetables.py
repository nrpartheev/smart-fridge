import cv2
import time
import requests
import io
import os

def get_items_name(file):
    with open(file, 'rb') as file:
        files = {'file': ('hand.png', file, 'image/png')}
        try:
            response = requests.post('http://127.0.0.1:5000/detectitems', files=files)
        except requests.RequestException as e:
            print(f"Error sending image: {e}")
        
        if response.text != "problem":
            return eval(response.text)
        
        else:
            return "problem"


