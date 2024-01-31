from flask import Flask, request, render_template, send_file
from ultralytics import YOLO
import os
import cv2
from roboflow import Roboflow
import yaml

rf = Roboflow(api_key="--PROVIDE ROBOFLOW API KEY--")
project = rf.workspace().project("vegetables-el4g6")
app = Flask(__name__)

ZIP_FOLDER = 'zip'
if not os.path.exists(ZIP_FOLDER):
    os.makedirs(ZIP_FOLDER)


HAND_FOLDER = 'hand_upload'
if not os.path.exists(HAND_FOLDER):
    os.makedirs(HAND_FOLDER)

app.config['ZIP_FOLDER'] = ZIP_FOLDER
app.config['HAND_FOLDER'] = HAND_FOLDER



# "found"
@app.route('/hand', methods=['POST'])
def findhand():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        filename = "temp.png"
        file_path = os.path.join(app.config['HAND_FOLDER'], filename)
        file.save(file_path)
        model = YOLO('/Users/nrpartheev/Desktop/MMDS/static/content/runs/detect/train2/weights/best.pt')
        results = model(file_path)
        threshold = 0.79
        for i in results[0].boxes.conf:
            if i > threshold:
                return "found"
    
    return "not found"
    
@app.route('/detectitems', methods=['POST'])
def detect():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        filename = "temp.png"
        file_path = os.path.join(app.config['HAND_FOLDER'], filename)
        file.save(file_path)
        model = project.version(1).model
        obj = model.predict("hand_upload/temp.png", confidence=75, overlap=30).json()
        items = []
        for i in obj['predictions']:
            items.append(i['class'])

        return str(set(items))

    else:
        return "problem"



@app.route('/setup', methods=['POST'])
def setup():
    os.system('mkdir data')
    os.system('mkdir data/train')
    os.system('mkdir data/test')
    os.system('mkdir data/val')
    os.system('mkdir data/train/images')
    os.system('mkdir data/train/labels')
    os.system('mkdir data/test/images')
    os.system('mkdir data/test/labels')
    os.system('mkdir data/val/images')
    os.system('mkdir data/val/c')
    count = 0
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        filename = "temp.zip"
        file_path = os.path.join(app.config['ZIP_FOLDER'], filename)
        file.save(file_path)
        itemname = request.form.get('item')
        print("ITEMNAME:",itemname)
        os.system('unzip zip/temp.zip')
        os.system('mv bounding_box_frames/* data/train/images/ ')
        os.system('cp data/train/images/* data/train/images/*')
        os.system('cp data/train/images/* data/val/images/*')

        data = {
            'train': 'train/images',
            'val': 'valid/images',
            'test': 'test/images',
            'nc': 1,
            'names': [itemname],
        }

        with open('data/data.yaml', 'w') as file:
            yaml.dump(data, file)

        files = os.listdir('data/train/images')
        for file in files:
            filename, extension = os.path.splitext(file)
            new_filename = filename + '.txt'
            new_file_path = 'data/train/labels/' + new_filename
            with open(new_file_path, 'w') as new_file:
                new_file.write('1 1 1 1 1\n')

        os.system('cp data/train/labels data/test/labels')
        os.system('cp data/test/labels data/val/labels')

        os.system('yolo task=detect mode=train model=yolov8s.pt data=data/data.yaml epochs=100 imgsz=640')

        os.system('rm -rf data')
        os.system('rm -rf bouding_box_frames')
        return f'File {filename} uploaded successfully. Item name: {itemname}'

    return 'Error uploading file'

if __name__ == '__main__':
    app.run(debug=True)
