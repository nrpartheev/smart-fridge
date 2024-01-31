import cv2
import time
import requests
import io
import os

def find_hand(file):
    with open(file, 'rb') as file:
        files = {'file': ('hand.png', file, 'image/png')}
        try:
            print('sending image')
            response = requests.post('http://172.172.167.103:8080/hand', files=files)
            print(response.text)
        except requests.RequestException as e:
            print(f"Error sending image: {e}")
        
        if response.text == "found":
            return True
        
        else:
            return False

